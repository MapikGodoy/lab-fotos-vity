from fastapi import APIRouter, HTTPException, Query
import cv2
import os
import shutil
import time
from pathlib import Path

from app.state import app_state
from app.config import get_settings
from app.services.ai_service import AIService

import asyncio

router = APIRouter(prefix="/api", tags=["processing"])

_base_locks = {}

def _get_base_lock(nombre_base: str) -> asyncio.Lock:
    if nombre_base not in _base_locks:
        _base_locks[nombre_base] = asyncio.Lock()
    return _base_locks[nombre_base]

settings = get_settings()
ai_service = AIService(
    dir_ia=settings.DIR_IA,
    modelo=settings.VULKAN_MODEL,
    escala=settings.VULKAN_SCALE,
    tile=settings.VULKAN_TILE,
    threads=settings.VULKAN_THREADS,
    timeout=settings.VULKAN_TIMEOUT
)

def _porcentaje_a_pixeles(x1, y1, x2, y2, ancho, alto):
    x1r = max(0, min(int(x1 / 100.0 * ancho), ancho))
    y1r = max(0, min(int(y1 / 100.0 * alto), alto))
    x2r = max(0, min(int(x2 / 100.0 * ancho), ancho))
    y2r = max(0, min(int(y2 / 100.0 * alto), alto))
    if x1r > x2r: x1r, x2r = x2r, x1r
    if y1r > y2r: y1r, y2r = y2r, y1r
    return x1r, y1r, x2r, y2r

def sincronizar_orientacion_con_original(nombre_base: str):
    """
    Garantiza que _caras, _ia y _completa tengan exactamente la misma orientación
    (vertical vs horizontal) que _original.png. Si alguna quedó desfasada, la auto-rota.
    """
    ruta_orig = settings.DIR_SESION / f"{nombre_base}_original.png"
    if not ruta_orig.exists():
        return
    img_orig = cv2.imread(str(ruta_orig))
    if img_orig is None:
        return
    alto_orig, ancho_orig = img_orig.shape[:2]
    orig_es_vertical = (alto_orig >= ancho_orig)

    sufijos = ("_caras.png", "_ia.png", "_completa.png")
    for suf in sufijos:
        ruta = settings.DIR_SESION / f"{nombre_base}{suf}"
        if ruta.exists():
            img = cv2.imread(str(ruta))
            if img is not None:
                alto, ancho = img.shape[:2]
                var_es_vertical = (alto >= ancho)
                if var_es_vertical != orig_es_vertical:
                    print(f"⚠️ Sincronizando orientación de {ruta.name} para que coincida con original...")
                    rotada = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                    cv2.imwrite(str(ruta), rotada)
                    try: os.chmod(str(ruta), 0o666)
                    except Exception: pass

@router.post("/procesar-ia/{nombre_base}")
async def procesar_ia_individual(nombre_base: str):
    """
    Procesa de forma segura:
      1. Real-ESRGAN en GPU -> {base}_ia.png (4x)
      2. GFPGAN en CPU -> {base}_caras.png (1x)
      3. GFPGAN sobre Real-ESRGAN -> {base}_completa.png (4x + Rostros)
    """
    ruta_original = settings.DIR_SESION / f"{nombre_base}_original.png"
    ruta_caras = settings.DIR_SESION / f"{nombre_base}_caras.png"
    ruta_ia = settings.DIR_SESION / f"{nombre_base}_ia.png"
    ruta_completa = settings.DIR_SESION / f"{nombre_base}_completa.png"

    if not ruta_original.exists():
        raise HTTPException(status_code=404, detail="Imagen original no encontrada")

    try:
        # Auto-orientación inteligente: solo rota si detecta personas con inclinación
        auto_rot = {"rotada": False, "grados": 0}
        try:
            auto_rot = await ai_service.detectar_y_auto_orientar_rostros(ruta_original)
        except Exception as e_rot:
            print(f"Aviso auto-orientación para {nombre_base}: {e_rot}")

        res = await ai_service.procesar_foto_completo(ruta_original, ruta_caras, ruta_ia, ruta_completa)
        sincronizar_orientacion_con_original(nombre_base)
        
        return {
            "base": nombre_base,
            "original": f"{nombre_base}_original.png",
            "caras": f"{nombre_base}_caras.png" if res.get("exito_caras") else None,
            "ia": f"{nombre_base}_ia.png" if res.get("exito_ia") else None,
            "completa": f"{nombre_base}_completa.png" if res.get("exito_completa") else None,
            "rostros_detectados": res.get("rostros_detectados", 0),
            "auto_rotada": auto_rot.get("rotada", False),
            "grados_auto_rotados": auto_rot.get("grados", 0),
            "gpu_usada": ai_service._gpu_id,
            "error": None
        }
    except Exception as e:
        print(f"❌ Error en procesar_ia_individual para {nombre_base}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "base": nombre_base,
            "original": f"{nombre_base}_original.png",
            "caras": None,
            "ia": None,
            "completa": None,
            "rostros_detectados": 0,
            "gpu_usada": ai_service._gpu_id,
            "error": str(e)
        }

@router.post("/rotar/{nombre_base}")
async def rotar_foto(nombre_base: str):
    """
    1. Asegura que todas las variantes estén sincronizadas con _original.png.
    2. Rota todas las variantes existentes 90 grados en sentido horario.
    """
    async with _get_base_lock(nombre_base):
        sincronizar_orientacion_con_original(nombre_base)
        rutas = [
            settings.DIR_SESION / f"{nombre_base}_original.png",
            settings.DIR_SESION / f"{nombre_base}_caras.png",
            settings.DIR_SESION / f"{nombre_base}_ia.png",
            settings.DIR_SESION / f"{nombre_base}_completa.png"
        ]
        rotadas = 0
        for ruta in rutas:
            if ruta.exists() and ruta.stat().st_size > 1000:
                respaldo = ruta.with_suffix('.backup.png')
                if not respaldo.exists():
                    shutil.copy2(str(ruta), str(respaldo))
                img = cv2.imread(str(ruta))
                if img is not None:
                    cv2.imwrite(str(ruta), cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
                    try: os.chmod(str(ruta), 0o666)
                    except Exception: pass
                    rotadas += 1
        
        if rotadas == 0:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes para rotar")
        return {"mensaje": "Rotada exitosamente", "variantes_rotadas": rotadas}

@router.post("/recortar/{nombre_base}")
async def recortar_foto(
    nombre_base: str,
    x1: float = Query(...), y1: float = Query(...),
    x2: float = Query(...), y2: float = Query(...)
):
    """
    Recorta in-place todas las variantes existentes conservando proporciones.
    Las versiones IA y Completa conservan su resolución nativa 4x.
    Usa bloqueo por nombre_base para evitar condiciones de carrera si se presiona varias veces.
    """
    async with _get_base_lock(nombre_base):
        sincronizar_orientacion_con_original(nombre_base)
        ruta_original = settings.DIR_SESION / f"{nombre_base}_original.png"
        ruta_caras = settings.DIR_SESION / f"{nombre_base}_caras.png"
        ruta_ia = settings.DIR_SESION / f"{nombre_base}_ia.png"
        ruta_completa = settings.DIR_SESION / f"{nombre_base}_completa.png"

        if not ruta_original.exists():
            raise HTTPException(status_code=404, detail="Imagen original no encontrada")

        # 1. Recortar Original
        respaldo_original = ruta_original.with_suffix('.backup.png')
        if not respaldo_original.exists():
            shutil.copy2(str(ruta_original), str(respaldo_original))

        img = cv2.imread(str(ruta_original))
        if img is None:
            raise HTTPException(status_code=500, detail="No se pudo cargar la imagen original")
        alto, ancho = img.shape[:2]
        x1r, y1r, x2r, y2r = _porcentaje_a_pixeles(x1, y1, x2, y2, ancho, alto)
        if (x2r - x1r) < 30 or (y2r - y1r) < 30:
            raise HTTPException(status_code=400, detail="Área de recorte muy pequeña")

        recorte_orig = img[y1r:y2r, x1r:x2r]
        cv2.imwrite(str(ruta_original), recorte_orig)
        try: os.chmod(str(ruta_original), 0o666)
        except Exception: pass

        # 2. Recortar Caras (1x)
        if ruta_caras.exists() and ruta_caras.stat().st_size > 1000:
            respaldo_caras = ruta_caras.with_suffix('.backup.png')
            if not respaldo_caras.exists():
                shutil.copy2(str(ruta_caras), str(respaldo_caras))
            img_caras = cv2.imread(str(ruta_caras))
            if img_caras is not None:
                alto_c, ancho_c = img_caras.shape[:2]
                xc1, yc1, xc2, yc2 = _porcentaje_a_pixeles(x1, y1, x2, y2, ancho_c, alto_c)
                if (xc2 - xc1) >= 30 and (yc2 - yc1) >= 30:
                    recorte_caras = img_caras[yc1:yc2, xc1:xc2]
                    cv2.imwrite(str(ruta_caras), recorte_caras)
                    try: os.chmod(str(ruta_caras), 0o666)
                    except Exception: pass

        # 3. Recortar IA 4x y Completa 4x
        if (not ruta_completa.exists() or ruta_completa.stat().st_size <= 1000) and ruta_ia.exists() and ruta_ia.stat().st_size > 1000:
            try: shutil.copy2(str(ruta_ia), str(ruta_completa))
            except Exception: pass

        for r_4x in (ruta_ia, ruta_completa):
            if r_4x.exists() and r_4x.stat().st_size > 1000:
                respaldo_4x = r_4x.with_suffix('.backup.png')
                if not respaldo_4x.exists():
                    shutil.copy2(str(r_4x), str(respaldo_4x))
                img_4x = cv2.imread(str(r_4x))
                if img_4x is not None:
                    alto_4x, ancho_4x = img_4x.shape[:2]
                    xa1, ya1, xa2, ya2 = _porcentaje_a_pixeles(x1, y1, x2, y2, ancho_4x, alto_4x)
                    if (xa2 - xa1) >= 30 and (ya2 - ya1) >= 30:
                        recorte_4x = img_4x[ya1:ya2, xa1:xa2]
                        cv2.imwrite(str(r_4x), recorte_4x)
                        try: os.chmod(str(r_4x), 0o666)
                        except Exception: pass

        return {
            "mensaje": "Recortada exitosamente",
            "dimensiones_original": f"{recorte_orig.shape[1]}x{recorte_orig.shape[0]}"
        }

@router.post("/extraer-foto/{nombre_base}")
async def extraer_foto(
    nombre_base: str,
    x1: float = Query(...), y1: float = Query(...),
    x2: float = Query(...), y2: float = Query(...)
):
    ruta_original = settings.DIR_SESION / f"{nombre_base}_original.png"
    if not ruta_original.exists():
        raise HTTPException(status_code=404, detail="Imagen original no encontrada")

    img = cv2.imread(str(ruta_original))
    if img is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar la imagen")
    alto, ancho = img.shape[:2]
    x1r, y1r, x2r, y2r = _porcentaje_a_pixeles(x1, y1, x2, y2, ancho, alto)
    if (x2r - x1r) < 50 or (y2r - y1r) < 50:
        raise HTTPException(status_code=400, detail="Área de extracción muy pequeña")

    nueva_base = f"{nombre_base}_extra_{int(time.time()*1000)}"
    ruta_nueva = settings.DIR_SESION / f"{nueva_base}_original.png"
    recorte = img[y1r:y2r, x1r:x2r]
    cv2.imwrite(str(ruta_nueva), recorte)
    try: os.chmod(str(ruta_nueva), 0o666)
    except Exception: pass

    print(f"🆕 Extracción: {nueva_base} ({recorte.shape[1]}x{recorte.shape[0]})")
    return {"nueva_base": nueva_base, "dimensiones": f"{recorte.shape[1]}x{recorte.shape[0]}"}

@router.post("/deshacer-edicion/{nombre_base}")
async def deshacer_edicion(nombre_base: str):
    rutas = [
        settings.DIR_SESION / f"{nombre_base}_original.png",
        settings.DIR_SESION / f"{nombre_base}_caras.png",
        settings.DIR_SESION / f"{nombre_base}_ia.png",
        settings.DIR_SESION / f"{nombre_base}_completa.png"
    ]
    restaurado = False
    for ruta in rutas:
        respaldo = ruta.with_suffix('.backup.png')
        if respaldo.exists():
            shutil.copy2(str(respaldo), str(ruta))
            try: os.chmod(str(ruta), 0o666)
            except Exception: pass
            restaurado = True
    
    if not restaurado:
        raise HTTPException(status_code=404, detail="No hay respaldos para restaurar")
    return {"mensaje": "Edición deshecha"}
