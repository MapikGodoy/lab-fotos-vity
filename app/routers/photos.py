from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from typing import List
from pathlib import Path
import time
import shutil
import os
import socket
import subprocess
import cv2
import numpy as np

from app.state import app_state
from app.config import get_settings
from app.services.image_processor import ImageProcessor
from app.utils.qr_generator import generate_qr_svg, generate_qr_matrix

router = APIRouter(prefix="/api", tags=["photos"])
settings = get_settings()
image_processor = ImageProcessor()

# Auto-test de verificación del generador QR con OpenCV
try:
    _test_url = "http://192.168.1.48:7777"
    _m = generate_qr_matrix(_test_url, level='M')
    _arr = (np.array(_m, dtype=np.uint8) == 0).astype(np.uint8) * 255 # True=negro(0), False=blanco(255)
    # En OpenCV: 0=negro, 255=blanco
    _arr = np.pad(_arr, 4, constant_values=255)
    _arr = cv2.resize(_arr, (330, 330), interpolation=cv2.INTER_NEAREST)
    _decoded, _bbox, _ = cv2.QRCodeDetector().detectAndDecode(_arr)
    if _decoded == _test_url:
        print(f"✅ Auto-test QR exitoso: OpenCV decodificó '{_decoded}' correctamente.")
    else:
        print(f"⚠️ Auto-test QR decodificación incompleta: '{_decoded}'")
except Exception as _e_qr:
    print(f"Aviso en test QR: {_e_qr}")

@router.get("/qr.svg")
async def obtener_qr_svg(url: str = "http://127.0.0.1:7777", size: int = 220):
    """Genera y sirve el código QR vectorial en SVG para conectar móviles."""
    svg_content = generate_qr_svg(url, size=size, margin=4)
    return Response(
        content=svg_content,
        media_type="image/svg+xml",
        headers={"Cache-Control": "no-cache"}
    )

@router.post("/aprobar/{nombre_foto}")
async def aprobar_foto(nombre_foto: str):
    """Aprueba una foto específica (original, caras, ia o completa)."""
    app_state.agregar_foto_aprobada(nombre_foto)
    return {"mensaje": "Aprobada", "foto": nombre_foto}

@router.post("/descartar/{nombre_foto}")
async def descartar_foto(nombre_foto: str):
    """Descarta un archivo individual."""
    ruta = settings.DIR_SESION / nombre_foto
    if ruta.exists():
        try:
            ruta.unlink()
        except Exception as e:
            print(f"Error eliminando {nombre_foto}: {e}")
    
    app_state.remover_foto_aprobada(nombre_foto)
    return {"mensaje": "Descartada", "foto": nombre_foto}

@router.post("/descartar-base/{nombre_base}")
async def descartar_base_completa(nombre_base: str):
    """
    Descarta completamente una foto y todas sus variantes:
    _original, _caras, _ia, _completa y sus backups.
    """
    sufijos = (
        "_original.png", "_caras.png", "_ia.png", "_completa.png",
        "_original.backup.png", "_caras.backup.png", "_ia.backup.png", "_completa.backup.png"
    )
    eliminados = []
    for suf in sufijos:
        archivo = f"{nombre_base}{suf}"
        ruta = settings.DIR_SESION / archivo
        if ruta.exists():
            try:
                ruta.unlink()
                eliminados.append(archivo)
            except Exception as e:
                print(f"Error eliminando {archivo}: {e}")
        app_state.remover_foto_aprobada(archivo)

    return {"mensaje": "Base descartada por completo", "base": nombre_base, "eliminados": eliminados}

@router.post("/cargar-fotos")
async def cargar_fotos(archivos: List[UploadFile] = File(...)):
    """
    Recibe una o más fotos subidas directamente desde disco/celular/carpeta,
    las valida y las deposita en sesion_activa como {base}_original.png.
    Devuelve la lista de bases listas para el pipeline de IA y envío al NAS.
    """
    if not app_state.album_abierto:
        raise HTTPException(status_code=400, detail="Debe iniciar un lote o sesión primero.")
    
    if not archivos:
        raise HTTPException(status_code=400, detail="No se seleccionaron archivos.")

    timestamp = int(time.time() * 1000)
    nuevas_bases = []
    
    for idx, archivo in enumerate(archivos, start=1):
        nombre_original = archivo.filename or f"foto_{idx}.png"
        ext = Path(nombre_original).suffix.lower()
        if ext not in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"):
            continue
        
        prefijo_base = f"foto_{timestamp}_{idx}"
        ruta_temp = settings.DIR_SESION / f"temp_{prefijo_base}{ext}"
        
        try:
            with open(ruta_temp, "wb") as f_out:
                shutil.copyfileobj(archivo.file, f_out)
            
            # Si es 1 solo archivo, evaluamos si es una platina escaneada con varias fotos
            if len(archivos) == 1:
                fotos_platina = image_processor.procesar_platina(
                    ruta_temp, prefijo_base, settings.DIR_SESION, forzar_recorte=False
                )
                if fotos_platina:
                    nuevas_bases.extend(fotos_platina)
                else:
                    ruta_final = settings.DIR_SESION / f"{prefijo_base}_original.png"
                    img = image_processor.cargar_imagen_tolerante(ruta_temp)
                    if img is not None:
                        cv2.imwrite(str(ruta_final), img)
                    else:
                        shutil.move(str(ruta_temp), str(ruta_final))
                    try: os.chmod(str(ruta_final), 0o666)
                    except Exception: pass
                    nuevas_bases.append(prefijo_base)
            else:
                # Múltiples archivos: cada uno es una foto directa
                ruta_final = settings.DIR_SESION / f"{prefijo_base}_original.png"
                img = image_processor.cargar_imagen_tolerante(ruta_temp)
                if img is not None:
                    cv2.imwrite(str(ruta_final), img)
                else:
                    shutil.move(str(ruta_temp), str(ruta_final))
                try: os.chmod(str(ruta_final), 0o666)
                except Exception: pass
                nuevas_bases.append(prefijo_base)
                
        except Exception as e:
            print(f"❌ Error procesando archivo subido {nombre_original}: {e}")
        finally:
            if ruta_temp.exists():
                try: ruta_temp.unlink()
                except Exception: pass
                
    if not nuevas_bases:
        raise HTTPException(status_code=400, detail="No se pudo procesar ninguna de las fotos seleccionadas.")
    
    return {
        "mensaje": f"{len(nuevas_bases)} foto(s) importada(s) correctamente.",
        "fotos_listas": nuevas_bases
    }

def _obtener_ips_locales():
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and ip not in ips:
            ips.append(ip)
    except Exception:
        pass

    try:
        res = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=2)
        for ip in res.stdout.strip().split():
            if not ip.startswith("127.") and not ip.startswith("172.17.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    if not ips:
        ips.append("127.0.0.1")
    return ips

@router.get("/info-red")
async def info_red():
    """Devuelve las IPs locales para conectar celulares en la misma red Wi-Fi."""
    ips = _obtener_ips_locales()
    puerto = settings.PORT
    return {
        "ips": ips,
        "puerto": puerto,
        "url_recomendada": f"http://{ips[0]}:{puerto}"
    }
