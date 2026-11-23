from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import json
import datetime
import os
import socket
import shutil
from pathlib import Path

from app.state import app_state
from app.config import get_settings

router = APIRouter(prefix="/api", tags=["sessions"])

settings = get_settings()
ARCHIVO_REGISTRO = settings.BASE_DIR / "registro_operadores.json"


def _datos_lote():
    """Devuelve (operador, nombre, fecha) del lote abierto."""
    lote = getattr(app_state, "lote_actual", None)
    if lote and isinstance(lote, dict):
        op = lote.get("operador")
        nombre = lote.get("nombre_lote") or lote.get("nombre")
        fecha = lote.get("fecha_historica") or lote.get("fecha")
        if op and nombre and fecha:
            return op, nombre, fecha
    
    def _pick(*candidatos):
        for c in candidatos:
            v = getattr(app_state, c, None)
            if v:
                return v
        return None
    op = _pick("operador", "op", "usuario")
    nombre = _pick("nombre_lote", "lote_nombre", "nombre", "album", "nombre_album", "lote")
    fecha = _pick("fecha_historica", "fecha", "anio", "year")
    if not (op and nombre and fecha):
        attrs = [a for a in dir(app_state) if not a.startswith("_")]
        raise HTTPException(status_code=500, detail=f"No se encontraron datos del lote. Atributos disponibles: {attrs}")
    return op, nombre, fecha


def _registrar(operador, album, fecha_historica, fotos,
               aprobadas_orig=0, aprobadas_caras=0, aprobadas_ia=0, aprobadas_comp=0,
               fotos_respaldo=0,
               parcial=False, cierre=False):
    try:
        with open(ARCHIVO_REGISTRO, "r") as f:
            registros = json.load(f)
    except Exception:
        registros = []
    
    registros.append({
        "operador": operador,
        "album": album,
        "fecha_historica": fecha_historica,
        "fotos": fotos,
        "aprobadas_original": aprobadas_orig,
        "aprobadas_caras": aprobadas_caras,
        "aprobadas_ia": aprobadas_ia,
        "aprobadas_completa": aprobadas_comp,
        "fotos_respaldo": fotos_respaldo,
        "parcial": parcial,
        "cierre": cierre,
        "fecha_carga": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    with open(ARCHIVO_REGISTRO, "w") as f:
        json.dump(registros, f, indent=4)


def _bases_de(fotos):
    bases = set()
    for f in fotos:
        if f.endswith("_original.png"):
            bases.add(f[:-len("_original.png")])
        elif f.endswith("_caras.png"):
            bases.add(f[:-len("_caras.png")])
        elif f.endswith("_ia.png"):
            bases.add(f[:-len("_ia.png")])
        elif f.endswith("_completa.png"):
            bases.add(f[:-len("_completa.png")])
    return bases


def _respaldar_originales(fotos, lote_nombre, fecha, operador):
    """
    Copia las fotos originales de las bases aprobadas a la carpeta local:
    bkporiginal/[lote_nombre]_[fecha]/{base}_original.png
    e inyecta metadatos EXIF fotográficos (año histórico, software y operador).
    Garantiza que la toma original recortada/rotada quede siempre preservada.
    Retorna la cantidad de fotos respaldadas con éxito.
    """
    dir_lote_bkp = settings.DIR_BKP_ORIGINAL / f"{lote_nombre}_{fecha}"
    dir_lote_bkp.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(str(dir_lote_bkp), 0o777)
    except Exception:
        pass

    fecha_exif = f"{fecha}:01:01 12:00:00" if len(fecha) == 4 else f"{fecha} 12:00:00"
    bases = _bases_de(fotos)
    archivos_respaldo = []

    for b in bases:
        orig = settings.DIR_SESION / f"{b}_original.png"
        if orig.exists() and orig.stat().st_size > 0:
            dest = dir_lote_bkp / f"{b}_original.png"
            try:
                shutil.copy2(str(orig), str(dest))
                try:
                    os.chmod(str(dest), 0o666)
                except Exception:
                    pass
                archivos_respaldo.append(str(dest))
            except Exception as e:
                print(f"Error copiando respaldo original {orig} a {dest}: {e}")

    if archivos_respaldo:
        desc = f"Respaldo digitalizacion original (sin IA) - Lote: {lote_nombre} - Operador: {operador}"
        soft = "Desktopia Lab - Respaldo Original Local"
        for r_dest in archivos_respaldo:
            subprocess.run(
                ["exiftool",
                 f"-DateTimeOriginal={fecha_exif}",
                 f"-CreateDate={fecha_exif}",
                 f"-ImageDescription={desc}",
                 f"-Software={soft}",
                 "-overwrite_original", r_dest],
                check=False
            )

    return len(archivos_respaldo)


def _limpiar_base(base):
    for suf in ("_original.png", "_caras.png", "_ia.png", "_completa.png",
                "_original.backup.png", "_caras.backup.png", "_ia.backup.png", "_completa.backup.png"):
        r = settings.DIR_SESION / f"{base}{suf}"
        if r.exists():
            try: r.unlink()
            except Exception: pass


def _enviar_fotos(fotos, lote_nombre, fecha):
    """Inyecta metadatos EXIF descriptivos, crea carpeta NAS y rsync. Devuelve True si envío OK."""
    fecha_exif = f"{fecha}:01:01 12:00:00" if len(fecha) == 4 else f"{fecha} 12:00:00"
    for foto in fotos:
        ruta = settings.DIR_SESION / foto
        if ruta.exists():
            if foto.endswith("_completa.png"):
                desc = "Restauracion completa con IA (GFPGAN Rostros + Real-ESRGAN 4x)"
                soft = "Desktopia Lab - Completa (GFPGAN + Real-ESRGAN)"
            elif foto.endswith("_caras.png"):
                desc = "Rostros restaurados con IA (GFPGAN)"
                soft = "Desktopia Lab - GFPGAN"
            elif foto.endswith("_ia.png"):
                desc = "Escalado 4x con IA (Real-ESRGAN)"
                soft = "Desktopia Lab - Real-ESRGAN"
            else:
                desc = "Digitalizacion original (sin IA)"
                soft = "Desktopia Lab - Original"

            subprocess.run(
                ["exiftool",
                 f"-DateTimeOriginal={fecha_exif}",
                 f"-CreateDate={fecha_exif}",
                 f"-ImageDescription={desc}",
                 f"-Software={soft}",
                 "-overwrite_original", str(ruta)],
                check=False
            )

    PASS_SSH = settings.NAS_PASS or os.getenv("NAS_PASS") or ""
    if not PASS_SSH:
        return False
    PASS_SSH = PASS_SSH.strip().strip("'").strip('"')
    nas_base = settings.NAS_PATH.rstrip("/")
    RUTA_NAS = f"{nas_base}/{lote_nombre}_{fecha}/"
    env_seguro = os.environ.copy()
    env_seguro["SSHPASS"] = PASS_SSH

    subprocess.run(
        ["sshpass", "-e", "ssh", "-o", "StrictHostKeyChecking=no",
         f"{settings.NAS_USER}@{settings.NAS_HOST}", f"mkdir -p '{RUTA_NAS}'"],
        env=env_seguro, check=False
    )

    archivos = [str(settings.DIR_SESION / f) for f in fotos if (settings.DIR_SESION / f).exists()]
    if not archivos:
        return False
    try:
        subprocess.run(
            ["sshpass", "-e", "rsync", "-avz", "-e",
             "ssh -o StrictHostKeyChecking=no", *archivos,
             f"{settings.NAS_USER}@{settings.NAS_HOST}:{RUTA_NAS}"],
            env=env_seguro, check=True
        )
        return True
    except Exception:
        return False


@router.get("/estado-nas")
async def estado_nas():
    """Verifica si el NAS es alcanzable en la red local (puerto 22 SSH)."""
    host = settings.NAS_HOST
    user = settings.NAS_USER
    conectado = False
    mensaje = "Desconectado"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.2)
        s.connect((host, 22))
        s.close()
        conectado = True
        mensaje = f"Conectado a {host}"
    except Exception:
        mensaje = f"No alcanzable ({host})"
    
    return {
        "conectado": conectado,
        "host": host,
        "user": user,
        "mensaje": mensaje
    }


@router.get("/estado-sesion")
async def obtener_estado_sesion():
    """
    Permite recuperar la sesión activa completa tras un refresco de pantalla (F5).
    Reconstruye el lote y las fotos que ya están en la carpeta activa.
    """
    if not app_state.album_abierto:
        return JSONResponse(
            content={
                "album_abierto": False,
                "lote": None,
                "contador_aprobadas": 0,
                "fotos_aprobadas": [],
                "fotos": []
            },
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )

    bases_dict = {}
    if settings.DIR_SESION.exists():
        for archivo in settings.DIR_SESION.iterdir():
            if not archivo.is_file() or archivo.suffix.lower() != '.png' or '.backup' in archivo.name or '.temp_input' in archivo.name:
                continue
            nombre = archivo.name
            if nombre.endswith("_original.png"):
                base = nombre[:-len("_original.png")]
                bases_dict.setdefault(base, {})["original"] = nombre
            elif nombre.endswith("_caras.png"):
                base = nombre[:-len("_caras.png")]
                bases_dict.setdefault(base, {})["caras"] = nombre
            elif nombre.endswith("_ia.png"):
                base = nombre[:-len("_ia.png")]
                bases_dict.setdefault(base, {})["ia"] = nombre
            elif nombre.endswith("_completa.png"):
                base = nombre[:-len("_completa.png")]
                bases_dict.setdefault(base, {})["completa"] = nombre

    aprobadas = set(app_state.fotos_aprobadas)
    lista_fotos = []
    for base, datos in bases_dict.items():
        aprobada = None
        for v in (datos.get("completa"), datos.get("ia"), datos.get("caras"), datos.get("original")):
            if v and v in aprobadas:
                aprobada = v
                break
        lista_fotos.append({
            "base": base,
            "original": datos.get("original"),
            "caras": datos.get("caras"),
            "ia": datos.get("ia"),
            "completa": datos.get("completa"),
            "aprobada": aprobada,
            "tiene_ia": bool(datos.get("completa") or datos.get("ia"))
        })

    lista_fotos.sort(key=lambda x: x["base"])

    return JSONResponse(
        content={
            "album_abierto": True,
            "lote": app_state.lote_actual,
            "contador_aprobadas": len(aprobadas),
            "fotos_aprobadas": list(aprobadas),
            "fotos": lista_fotos
        },
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )


@router.post("/iniciar-lote")
async def iniciar_lote(operador: str, nombre: str, fecha: str):
    app_state.iniciar_lote(operador, nombre, fecha, settings.DIR_SESION)
    return {"mensaje": "Lote iniciado"}


@router.post("/cancelar-lote")
async def cancelar_lote():
    if not app_state.album_abierto:
        return {"mensaje": "No activo"}
    app_state.cancelar_lote(settings.DIR_SESION)
    return {"mensaje": "Cancelado"}


@router.post("/enviar-lote")
async def enviar_lote():
    """Envío PARCIAL: copia las aprobadas al NAS con metadatos y deja el álbum ABIERTO."""
    if not app_state.album_abierto:
        raise HTTPException(status_code=400, detail="Inicia un lote primero.")
    fotos = list(app_state.fotos_aprobadas)
    if not fotos:
        raise HTTPException(status_code=400, detail="No hay fotos aprobadas para enviar.")

    operador, nombre, fecha = _datos_lote()

    # 1. Respaldo de originales en bkporiginal/ antes de enviar y limpiar
    cant_respaldo = _respaldar_originales(fotos, nombre, fecha, operador)

    # 2. Envío de las versiones aprobadas al servidor NAS
    if not _enviar_fotos(fotos, nombre, fecha):
        raise HTTPException(status_code=500, detail="Falló el envío al NAS. El álbum sigue abierto.")

    # Conteo por tipo de aprobación
    cant_orig = sum(1 for f in fotos if f.endswith("_original.png"))
    cant_caras = sum(1 for f in fotos if f.endswith("_caras.png"))
    cant_ia = sum(1 for f in fotos if f.endswith("_ia.png"))
    cant_comp = sum(1 for f in fotos if f.endswith("_completa.png"))

    for b in _bases_de(fotos):
        _limpiar_base(b)
        app_state.remover_foto_aprobada(f"{b}_original.png")
        app_state.remover_foto_aprobada(f"{b}_caras.png")
        app_state.remover_foto_aprobada(f"{b}_ia.png")
        app_state.remover_foto_aprobada(f"{b}_completa.png")

    _registrar(operador, nombre, fecha, len(fotos),
               aprobadas_orig=cant_orig, aprobadas_caras=cant_caras,
               aprobadas_ia=cant_ia, aprobadas_comp=cant_comp,
               fotos_respaldo=cant_respaldo,
               parcial=True)
    return {
        "mensaje": f"{len(fotos)} foto(s) enviadas al NAS ({cant_respaldo} original(es) respaldados en bkporiginal).",
        "enviadas": len(fotos),
        "respaldadas": cant_respaldo,
        "desglose": {
            "completa": cant_comp,
            "ia": cant_ia,
            "caras": cant_caras,
            "original": cant_orig
        }
    }


@router.post("/cerrar-lote")
async def cerrar_lote():
    """CIERRE de álbum: envía pendientes si quedan, registra estadísticas, limpia y vuelve al inicio."""
    if not app_state.album_abierto:
        raise HTTPException(status_code=400, detail="No abierto.")

    operador, lote_nombre, fecha = _datos_lote()
    fotos = list(app_state.fotos_aprobadas)

    enviadas_cierre = 0
    cant_orig = 0
    cant_caras = 0
    cant_ia = 0
    cant_comp = 0
    cant_respaldo = 0
    if fotos:
        cant_respaldo = _respaldar_originales(fotos, lote_nombre, fecha, operador)
        if not _enviar_fotos(fotos, lote_nombre, fecha):
            raise HTTPException(status_code=500, detail="Falló el envío al NAS; el álbum sigue abierto.")
        enviadas_cierre = len(fotos)
        cant_orig = sum(1 for f in fotos if f.endswith("_original.png"))
        cant_caras = sum(1 for f in fotos if f.endswith("_caras.png"))
        cant_ia = sum(1 for f in fotos if f.endswith("_ia.png"))
        cant_comp = sum(1 for f in fotos if f.endswith("_completa.png"))
        for b in _bases_de(fotos):
            _limpiar_base(b)

    _registrar(operador, lote_nombre, fecha, enviadas_cierre,
               aprobadas_orig=cant_orig, aprobadas_caras=cant_caras,
               aprobadas_ia=cant_ia, aprobadas_comp=cant_comp,
               fotos_respaldo=cant_respaldo,
               cierre=True)

    for f in settings.DIR_SESION.iterdir():
        if f.is_file():
            try: f.unlink()
            except Exception: pass
    app_state.cerrar_lote()

    if enviadas_cierre:
        return {"mensaje": f"Álbum cerrado. {enviadas_cierre} foto(s) enviadas al NAS ({cant_respaldo} respaldadas en bkporiginal)."}
    return {"mensaje": "Álbum cerrado."}


@router.get("/estadisticas")
async def obtener_estadisticas():
    # Conteo de fotos físicas en la carpeta bkporiginal
    total_fisico_respaldo = 0
    if settings.DIR_BKP_ORIGINAL.exists():
        total_fisico_respaldo = sum(
            1 for p in settings.DIR_BKP_ORIGINAL.rglob("*")
            if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
        )

    if not ARCHIVO_REGISTRO.exists():
        return {
            "resumen_operadores": {},
            "totales_globales": {
                "total_fotos": 0, "completa": 0, "ia": 0, "caras": 0, "original": 0,
                "total_respaldo": total_fisico_respaldo,
                "pct_completa": 0, "pct_ia": 0, "pct_caras": 0, "pct_orig": 0
            },
            "detalle_albumes": []
        }
    try:
        with open(ARCHIVO_REGISTRO, "r") as f:
            registros = json.load(f)
    except Exception:
        registros = []

    resumen = {}
    albumes_map = {}
    total_g_fotos = 0
    total_g_orig = 0
    total_g_caras = 0
    total_g_ia = 0
    total_g_comp = 0
    total_g_respaldo = 0

    for r in registros:
        op = r.get("operador", "?")
        alb = r.get("album", "?")
        fotos = r.get("fotos", 0)
        parcial = bool(r.get("parcial"))
        cierre = bool(r.get("cierre")) or not parcial

        orig = r.get("aprobadas_original", 0)
        caras = r.get("aprobadas_caras", 0)
        ia = r.get("aprobadas_ia", 0)
        comp = r.get("aprobadas_completa", 0)
        respaldo = r.get("fotos_respaldo", 0)

        # Compatibilidad con registros antiguos
        if orig == 0 and caras == 0 and ia == 0 and comp == 0 and fotos > 0:
            ia = fotos

        total_g_fotos += fotos
        total_g_orig += orig
        total_g_caras += caras
        total_g_ia += ia
        total_g_comp += comp
        total_g_respaldo += respaldo

        if op not in resumen:
            resumen[op] = {
                "albumes_completados": 0,
                "total_fotos": 0,
                "fotos_respaldo": 0,
                "envios_parciales": 0,
                "aprobadas_completa": 0,
                "aprobadas_ia": 0,
                "aprobadas_caras": 0,
                "aprobadas_original": 0,
            }
        resumen[op]["total_fotos"] += fotos
        resumen[op]["fotos_respaldo"] += respaldo
        resumen[op]["aprobadas_completa"] += comp
        resumen[op]["aprobadas_ia"] += ia
        resumen[op]["aprobadas_caras"] += caras
        resumen[op]["aprobadas_original"] += orig

        if cierre:
            resumen[op]["albumes_completados"] += 1
        else:
            resumen[op]["envios_parciales"] += 1

        key = (op, alb)
        if key not in albumes_map:
            albumes_map[key] = {
                "operador": op, "album": alb,
                "fecha": r.get("fecha_historica", ""),
                "fotos": 0,
                "fotos_respaldo": 0,
                "cerrado": False,
            }
        albumes_map[key]["fotos"] += fotos
        albumes_map[key]["fotos_respaldo"] += respaldo
        if cierre:
            albumes_map[key]["cerrado"] = True

    # Calcular porcentajes para cada operador
    for op, data in resumen.items():
        tf = data["total_fotos"]
        data["pct_completa"] = round((data["aprobadas_completa"] / tf * 100), 1) if tf > 0 else 0
        data["pct_ia"] = round((data["aprobadas_ia"] / tf * 100), 1) if tf > 0 else 0
        data["pct_caras"] = round((data["aprobadas_caras"] / tf * 100), 1) if tf > 0 else 0
        data["pct_original"] = round((data["aprobadas_original"] / tf * 100), 1) if tf > 0 else 0

    totales_globales = {
        "total_fotos": total_g_fotos,
        "completa": total_g_comp,
        "ia": total_g_ia,
        "caras": total_g_caras,
        "original": total_g_orig,
        "total_respaldo": max(total_fisico_respaldo, total_g_respaldo),
        "pct_completa": round((total_g_comp / total_g_fotos * 100), 1) if total_g_fotos > 0 else 0,
        "pct_ia": round((total_g_ia / total_g_fotos * 100), 1) if total_g_fotos > 0 else 0,
        "pct_caras": round((total_g_caras / total_g_fotos * 100), 1) if total_g_fotos > 0 else 0,
        "pct_orig": round((total_g_orig / total_g_fotos * 100), 1) if total_g_fotos > 0 else 0,
    }

    detalle = sorted(albumes_map.values(), key=lambda a: (a["operador"], a["album"]))
    return {
        "resumen_operadores": resumen,
        "totales_globales": totales_globales,
        "detalle_albumes": detalle
    }
