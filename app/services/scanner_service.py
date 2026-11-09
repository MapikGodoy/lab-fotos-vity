import subprocess
import re
from pathlib import Path
from typing import Optional, Tuple

class ScannerService:
    """Servicio para manejar el escáner Xerox"""
    
    def __init__(self, device_pattern: str = r'XeroxPhaser3100:usb:\d+:\d+'):
        self.device_pattern = device_pattern
    
    def detectar_escaner(self) -> Optional[str]:
        """Detecta y retorna el dispositivo del escáner"""
        try:
            resultado = subprocess.run(
                ["sudo", "/usr/sbin/scanimage", "-L"],
                capture_output=True,
                text=True
            )
            
            match = re.search(self.device_pattern, resultado.stdout)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            print(f"Error detectando escáner: {e}")
            return None
    
    def escanear_platina(self, dispositivo: str, dpi: int, ruta_salida: Path) -> bool:
        """Ejecuta el escaneo de la platina"""
        try:
            comando = [
                "sudo", "/usr/sbin/scanimage",
                "-d", dispositivo,
                "--format=png",
                "--mode=Color",
                f"--resolution={dpi}"
            ]
            
            with open(ruta_salida, "wb") as f:
                subprocess.run(comando, stdout=f, check=True)
            
            return ruta_salida.exists() and ruta_salida.stat().st_size > 0
        except Exception as e:
            print(f"Error escaneando: {e}")
            return False
