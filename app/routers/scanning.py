from fastapi import APIRouter, BackgroundTasks, HTTPException
import subprocess
import re
import time
from pathlib import Path

from app.state import app_state
from app.config import get_settings
from app.services.image_processor import ImageProcessor

router = APIRouter(prefix="/api", tags=["scanning"])

settings = get_settings()
image_processor = ImageProcessor()

def ejecutar_escaneo_real(dpi: int):
    """Tarea en background para escaneo real (Xerox Phaser 3100MFP)"""
    try:
        app_state.update_scan_progress(
            progreso=20,
            mensaje="Buscando Xerox Phaser 3100MFP..."
        )
        
        resultado = subprocess.run(
            ["sudo", "/usr/sbin/scanimage", "-L"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        match = re.search(settings.SCANNER_DEVICE_PATTERN, resultado.stdout)
        if not match:
            raise Exception("No se encontró el escáner.")
        
        dispositivo = match.group(1) if match.groups() else match.group(0)
        
        app_state.update_scan_progress(
            progreso=40,
            mensaje=f"Escaneando platina a {dpi} DPI..."
        )
        
        timestamp = int(time.time() * 1000)
        prefijo_base = f"foto_{timestamp}"
        
        carpeta_escaneos = Path.home() / "Escritorio" / "Escaneos"
        carpeta_escaneos.mkdir(parents=True, exist_ok=True)
        ruta_platina = carpeta_escaneos / f"platina_{timestamp}.png"
        
        comando = [
            "sudo", "/usr/sbin/scanimage",
            "-d", dispositivo,
            "--format=png",
            "--mode=Color",
            f"--resolution={dpi}"
        ]
        
        with open(ruta_platina, "wb") as f:
            subprocess.run(comando, stdout=f, timeout=300)
        
        try:
            import os
            os.chmod(str(ruta_platina), 0o666)
        except:
            pass
        
        if not ruta_platina.exists() or ruta_platina.stat().st_size == 0:
            raise Exception("Archivo vacío.")
        
        app_state.update_scan_progress(
            progreso=75,
            mensaje="Planchando perspectiva con OpenCV..."
        )
        
        fotos_recortadas = image_processor.procesar_platina(
            ruta_platina, prefijo_base, settings.DIR_SESION
        )
        
        if ruta_platina.exists():
            ruta_platina.unlink()
        
        if not fotos_recortadas:
            raise Exception("OpenCV falló.")
        
        app_state.update_scan_progress(
            progreso=100,
            mensaje=f"¡{len(fotos_recortadas)} foto(s)!",
            fotos_listas=fotos_recortadas,
            completado=True
        )
        
    except subprocess.TimeoutExpired:
        try:
            if ruta_platina.exists():
                ruta_platina.unlink()
        except Exception:
            pass
        app_state.update_scan_progress(
            error=True,
            mensaje="Error: el escáner no respondió (timeout). Revisá USB/tapa."
        )

    except Exception as e:
        app_state.update_scan_progress(
            error=True,
            mensaje=f"Error: {str(e)}"
        )

def ejecutar_escaneo_simulado(dpi: int):
    """Tarea en background para modo simulación"""
    try:
        time.sleep(0.5)
        
        app_state.update_scan_progress(
            progreso=40,
            mensaje="Leyendo simulador..."
        )
        
        timestamp = int(time.time() * 1000)
        prefijo_base = f"foto_{timestamp}_test"
        
        archivos_sim = [
            f for f in settings.DIR_SIMULADOR.iterdir()
            if f.is_file() and f.suffix.lower() in ('.png', '.jpg')
        ]
        
        if not archivos_sim:
            raise Exception("No hay imágenes en simulador/")
        
        ruta_prueba = settings.DIR_SIMULADOR / "prueba.png"
        if not ruta_prueba.exists():
            ruta_prueba = archivos_sim[0]
        
        app_state.update_scan_progress(
            progreso=75,
            mensaje="Planchando perspectiva con OpenCV..."
        )
        
        fotos_recortadas = image_processor.procesar_platina(
            ruta_prueba, prefijo_base, settings.DIR_SESION
        )
        
        if not fotos_recortadas:
            raise Exception("Archivo dañado.")
        
        app_state.update_scan_progress(
            progreso=100,
            mensaje=f"¡Test listo! {len(fotos_recortadas)} foto(s).",
            fotos_listas=fotos_recortadas,
            completado=True
        )
        
    except Exception as e:
        app_state.update_scan_progress(
            error=True,
            mensaje=f"Error: {str(e)}"
        )

@router.post("/escanear")
async def iniciar_escaneo(background_tasks: BackgroundTasks, dpi: int = 300):
    """Inicia escaneo real"""
    if not app_state.album_abierto:
        raise HTTPException(status_code=400, detail="Inicia lote primero.")
    
    app_state.update_scan_progress(
        progreso=10,
        mensaje=f"Iniciando a {dpi} DPI...",
        completado=False,
        error=False,
        fotos_listas=[]
    )
    
    background_tasks.add_task(ejecutar_escaneo_real, dpi)
    return {"mensaje": "Escaneo en curso"}

@router.post("/escanear-test")
async def iniciar_escaneo_test(background_tasks: BackgroundTasks, dpi: int = 300):
    """Inicia escaneo de prueba"""
    if not app_state.album_abierto:
        raise HTTPException(status_code=400, detail="Inicia lote primero.")
    
    app_state.update_scan_progress(
        progreso=10,
        mensaje=f"Simulando a {dpi} DPI...",
        completado=False,
        error=False,
        fotos_listas=[]
    )
    
    background_tasks.add_task(ejecutar_escaneo_simulado, dpi)
    return {"mensaje": "Modo test"}

@router.get("/estado-escaner")
async def obtener_estado_escaner():
    """Obtiene estado del escáner"""
    return app_state.scan_progress