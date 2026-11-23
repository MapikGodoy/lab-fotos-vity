#!/usr/bin/env python3
"""
Genera 3 diagramas vectoriales SVG y los exporta a PNG (300 DPI) con Inkscape
para el Documento de Presentación Académica:
"Diseño e Integración del Ciclo de Vida de un Sistema con IA - Desktopia Lab 2.0"
"""
import subprocess
from pathlib import Path

DIR_SRC = Path(__file__).parent
DIR_SRC.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# 1. ARTICULACIÓN SISTÉMICA: SDLC <-> MLOps <-> DLM
# -------------------------------------------------------------------------
svg_articulacion = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 340" width="920" height="340">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#f1f5f9" />
    </linearGradient>
  </defs>
  <rect width="920" height="340" rx="14" fill="url(#bgGrad)" stroke="#cbd5e1" stroke-width="2" />

  <!-- Título Superior -->
  <text x="460" y="28" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a" text-anchor="middle">ARTICULACIÓN SISTÉMICA EN DESKTOPIA LAB 2.0 (CORE AI)</text>
  <text x="460" y="45" font-family="sans-serif" font-size="10.5" fill="#475569" text-anchor="middle">Intersección continua entre el Software Tradicional (SDLC), los Motores Inteligentes (MLOps) y la Gobernanza del Dato (DLM)</text>

  <!-- Encabezados de Columnas (Fases Integradas) -->
  <g transform="translate(175, 58)">
    <rect x="0" y="0" width="170" height="22" rx="4" fill="#0f172a" />
    <text x="85" y="15" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">1. INICIO Y CAPTURA</text>

    <rect x="180" y="0" width="170" height="22" rx="4" fill="#0f172a" />
    <text x="265" y="15" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">2. PROCESAMIENTO IA</text>

    <rect x="360" y="0" width="170" height="22" rx="4" fill="#0f172a" />
    <text x="445" y="15" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">3. CONTROL HUMANO</text>

    <rect x="540" y="0" width="175" height="22" rx="4" fill="#0f172a" />
    <text x="627" y="15" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">4. ARCHIVO Y MONITOREO</text>
  </g>

  <!-- FILA 1: SDLC (SISTEMA TRADICIONAL) -->
  <g transform="translate(20, 90)">
    <rect width="145" height="70" rx="8" fill="#1d4ed8" />
    <text x="72" y="28" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#ffffff" text-anchor="middle">CICLO SDLC</text>
    <text x="72" y="44" font-family="sans-serif" font-size="9.5" fill="#dbeafe" text-anchor="middle">Sistema Tradicional</text>
    <text x="72" y="58" font-family="sans-serif" font-size="8.5" fill="#93c5fd" text-anchor="middle">FastAPI + SPA + Manual</text>

    <!-- Celdas SDLC -->
    <rect x="155" y="0" width="170" height="70" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" />
    <text x="240" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Lanzador 1-Clic y Lote</text>
    <text x="240" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">UI Apertura de Álbum + QR</text>
    <text x="240" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Escáner SANE / Upload</text>

    <rect x="335" y="0" width="170" height="70" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" />
    <text x="420" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Orquestación Async API</text>
    <text x="420" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Routers /procesar-ia</text>
    <text x="420" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Locks GPU / Persistencia F5</text>

    <rect x="515" y="0" width="170" height="70" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" />
    <text x="600" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Mesa de Control Visual</text>
    <text x="600" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Slider + Lupa 2.2x + Atajos</text>
    <text x="600" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Recorte y Rotación 90°</text>

    <rect x="695" y="0" width="175" height="70" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" />
    <text x="782" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a" text-anchor="middle">Despliegue y Cierre</text>
    <text x="782" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Dashboard /estadisticas</text>
    <text x="782" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Botón Apagar Seguro</text>
  </g>

  <!-- FILA 2: MLOps (SISTEMA DE IA) -->
  <g transform="translate(20, 172)">
    <rect width="145" height="70" rx="8" fill="#7c3aed" />
    <text x="72" y="28" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#ffffff" text-anchor="middle">CICLO MLOps</text>
    <text x="72" y="44" font-family="sans-serif" font-size="9.5" fill="#ede9fe" text-anchor="middle">Módulos Inteligentes</text>
    <text x="72" y="58" font-family="sans-serif" font-size="8.5" fill="#ddd6fe" text-anchor="middle">OpenCV + Dual Engine</text>

    <!-- Celdas MLOps -->
    <rect x="155" y="0" width="170" height="70" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" />
    <text x="240" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#4c1d95" text-anchor="middle">Visión Clásica y Preproc.</text>
    <text x="240" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">OpenCV Contours + Warp</text>
    <text x="240" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Normalización MAX_DIM 1800</text>

    <rect x="335" y="0" width="170" height="70" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" />
    <text x="420" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#4c1d95" text-anchor="middle">Inferencia Paralela IA</text>
    <text x="420" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Auto-giro Landmarks Ojos</text>
    <text x="420" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">GFPGAN + Vulkan 4x + Fusión</text>

    <rect x="515" y="0" width="170" height="70" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" />
    <text x="600" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#4c1d95" text-anchor="middle">Human-in-the-Loop (HITL)</text>
    <text x="600" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Mitigación Falsos Positivos</text>
    <text x="600" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Elección: Total/4x/Caras/Orig</text>

    <rect x="695" y="0" width="175" height="70" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5" />
    <text x="782" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#4c1d95" text-anchor="middle">Monitoreo y Drift</text>
    <text x="782" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">KPIs Aceptación por Modelo</text>
    <text x="782" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Model Swap vía .env</text>
  </g>

  <!-- FILA 3: DLM (GESTIÓN DEL DATO) -->
  <g transform="translate(20, 254)">
    <rect width="145" height="70" rx="8" fill="#059669" />
    <text x="72" y="28" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="#ffffff" text-anchor="middle">CICLO DLM</text>
    <text x="72" y="44" font-family="sans-serif" font-size="9.5" fill="#d1fae5" text-anchor="middle">Ciclo de Vida del Dato</text>
    <text x="72" y="58" font-family="sans-serif" font-size="8.5" fill="#a7f3d0" text-anchor="middle">EDA + EXIF + PII Local</text>

    <!-- Celdas DLM -->
    <rect x="155" y="0" width="170" height="70" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" />
    <text x="240" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#065f46" text-anchor="middle">Captura y Metadatos</text>
    <text x="240" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">PNG 300 DPI / JPG EXIF</text>
    <text x="240" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Operador + Álbum + Año</text>

    <rect x="335" y="0" width="170" height="70" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" />
    <text x="420" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#065f46" text-anchor="middle">Almacenam. Efímero</text>
    <text x="420" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Carpeta sesion_activa/ LAN</text>
    <text x="420" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Purga inmediata de platina</text>

    <rect x="515" y="0" width="170" height="70" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" />
    <text x="600" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#065f46" text-anchor="middle">Enriquecimiento EXIF</text>
    <text x="600" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">exiftool: Año Histórico</text>
    <text x="600" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Transparencia Software IA</text>

    <rect x="695" y="0" width="175" height="70" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" />
    <text x="782" y="20" font-family="sans-serif" font-size="10" font-weight="bold" fill="#065f46" text-anchor="middle">Archivado NAS y Purga</text>
    <text x="782" y="36" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">rsync SSH a Fotos_escaneadas</text>
    <text x="782" y="51" font-family="sans-serif" font-size="9" fill="#334155" text-anchor="middle">Destrucción copias locales</text>
  </g>
</svg>'''

# -------------------------------------------------------------------------
# 2. PIPELINE MLOPS: MONITOREO, HITL Y CONTROL DE DRIFT
# -------------------------------------------------------------------------
svg_mlops_drift = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 270" width="920" height="270">
  <rect width="920" height="270" rx="14" fill="#0f172a" stroke="#334155" stroke-width="2" />
  <text x="460" y="28" font-family="sans-serif" font-size="13.5" font-weight="bold" fill="#f8fafc" text-anchor="middle">ARQUITECTURA MLOPS: DESPLIEGUE SEGURO, EVALUACIÓN HITL Y DETECCIÓN DE DRIFT</text>

  <!-- Bloque 1: Pre-procesamiento & Guards -->
  <g transform="translate(22, 48)">
    <rect width="195" height="145" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8" />
    <rect x="12" y="10" width="171" height="22" rx="4" fill="#0284c7" />
    <text x="97" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">1. GUARDAS DE ENTRADA</text>
    <text x="15" y="52" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• EXIF Transpose (JPG móvil)</text>
    <text x="15" y="70" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Resize LANCZOS MAX 1800px</text>
    <text x="15" y="88" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Auto-orientación Landmarks</text>
    <text x="15" y="106" font-family="sans-serif" font-size="9.5" fill="#7dd3fc">• Si caras == 0 (Paisaje):</text>
    <text x="22" y="120" font-family="sans-serif" font-size="9" fill="#bae6fd">Inhibe rotación automática</text>
    <text x="15" y="136" font-family="sans-serif" font-size="8.5" fill="#94a3b8">Mitiga Data Drift de fuentes</text>
  </g>

  <path d="M 222 120 L 244 120" stroke="#38bdf8" stroke-width="2.5" fill="none" />
  <polygon points="244,115 252,120 244,125" fill="#38bdf8" />

  <!-- Bloque 2: Serving Paralelo + Fallbacks -->
  <g transform="translate(254, 48)">
    <rect width="205" height="145" rx="10" fill="#1e293b" stroke="#a855f7" stroke-width="1.8" />
    <rect x="12" y="10" width="181" height="22" rx="4" fill="#7c3aed" />
    <text x="102" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">2. SERVING ASÍNCRONO</text>
    <text x="15" y="52" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• GPU Lock RX 580 (tile=200)</text>
    <text x="15" y="70" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• CPU Lock GFPGAN v1.4</text>
    <text x="15" y="88" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Fusión Total (Caras + 4x)</text>
    <text x="15" y="106" font-family="sans-serif" font-size="9.5" fill="#d8b4fe">• Fallback determinístico:</text>
    <text x="22" y="120" font-family="sans-serif" font-size="9" fill="#e9d5ff">Copia segura a 4x si falla</text>
    <text x="15" y="136" font-family="sans-serif" font-size="8.5" fill="#94a3b8">Timeout 300s + Botón Reintentar</text>
  </g>

  <path d="M 464 120 L 486 120" stroke="#a855f7" stroke-width="2.5" fill="none" />
  <polygon points="486,115 494,120 486,125" fill="#a855f7" />

  <!-- Bloque 3: Validación Humana (HITL) -->
  <g transform="translate(496, 48)">
    <rect width="195" height="145" rx="10" fill="#1e293b" stroke="#10b981" stroke-width="1.8" />
    <rect x="12" y="10" width="171" height="22" rx="4" fill="#059669" />
    <text x="97" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">3. FILTRO HUMANO (HITL)</text>
    <text x="15" y="52" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Visor Slider Comparativo</text>
    <text x="15" y="70" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Lupa 2.2x de detalle facial</text>
    <text x="15" y="88" font-family="sans-serif" font-size="9.5" fill="#6ee7b7">• Aprobación selectiva:</text>
    <text x="22" y="103" font-family="monospace" font-size="9" fill="#a7f3d0">[A] Total   [I] Solo 4x</text>
    <text x="22" y="117" font-family="monospace" font-size="9" fill="#a7f3d0">[C] Caras   [0] Original</text>
    <text x="15" y="136" font-family="sans-serif" font-size="8.5" fill="#94a3b8">Bloquea falsos positivos IA</text>
  </g>

  <path d="M 696 120 L 718 120" stroke="#10b981" stroke-width="2.5" fill="none" />
  <polygon points="718,115 726,120 718,125" fill="#10b981" />

  <!-- Bloque 4: Telemetría y Monitoreo -->
  <g transform="translate(728, 48)">
    <rect width="170" height="145" rx="10" fill="#1e293b" stroke="#f59e0b" stroke-width="1.8" />
    <rect x="10" y="10" width="150" height="22" rx="4" fill="#d97706" />
    <text x="85" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">4. MONITOREO Y DRIFT</text>
    <text x="12" y="52" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• Log: desktopia.log</text>
    <text x="12" y="70" font-family="sans-serif" font-size="9.5" fill="#e2e8f0">• KPIs: /api/estadisticas</text>
    <text x="12" y="88" font-family="sans-serif" font-size="9.5" fill="#fcd34d">• Alerta de Drift:</text>
    <text x="16" y="103" font-family="sans-serif" font-size="8.8" fill="#fde68a">Si baja % Completa o</text>
    <text x="16" y="116" font-family="sans-serif" font-size="8.8" fill="#fde68a">sube % Original/Descarte</text>
    <text x="12" y="136" font-family="sans-serif" font-size="8.5" fill="#94a3b8">Swap modelo vía .env</text>
  </g>

  <!-- Bucle de Retroalimentación (Feedback Loop) abajo -->
  <path d="M 813 195 L 813 226 L 119 226 L 119 200" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6,4" fill="none" />
  <polygon points="114,202 119,193 124,202" fill="#f59e0b" />
  <rect x="150" y="213" width="620" height="24" rx="12" fill="#78350f" stroke="#f59e0b" stroke-width="1.2" />
  <text x="460" y="229" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#fef3c7" text-anchor="middle">LAZO DE MEJORA CONTINUA: Ajuste de VULKAN_MODEL / Umbrales OpenCV / Pesos GFPGAN según KPIs reales</text>
</svg>'''

# -------------------------------------------------------------------------
# 3. CICLO DE VIDA DEL DATO (DLM) + EDA + GOBERNANZA PII
# -------------------------------------------------------------------------
svg_dlm_eda = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 250" width="920" height="250">
  <rect width="920" height="250" rx="14" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2" />
  <text x="460" y="26" font-family="sans-serif" font-size="13.5" font-weight="bold" fill="#0f172a" text-anchor="middle">CICLO DE VIDA DEL DATO (DLM): TRAZABILIDAD, ANÁLISIS EDA Y DESTRUCCIÓN SEGURA</text>

  <!-- 5 Cajas Secuenciales -->
  <g transform="translate(20, 48)">
    <!-- 1. Captura -->
    <rect width="160" height="122" rx="8" fill="#ffffff" stroke="#0284c7" stroke-width="2" />
    <rect width="160" height="24" rx="8" fill="#0284c7" />
    <text x="80" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">1. CAPTURA</text>
    <text x="80" y="42" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">Origen Multicanal</text>
    <text x="80" y="58" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Escáner SANE 300 DPI</text>
    <text x="80" y="72" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Upload JPG/PNG móvil</text>
    <text x="80" y="86" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Simulador capacitación</text>
    <text x="80" y="108" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#0369a1" text-anchor="middle">+ Contexto (Operador/Año)</text>
  </g>

  <path d="M 184 109 L 198 109" stroke="#64748b" stroke-width="2" />
  <polygon points="196,105 203,109 196,113" fill="#64748b" />

  <g transform="translate(205, 48)">
    <!-- 2. Procesamiento & EDA -->
    <rect width="160" height="122" rx="8" fill="#ffffff" stroke="#7c3aed" stroke-width="2" />
    <rect width="160" height="24" rx="8" fill="#7c3aed" />
    <text x="80" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">2. LIMPIEZA Y EDA</text>
    <text x="80" y="42" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">Normalización Activa</text>
    <text x="80" y="58" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Umbral OpenCV &gt;100k px²</text>
    <text x="80" y="72" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Limpieza borde 10px tapa</text>
    <text x="80" y="86" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Outliers: MAX_DIM 1800px</text>
    <text x="80" y="108" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#6d28d9" text-anchor="middle">Copias temporales en RAM/disco</text>
  </g>

  <path d="M 369 109 L 383 109" stroke="#64748b" stroke-width="2" />
  <polygon points="381,105 388,109 381,113" fill="#64748b" />

  <g transform="translate(390, 48)">
    <!-- 3. Uso & Enriquecimiento -->
    <rect width="160" height="122" rx="8" fill="#ffffff" stroke="#0d9488" stroke-width="2" />
    <rect width="160" height="24" rx="8" fill="#0d9488" />
    <text x="80" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">3. USO Y EXIF</text>
    <text x="80" y="42" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">Sesión y Trazabilidad</text>
    <text x="80" y="58" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Estado en sesion_activa/</text>
    <text x="80" y="72" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• DateTimeOriginal = Año</text>
    <text x="80" y="86" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Software = Motor IA usado</text>
    <text x="80" y="108" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#0f766e" text-anchor="middle">Inyectado con exiftool</text>
  </g>

  <path d="M 554 109 L 568 109" stroke="#64748b" stroke-width="2" />
  <polygon points="566,105 573,109 566,113" fill="#64748b" />

  <g transform="translate(575, 48)">
    <!-- 4. Archivado -->
    <rect width="160" height="122" rx="8" fill="#ffffff" stroke="#059669" stroke-width="2" />
    <rect width="160" height="24" rx="8" fill="#059669" />
    <text x="80" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">4. ARCHIVADO NAS</text>
    <text x="80" y="42" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#0f172a" text-anchor="middle">Almacenamiento Seguro</text>
    <text x="80" y="58" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Túnel cifrado SSH + rsync</text>
    <text x="80" y="72" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• IP Privada 192.168.1.80</text>
    <text x="80" y="86" font-family="sans-serif" font-size="8.8" fill="#334155" text-anchor="middle">• Carpeta: [Album]_[Año]/</text>
    <text x="80" y="108" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#047857" text-anchor="middle">100% On-Premise (Sin Nube)</text>
  </g>

  <path d="M 739 109 L 753 109" stroke="#64748b" stroke-width="2" />
  <polygon points="751,105 758,109 751,113" fill="#64748b" />

  <g transform="translate(760, 48)">
    <!-- 5. Destrucción Segura -->
    <rect width="140" height="122" rx="8" fill="#fff1f2" stroke="#e11d48" stroke-width="2" />
    <rect width="140" height="24" rx="8" fill="#e11d48" />
    <text x="70" y="16" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">5. PURGA SEGURA</text>
    <text x="70" y="42" font-family="sans-serif" font-size="9.5" font-weight="bold" fill="#881337" text-anchor="middle">Higiene de Datos Local</text>
    <text x="70" y="58" font-family="sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">• Borra platina y .temp</text>
    <text x="70" y="72" font-family="sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">• Purga variantes desc.</text>
    <text x="70" y="86" font-family="sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">• Limpia sesión al cerrar</text>
    <text x="70" y="108" font-family="sans-serif" font-size="8.5" font-weight="bold" fill="#be123c" text-anchor="middle">Minimización PII en PC</text>
  </g>

  <!-- Banda inferior de Gobernanza -->
  <rect x="20" y="186" width="880" height="48" rx="8" fill="#0f172a" />
  <text x="460" y="206" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="#34d399" text-anchor="middle">GOBERNANZA, PRIVACIDAD POR DISEÑO (LEY 25.326) Y ÉTICA ALGORÍTMICA</text>
  <text x="460" y="224" font-family="sans-serif" font-size="9.3" fill="#cbd5e1" text-anchor="middle">Ningún rostro biométrico sale a APIs externas • Secretos NAS protegidos en .env • Transparencia en EXIF sobre intervención de IA</text>
</svg>'''

diagrams = {
    "diagrama_ciclos_articulacion": svg_articulacion,
    "diagrama_mlops_drift": svg_mlops_drift,
    "diagrama_dlm_eda": svg_dlm_eda,
}

for name, content in diagrams.items():
    svg_path = DIR_SRC / f"{name}.svg"
    png_path = DIR_SRC / f"{name}.png"
    svg_path.write_text(content, encoding="utf-8")
    subprocess.run([
        "inkscape", str(svg_path),
        "--export-type=png",
        "--export-dpi=300",
        f"--export-filename={png_path}"
    ], check=True)
    print(f"✅ Generado {png_path.name}")
