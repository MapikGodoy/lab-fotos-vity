from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    DIR_SESION: Path = BASE_DIR / "sesion_activa"
    DIR_BKP_ORIGINAL: Path = BASE_DIR / "bkporiginal"
    DIR_IA: Path = BASE_DIR / "ia_engine"
    DIR_SIMULADOR: Path = BASE_DIR / "simulador"
    DIR_STATIC: Path = BASE_DIR / "static"
    
    HOST: str = "0.0.0.0"
    PORT: int = 7777
    
    NAS_USER: str = "mak"
    NAS_HOST: str = "192.168.1.80"
    NAS_PATH: str = "/srv/dev-disk-by-uuid-69fe1c68-291a-4766-8e61-bdc74f584e89/Fotos_escaneadas"
    NAS_PASS: str = ""
    
    SCANNER_DEVICE_PATTERN: str = r'(XeroxPhaser3100:usb:\d+:\d+)'
    DEFAULT_DPI: int = 300
    
    # Parámetros SEGUROS para RX 580 + RADV (evita cuelgues en 0.00%)
    VULKAN_MODEL: str = "realesrgan-x4plus"
    VULKAN_SCALE: int = 4
    VULKAN_TILE: int = 200        # Conservador, evita bloqueos de memoria
    VULKAN_THREADS: str = "1:1:1"  # Secuencial, máxima estabilidad
    VULKAN_TIMEOUT: int = 300      # Más tiempo por si la imagen es grande
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
