from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class ScanProgress(BaseModel):
    """Progreso del escaneo"""
    progreso: int = Field(0, ge=0, le=100)
    mensaje: str = "Inactivo"
    completado: bool = False
    error: bool = False
    fotos_listas: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)

class LoteInfo(BaseModel):
    """Información de un lote/álbum"""
    operador: str = Field(..., min_length=1)
    nombre_lote: str = Field(..., min_length=1)
    fecha_historica: str = Field(..., min_length=4)
    creado_en: datetime = Field(default_factory=datetime.now)

class FotoProcesada(BaseModel):
    """Información de una foto procesada"""
    base_name: str
    original_path: str
    ia_path: Optional[str] = None
    aprobada: bool = False
    descartada: bool = False

class ScanRequest(BaseModel):
    """Request para escaneo"""
    dpi: int = Field(300, ge=150, le=1200)
    modo_test: bool = False

class RegistrarOperadorRequest(BaseModel):
    """Request para registrar operador"""
    operador: str
    album: str
    fotos: int
    fecha_carga: datetime = Field(default_factory=datetime.now)