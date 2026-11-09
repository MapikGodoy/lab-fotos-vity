from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import threading
import json
from app.config import get_settings

class AppState:
    """Estado global thread-safe con persistencia en disco ante F5 o reinicio."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self._album_abierto = False
        self._lote_actual: Optional[Dict] = None
        self._fotos_aprobadas: List[str] = []
        self._scan_progress: Dict = {
            "progreso": 0,
            "mensaje": "Inactivo",
            "completado": False,
            "error": False,
            "fotos_listas": []
        }
        self._restaurar_de_disco()

    def _restaurar_de_disco(self):
        """Recupera el lote y las fotos aprobadas desde sesion_activa si existen."""
        try:
            settings = get_settings()
            if not settings.DIR_SESION.exists():
                return
            
            meta_file = settings.DIR_SESION / "session_meta.json"
            aprob_file = settings.DIR_SESION / "aprobadas.json"

            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        self._lote_actual = json.load(f)
                        self._album_abierto = True
                except Exception as e:
                    print(f"Error leyendo session_meta.json: {e}")
            else:
                # Si hay fotos en la carpeta pero no había meta_file
                hay_fotos = any(
                    f.name.endswith("_original.png") or f.name.endswith(".png")
                    for f in settings.DIR_SESION.iterdir()
                    if f.is_file() and not f.name.startswith(".")
                )
                if hay_fotos:
                    self._lote_actual = {
                        "operador": "Mak",
                        "nombre_lote": "Lote_Activo",
                        "fecha_historica": "Historico",
                        "creado_en": str(datetime.now())
                    }
                    self._album_abierto = True

            if aprob_file.exists():
                try:
                    with open(aprob_file, "r", encoding="utf-8") as f:
                        self._fotos_aprobadas = json.load(f)
                except Exception as e:
                    print(f"Error leyendo aprobadas.json: {e}")
        except Exception as e:
            print(f"Aviso al restaurar estado de sesión: {e}")

    def _guardar_meta_disco(self):
        try:
            settings = get_settings()
            settings.DIR_SESION.mkdir(parents=True, exist_ok=True)
            meta_file = settings.DIR_SESION / "session_meta.json"
            if self._lote_actual:
                with open(meta_file, "w", encoding="utf-8") as f:
                    json.dump(self._lote_actual, f, ensure_ascii=False, indent=2)
            elif meta_file.exists():
                meta_file.unlink()
        except Exception as e:
            print(f"Error guardando session_meta.json: {e}")

    def _guardar_aprobadas_disco(self):
        try:
            settings = get_settings()
            settings.DIR_SESION.mkdir(parents=True, exist_ok=True)
            aprob_file = settings.DIR_SESION / "aprobadas.json"
            with open(aprob_file, "w", encoding="utf-8") as f:
                json.dump(self._fotos_aprobadas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando aprobadas.json: {e}")
    
    def iniciar_lote(self, operador: str, nombre: str, fecha: str, dir_sesion: Path):
        """Inicia un nuevo lote y limpia la sesión anterior."""
        with self._lock:
            if dir_sesion.exists():
                for f in dir_sesion.iterdir():
                    if f.is_file():
                        try:
                            f.unlink()
                        except Exception as e:
                            print(f"Error eliminando {f}: {e}")
            
            self._album_abierto = True
            self._lote_actual = {
                "operador": operador.strip(),
                "nombre_lote": nombre.strip().replace(" ", "_"),
                "fecha_historica": fecha.strip(),
                "creado_en": str(datetime.now())
            }
            self._fotos_aprobadas = []
            self._guardar_meta_disco()
            self._guardar_aprobadas_disco()
    
    def cerrar_lote(self):
        """Cierra el lote actual y limpia la persistencia."""
        with self._lock:
            self._album_abierto = False
            lote_cerrado = self._lote_actual
            self._lote_actual = None
            self._fotos_aprobadas = []
            self._guardar_meta_disco()
            self._guardar_aprobadas_disco()
            return lote_cerrado
    
    def cancelar_lote(self, dir_sesion: Path):
        """Cancela el lote y limpia archivos y persistencia."""
        with self._lock:
            if dir_sesion.exists():
                for f in dir_sesion.iterdir():
                    if f.is_file():
                        try:
                            f.unlink()
                        except:
                            pass
            
            self._album_abierto = False
            self._lote_actual = None
            self._fotos_aprobadas = []
            self._guardar_meta_disco()
            self._guardar_aprobadas_disco()
    
    def agregar_foto_aprobada(self, nombre_foto: str):
        """Agrega foto a aprobadas persistiendo en disco."""
        with self._lock:
            if nombre_foto not in self._fotos_aprobadas:
                self._fotos_aprobadas.append(nombre_foto)
                self._guardar_aprobadas_disco()
    
    def remover_foto_aprobada(self, nombre_foto: str):
        """Remueve foto de aprobadas persistiendo en disco."""
        with self._lock:
            if nombre_foto in self._fotos_aprobadas:
                self._fotos_aprobadas.remove(nombre_foto)
                self._guardar_aprobadas_disco()
    
    def update_scan_progress(self, **kwargs):
        """Actualiza progreso del escaneo."""
        with self._lock:
            for key, value in kwargs.items():
                if key in self._scan_progress:
                    self._scan_progress[key] = value
    
    @property
    def album_abierto(self) -> bool:
        with self._lock:
            return self._album_abierto
    
    @property
    def lote_actual(self) -> Optional[Dict]:
        with self._lock:
            return self._lote_actual.copy() if self._lote_actual else None
    
    @property
    def fotos_aprobadas(self) -> List[str]:
        with self._lock:
            return self._fotos_aprobadas.copy()
    
    @property
    def scan_progress(self) -> Dict:
        with self._lock:
            return self._scan_progress.copy()

# Singleton
app_state = AppState()
