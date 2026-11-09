from pathlib import Path
import shutil
from typing import List

def limpiar_directorio(dir_path: Path, extensiones: List[str] = None):
    """
    Limpia un directorio de archivos
    
    Args:
        dir_path: Path del directorio
        extensiones: Lista de extensiones a eliminar (None = todas)
    """
    if not dir_path.exists():
        return
    
    for archivo in dir_path.iterdir():
        if archivo.is_file():
            if extensiones is None or archivo.suffix.lower() in extensiones:
                try:
                    archivo.unlink()
                except Exception as e:
                    print(f"Error eliminando {archivo}: {e}")

def asegurar_directorio(dir_path: Path, permisos: int = 0o755):
    """Crea un directorio si no existe"""
    dir_path.mkdir(parents=True, exist_ok=True)
    try:
        dir_path.chmod(permisos)
    except:
        pass

def obtener_archivos_simulador(dir_simulador: Path) -> List[Path]:
    """Obtiene archivos válidos del simulador"""
    if not dir_simulador.exists():
        return []
    
    extensiones_validas = {'.png', '.jpg', '.jpeg'}
    return [
        f for f in dir_simulador.iterdir()
        if f.is_file() and f.suffix.lower() in extensiones_validas
    ]