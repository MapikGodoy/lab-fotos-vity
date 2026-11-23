import os
import signal
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pathlib import Path
import uvicorn

from app.config import get_settings
from app.state import app_state
from app.routers import scanning, processing, photos, sessions

settings = get_settings()

app = FastAPI(title="Desktopia Lab - Motor de Digitalización")

# Montar routers
app.include_router(scanning.router)
app.include_router(processing.router)
app.include_router(photos.router)
app.include_router(sessions.router)

# Montar estáticos
app.mount("/static", StaticFiles(directory=str(settings.DIR_STATIC)), name="static")

# Asegurar directorio de sesión y respaldo local de originales
settings.DIR_SESION.mkdir(parents=True, exist_ok=True)
settings.DIR_BKP_ORIGINAL.mkdir(parents=True, exist_ok=True)
try:
    os.chmod(str(settings.DIR_SESION), 0o777)
    os.chmod(str(settings.DIR_BKP_ORIGINAL), 0o777)
except:
    pass

@app.get("/")
async def root():
    """Sirve la interfaz web con encabezados no-cache para garantizar siempre la versión más reciente."""
    ruta_index = settings.DIR_STATIC / "index.html"
    return HTMLResponse(
        content=ruta_index.read_text(encoding="utf-8"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.post("/api/apagar-servidor")
async def apagar_servidor(limpiar_sesion: bool = False):
    """
    Detiene de forma limpia el servidor y todos los subprocesos de Desktopia Lab.
    Permite liberar los puertos y la memoria de la GPU/CPU al terminar la jornada.
    """
    if limpiar_sesion:
        try:
            app_state.cancelar_lote(settings.DIR_SESION)
        except Exception as e:
            print(f"Aviso limpiando sesión al apagar: {e}")

    async def _apagar():
        await asyncio.sleep(0.5)
        print("🛑 Apagando servidor Desktopia Lab por orden del usuario...")
        try:
            # Terminar el grupo completo de procesos (incluye reloader si existe)
            os.killpg(os.getpgrp(), signal.SIGTERM)
        except Exception:
            try:
                os.kill(os.getppid(), signal.SIGTERM)
            except Exception:
                pass
            os.kill(os.getpid(), signal.SIGTERM)

    asyncio.create_task(_apagar())
    return {
        "status": "ok",
        "mensaje": "Servidor apagado exitosamente. Podés cerrar la pestaña del navegador."
    }

@app.get("/api/ver-foto/{nombre_archivo}")
async def ver_foto(nombre_archivo: str):
    """Sirve una foto desde la sesión activa con fallback automático para evitar imágenes rotas."""
    ruta = settings.DIR_SESION / nombre_archivo
    if ruta.exists() and ruta.is_file() and ruta.stat().st_size > 1000:
        return FileResponse(
            ruta,
            media_type="image/png",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )

    # Si el archivo existe pero está vacío o corrupto (<=1000 bytes), lo limpiamos
    if ruta.exists() and ruta.is_file() and ruta.stat().st_size <= 1000:
        try: ruta.unlink()
        except Exception: pass

    # Fallback inteligente para variantes que puedan estar finalizando procesamiento
    if nombre_archivo.endswith("_completa.png"):
        base = nombre_archivo[:-len("_completa.png")]
        fallback_ia = settings.DIR_SESION / f"{base}_ia.png"
        if fallback_ia.exists() and fallback_ia.is_file() and fallback_ia.stat().st_size > 1000:
            return FileResponse(fallback_ia, media_type="image/png", headers={"Cache-Control": "no-cache"})
        fallback_orig = settings.DIR_SESION / f"{base}_original.png"
        if fallback_orig.exists() and fallback_orig.is_file() and fallback_orig.stat().st_size > 1000:
            return FileResponse(fallback_orig, media_type="image/png", headers={"Cache-Control": "no-cache"})

    if nombre_archivo.endswith("_caras.png") or nombre_archivo.endswith("_ia.png"):
        suf = "_caras.png" if nombre_archivo.endswith("_caras.png") else "_ia.png"
        base = nombre_archivo[:-len(suf)]
        fallback_orig = settings.DIR_SESION / f"{base}_original.png"
        if fallback_orig.exists() and fallback_orig.is_file() and fallback_orig.stat().st_size > 1000:
            return FileResponse(fallback_orig, media_type="image/png", headers={"Cache-Control": "no-cache"})

    return HTMLResponse("Imagen no encontrada", status_code=404)

@app.get("/api/health")
async def health_check():
    """Endpoint de salud con no-cache"""
    return JSONResponse(
        content={
            "status": "ok",
            "album_abierto": app_state.album_abierto,
            "lote_actual": app_state.lote_actual
        },
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)