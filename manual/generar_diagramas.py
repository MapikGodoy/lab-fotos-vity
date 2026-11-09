import os
from pathlib import Path
import subprocess

DIR_MANUAL = Path("/home/mapik/lab-fotos-vity/manual")
DIR_MANUAL.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. DIAGRAMA DE FLUJO GENERAL (Paso a paso)
# -------------------------------------------------------------
svg_flujo = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 160" width="960" height="160">
  <defs>
    <linearGradient id="grad-1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#1d4ed8"/></linearGradient>
    <linearGradient id="grad-2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0ea5e9"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="grad-3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#4338ca"/></linearGradient>
    <linearGradient id="grad-4" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#6d28d9"/></linearGradient>
    <linearGradient id="grad-5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ec4899"/><stop offset="100%" stop-color="#be185d"/></linearGradient>
    <linearGradient id="grad-6" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#047857"/></linearGradient>
  </defs>

  <rect width="960" height="160" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" />

  <!-- Paso 1 -->
  <g transform="translate(15, 20)">
    <rect width="135" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-1)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">1</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Iniciar App</text>
    <text x="12" y="58" font-family="sans-serif" font-size="11" fill="#475569">1 clic en acceso directo</text>
    <text x="12" y="74" font-family="sans-serif" font-size="11" fill="#475569">o ejecutar script</text>
    <rect x="10" y="88" width="115" height="22" rx="5" fill="#dbeafe" />
    <text x="67" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1e40af" text-anchor="middle">Abre Navegador</text>
  </g>

  <!-- Flecha 1-2 -->
  <path d="M 155 80 L 170 80" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <polygon points="170,76 177,80 170,84" fill="#94a3b8" />

  <!-- Paso 2 -->
  <g transform="translate(180, 20)">
    <rect width="135" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-2)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">2</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Crear Lote</text>
    <text x="12" y="58" font-family="sans-serif" font-size="11" fill="#475569">• Nombre Operador</text>
    <text x="12" y="74" font-family="sans-serif" font-size="11" fill="#475569">• Nombre del Álbum</text>
    <rect x="10" y="88" width="115" height="22" rx="5" fill="#e0f2fe" />
    <text x="67" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">Año Histórico (EXIF)</text>
  </g>

  <!-- Flecha 2-3 -->
  <path d="M 320 80 L 335 80" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <polygon points="335,76 342,80 335,84" fill="#94a3b8" />

  <!-- Paso 3 -->
  <g transform="translate(345, 20)">
    <rect width="135" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-3)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">3</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#0f172a">Escanear</text>
    <text x="12" y="58" font-family="sans-serif" font-size="11" fill="#475569">1 o más fotos en vidrio</text>
    <text x="12" y="74" font-family="sans-serif" font-size="11" fill="#475569">o Importar foto móvil</text>
    <rect x="10" y="88" width="115" height="22" rx="5" fill="#ede9fe" />
    <text x="67" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#5b21b6" text-anchor="middle">Auto-corte OpenCV</text>
  </g>

  <!-- Flecha 3-4 -->
  <path d="M 485 80 L 500 80" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <polygon points="500,76 507,80 500,84" fill="#94a3b8" />

  <!-- Paso 4 -->
  <g transform="translate(510, 20)">
    <rect width="135" height="120" rx="10" fill="#faf5ff" stroke="#c084fc" stroke-width="1.5" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-4)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">4</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#581c87">Motor IA</text>
    <text x="12" y="58" font-family="sans-serif" font-size="11" fill="#475569">• GPU: Real-ESRGAN</text>
    <text x="12" y="74" font-family="sans-serif" font-size="11" fill="#475569">• CPU: GFPGAN caras</text>
    <rect x="10" y="88" width="115" height="22" rx="5" fill="#f3e8ff" />
    <text x="67" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#7e22ce" text-anchor="middle">Genera 3 Variantes</text>
  </g>

  <!-- Flecha 4-5 -->
  <path d="M 650 80 L 665 80" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <polygon points="665,76 672,80 665,84" fill="#94a3b8" />

  <!-- Paso 5 -->
  <g transform="translate(675, 20)">
    <rect width="135" height="120" rx="10" fill="#fff1f2" stroke="#fda4af" stroke-width="1.5" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-5)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">5</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#9f1239">Revisar</text>
    <text x="12" y="58" font-family="sans-serif" font-size="11" fill="#475569">Comparador slider</text>
    <text x="12" y="74" font-family="sans-serif" font-size="11" fill="#475569">Lupa 2x, rotar y corte</text>
    <rect x="10" y="88" width="115" height="22" rx="5" fill="#ffe4e6" />
    <text x="67" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#be123c" text-anchor="middle">Aprobar [A, I, C, O]</text>
  </g>

  <!-- Flecha 5-6 -->
  <path d="M 815 80 L 830 80" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" fill="none" />
  <polygon points="830,76 837,80 830,84" fill="#94a3b8" />

  <!-- Paso 6 -->
  <g transform="translate(840, 20)">
    <rect width="105" height="120" rx="10" fill="#ecfdf5" stroke="#10b981" stroke-width="2" />
    <circle cx="24" cy="24" r="14" fill="url(#grad-6)" />
    <text x="24" y="29" font-family="sans-serif" font-size="13" font-weight="900" fill="#ffffff" text-anchor="middle">6</text>
    <text x="46" y="29" font-family="sans-serif" font-size="14" font-weight="bold" fill="#065f46">Al NAS</text>
    <text x="10" y="58" font-family="sans-serif" font-size="10" fill="#047857">• Inyección EXIF</text>
    <text x="10" y="74" font-family="sans-serif" font-size="10" fill="#047857">• rsync a disco</text>
    <rect x="8" y="88" width="89" height="22" rx="5" fill="#10b981" />
    <text x="52" y="103" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">¡Cerrar Lote!</text>
  </g>
</svg>'''

# -------------------------------------------------------------
# 2. DIAGRAMA DEL MOTOR IA (Cómo interactúan las 2 IAs)
# -------------------------------------------------------------
svg_ia = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 270" width="880" height="270">
  <defs>
    <linearGradient id="grad-gpu-box" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#3730a3"/></linearGradient>
    <linearGradient id="grad-cpu-box" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0284c7"/><stop offset="100%" stop-color="#0369a1"/></linearGradient>
    <linearGradient id="grad-fusion-box" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#047857"/></linearGradient>
  </defs>

  <rect width="880" height="270" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" />

  <!-- Entrada: Foto Original -->
  <g transform="translate(20, 65)">
    <rect width="170" height="140" rx="10" fill="#f8fafc" stroke="#64748b" stroke-width="2" />
    <rect x="15" y="12" width="140" height="22" rx="6" fill="#e2e8f0" />
    <text x="85" y="27" font-family="sans-serif" font-size="11" font-weight="bold" fill="#475569" text-anchor="middle">ENTRADA DIGITAL</text>
    <text x="85" y="65" font-family="sans-serif" font-size="16" font-weight="bold" fill="#0f172a" text-anchor="middle">Foto Original</text>
    <text x="85" y="90" font-family="sans-serif" font-size="11" fill="#64748b" text-anchor="middle">Escáner o Celular</text>
    <text x="85" y="110" font-family="monospace" font-size="11" font-weight="bold" fill="#0284c7" text-anchor="middle">{base}_original.png</text>
    <text x="85" y="128" font-family="sans-serif" font-size="10" fill="#94a3b8" text-anchor="middle">Resolución Nativa 1x</text>
  </g>

  <!-- Conectores desde entrada -->
  <path d="M 190 100 L 235 100 L 235 55 L 260 55" stroke="#94a3b8" stroke-width="2.5" fill="none" stroke-dasharray="4,4" />
  <polygon points="260,51 267,55 260,59" fill="#94a3b8" />

  <path d="M 190 170 L 235 170 L 235 210 L 260 210" stroke="#94a3b8" stroke-width="2.5" fill="none" stroke-dasharray="4,4" />
  <polygon points="260,206 267,210 260,214" fill="#94a3b8" />

  <!-- Rama 1: GFPGAN (CPU) -->
  <g transform="translate(267, 15)">
    <rect width="280" height="95" rx="10" fill="#f0f9ff" stroke="#0284c7" stroke-width="2" />
    <rect x="175" y="12" width="92" height="22" rx="11" fill="url(#grad-cpu-box)" />
    <text x="221" y="27" font-family="monospace" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">CPU i5/i7</text>
    <text x="18" y="32" font-family="sans-serif" font-size="15" font-weight="bold" fill="#0369a1">GFPGAN v1.4</text>
    <text x="18" y="55" font-family="sans-serif" font-size="11" fill="#334155">• Detecta rostros con IA facial</text>
    <text x="18" y="72" font-family="sans-serif" font-size="11" fill="#334155">• Restaura ojos, piel y rasgos perdidos</text>
    <text x="18" y="88" font-family="monospace" font-size="10" font-weight="bold" fill="#0284c7">{base}_caras.png (1x)</text>
  </g>

  <!-- Rama 2: Real-ESRGAN Vulkan (GPU) -->
  <g transform="translate(267, 160)">
    <rect width="280" height="95" rx="10" fill="#eef2ff" stroke="#4f46e5" stroke-width="2" />
    <rect x="165" y="12" width="102" height="22" rx="11" fill="url(#grad-gpu-box)" />
    <text x="216" y="27" font-family="monospace" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">GPU RX 580</text>
    <text x="18" y="32" font-family="sans-serif" font-size="15" font-weight="bold" fill="#3730a3">Real-ESRGAN 4x</text>
    <text x="18" y="55" font-family="sans-serif" font-size="11" fill="#334155">• Cuadriplica la resolución (4x)</text>
    <text x="18" y="72" font-family="sans-serif" font-size="11" fill="#334155">• Elimina ruido, grano y desenfoque</text>
    <text x="18" y="88" font-family="monospace" font-size="10" font-weight="bold" fill="#4338ca">{base}_ia.png (4x Ultra)</text>
  </g>

  <!-- Conectores hacia Fusión -->
  <path d="M 547 62 L 585 62 L 585 105 L 605 105" stroke="#10b981" stroke-width="2.5" fill="none" />
  <polygon points="605,101 612,105 605,109" fill="#10b981" />

  <path d="M 547 207 L 585 207 L 585 165 L 605 165" stroke="#10b981" stroke-width="2.5" fill="none" />
  <polygon points="605,161 612,165 605,169" fill="#10b981" />

  <!-- FUSIÓN TOTAL -->
  <g transform="translate(615, 65)">
    <rect width="245" height="140" rx="12" fill="#ecfdf5" stroke="#10b981" stroke-width="2.5" />
    <rect x="12" y="12" width="110" height="22" rx="11" fill="url(#grad-fusion-box)" />
    <text x="67" y="27" font-family="sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">⭐ RECOMENDADO</text>
    <text x="15" y="58" font-family="sans-serif" font-size="16" font-weight="bold" fill="#065f46">Restauración Total</text>
    <text x="15" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="#047857">Rostros GFPGAN + 4x GPU</text>
    <text x="15" y="98" font-family="sans-serif" font-size="10" fill="#334155">Lo mejor de ambos mundos</text>
    <text x="15" y="115" font-family="monospace" font-size="10" font-weight="bold" fill="#059669">{base}_completa.png</text>
    <rect x="15" y="122" width="215" height="1" fill="#10b981" opacity="0.3" />
  </g>
</svg>'''

# -------------------------------------------------------------
# 3. DIAGRAMA DEL VISOR COMPARADOR Y ATAJOS
# -------------------------------------------------------------
svg_visor = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 340" width="880" height="340">
  <defs>
    <linearGradient id="bg-card" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#020617"/></linearGradient>
    <linearGradient id="bg-box-visor" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#18181b"/><stop offset="100%" stop-color="#09090b"/></linearGradient>
  </defs>

  <rect width="880" height="340" rx="14" fill="url(#bg-card)" stroke="#334155" stroke-width="2" />

  <!-- Barra Superior de la Tarjeta -->
  <g transform="translate(30, 25)">
    <circle cx="8" cy="12" r="5" fill="#10b981" />
    <text x="22" y="16" font-family="sans-serif" font-size="13" font-weight="bold" fill="#f8fafc">Listo para revisión</text>
    <rect x="160" y="2" width="140" height="20" rx="6" fill="#1e293b" />
    <text x="230" y="16" font-family="monospace" font-size="10" fill="#10b981" text-anchor="middle">2 rostros detectados</text>

    <!-- Pestañas de Capas -->
    <g transform="translate(470, 0)">
      <rect x="0" y="0" width="145" height="25" rx="6" fill="#10b981" />
      <text x="72" y="16" font-family="sans-serif" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">Total (Rostros+4x) [1]</text>

      <rect x="153" y="0" width="85" height="25" rx="6" fill="#1e293b" stroke="#475569" />
      <text x="195" y="16" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">Solo 4x [2]</text>

      <rect x="246" y="0" width="75" height="25" rx="6" fill="#1e293b" stroke="#475569" />
      <text x="283" y="16" font-family="sans-serif" font-size="11" font-weight="bold" fill="#94a3b8" text-anchor="middle">Facial [3]</text>
    </g>
  </g>

  <!-- El Visor Interactivo Dividido -->
  <g transform="translate(30, 65)">
    <rect width="820" height="190" rx="10" fill="url(#bg-box-visor)" stroke="#1e293b" stroke-width="1.5" />
    
    <!-- Lado Izquierdo: Original -->
    <rect x="0" y="0" width="410" height="190" rx="10" fill="#1c1917" opacity="0.6" />
    <text x="50" y="95" font-family="sans-serif" font-size="18" font-weight="900" fill="#78716c">ORIGINAL</text>
    <text x="50" y="120" font-family="sans-serif" font-size="12" fill="#a8a29e">Escaneo natural sin IA</text>
    <rect x="15" y="155" width="70" height="22" rx="4" fill="#09090b" opacity="0.8" />
    <text x="50" y="170" font-family="sans-serif" font-size="10" fill="#e2e8f0" text-anchor="middle">Original</text>

    <!-- Lado Derecho: Restauración Total -->
    <text x="490" y="95" font-family="sans-serif" font-size="18" font-weight="900" fill="#10b981">RESTAURACIÓN TOTAL</text>
    <text x="490" y="120" font-family="sans-serif" font-size="12" fill="#6ee7b7">Rostros GFPGAN + Escalado 4x GPU</text>
    <rect x="690" y="155" width="115" height="22" rx="4" fill="#09090b" opacity="0.8" />
    <text x="747" y="170" font-family="sans-serif" font-size="10" font-weight="bold" fill="#10b981" text-anchor="middle">Restauración Total</text>

    <!-- Línea divisoria interactiva -->
    <line x1="410" y1="0" x2="410" y2="190" stroke="#10b981" stroke-width="3" />
    <circle cx="410" cy="95" r="16" fill="#0f172a" stroke="#10b981" stroke-width="2.5" />
    <path d="M 403 95 L 407 91 M 403 95 L 407 99" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
    <path d="M 417 95 L 413 91 M 417 95 L 413 99" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />

    <!-- Botón Lupa en esquina superior derecha -->
    <g transform="translate(725, 12)">
      <rect width="82" height="26" rx="6" fill="#1e293b" stroke="#6366f1" stroke-width="1.5" />
      <text x="41" y="17" font-family="sans-serif" font-size="11" font-weight="bold" fill="#c7d2fe" text-anchor="middle">🔍 Lupa 2x</text>
    </g>
  </g>

  <!-- Botonera Inferior de Acciones -->
  <g transform="translate(30, 275)">
    <!-- Herramientas -->
    <rect x="0" y="0" width="85" height="36" rx="8" fill="#1e293b" stroke="#334155" />
    <text x="42" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#cbd5e1" text-anchor="middle">🔄 Rotar</text>

    <rect x="95" y="0" width="105" height="36" rx="8" fill="#1e293b" stroke="#334155" />
    <text x="147" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#cbd5e1" text-anchor="middle">✂️ Recortar</text>

    <rect x="210" y="0" width="80" height="36" rx="8" fill="#1e293b" stroke="#6366f1" />
    <text x="250" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#a5b4fc" text-anchor="middle">🔍 Lupa</text>

    <!-- Botones de Aprobación -->
    <rect x="330" y="0" width="180" height="36" rx="8" fill="#10b981" />
    <text x="420" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">⭐ Aprobar Total [A]</text>

    <rect x="520" y="0" width="95" height="36" rx="8" fill="#4f46e5" />
    <text x="567" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Solo 4x [I]</text>

    <rect x="625" y="0" width="90" height="36" rx="8" fill="#0284c7" />
    <text x="670" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">Facial [C]</text>

    <rect x="725" y="0" width="85" height="36" rx="8" fill="#334155" />
    <text x="767" y="22" font-family="sans-serif" font-size="12" font-weight="bold" fill="#e2e8f0" text-anchor="middle">Original [O]</text>
  </g>
</svg>'''

# -------------------------------------------------------------
# 4. DIAGRAMA DE RED Y SERVIDOR NAS
# -------------------------------------------------------------
svg_red = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 180" width="880" height="180">
  <defs>
    <linearGradient id="grad-nas-bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0f172a"/><stop offset="100%" stop-color="#020617"/></linearGradient>
  </defs>

  <rect width="880" height="180" rx="12" fill="#ffffff" stroke="#e2e8f0" stroke-width="2" />

  <!-- Escáner Xerox -->
  <g transform="translate(20, 25)">
    <rect width="180" height="130" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2" />
    <text x="90" y="38" font-family="sans-serif" font-size="15" font-weight="bold" fill="#0f172a" text-anchor="middle">Escáner Xerox</text>
    <text x="90" y="60" font-family="sans-serif" font-size="12" fill="#475569" text-anchor="middle">Phaser 3100 Flatbed</text>
    <rect x="25" y="80" width="130" height="24" rx="6" fill="#e2e8f0" />
    <text x="90" y="96" font-family="monospace" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">USB / SANE 300 DPI</text>
    <text x="90" y="122" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Hasta 4 fotos en platina</text>
  </g>

  <!-- Flecha Escáner -> PC -->
  <path d="M 200 90 L 250 90" stroke="#10b981" stroke-width="3" fill="none" />
  <polygon points="250,85 260,90 250,95" fill="#10b981" />

  <!-- PC Desktopia Lab -->
  <g transform="translate(260, 15)">
    <rect width="280" height="150" rx="12" fill="#f0fdf4" stroke="#10b981" stroke-width="2.5" />
    <text x="140" y="32" font-family="sans-serif" font-size="15" font-weight="bold" fill="#065f46" text-anchor="middle">Estación Desktopia Lab</text>
    <text x="140" y="52" font-family="sans-serif" font-size="11" fill="#047857" text-anchor="middle">FastAPI + OpenCV + GPU Vulkan + GFPGAN</text>
    
    <rect x="25" y="65" width="230" height="30" rx="6" fill="#10b981" />
    <text x="140" y="85" font-family="monospace" font-size="12" font-weight="bold" fill="#ffffff" text-anchor="middle">http://192.168.1.48:7777</text>
    
    <text x="140" y="112" font-family="sans-serif" font-size="10" fill="#334155" text-anchor="middle">• Compatible con Navegador de PC y Celular</text>
    <text x="140" y="128" font-family="sans-serif" font-size="10" fill="#334155" text-anchor="middle">• Inyección automática de metadatos EXIF</text>
  </g>

  <!-- Flecha PC -> NAS -->
  <path d="M 540 90 L 590 90" stroke="#10b981" stroke-width="3" fill="none" />
  <polygon points="590,85 600,90 590,95" fill="#10b981" />

  <!-- Servidor NAS -->
  <g transform="translate(600, 15)">
    <rect width="260" height="150" rx="12" fill="url(#grad-nas-bg)" stroke="#38bdf8" stroke-width="2" />
    <text x="130" y="32" font-family="sans-serif" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">Servidor NAS Central</text>
    <text x="130" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">IP: 192.168.1.80 (SSH rsync)</text>
    
    <rect x="15" y="62" width="230" height="58" rx="6" fill="#1e293b" stroke="#334155" />
    <text x="130" y="76" font-family="monospace" font-size="7.5" fill="#94a3b8" text-anchor="middle">/srv/dev-disk-by-uuid-69fe1c68-291a-4766-</text>
    <text x="130" y="90" font-family="monospace" font-size="7.8" fill="#94a3b8" text-anchor="middle">8e61-bdc74f584e89/Fotos_escaneadas/</text>
    <text x="130" y="109" font-family="monospace" font-size="10.5" font-weight="bold" fill="#a7f3d0" text-anchor="middle">[Nombre_Album]_[Año]/</text>

    <text x="130" y="136" font-family="sans-serif" font-size="10" fill="#64748b" text-anchor="middle">Almacenamiento permanente y seguro</text>
  </g>
</svg>'''

# -------------------------------------------------------------
# 5. DIAGRAMA DE LA HERRAMIENTA DE RECORTE Y ENCUADRE
# -------------------------------------------------------------
svg_recorte = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 220" width="880" height="220">
  <rect width="880" height="220" rx="12" fill="#09090b" stroke="#27272a" stroke-width="2" />

  <!-- Título Modal Recorte -->
  <g transform="translate(25, 25)">
    <text x="0" y="16" font-family="sans-serif" font-size="15" font-weight="bold" fill="#f43f5e">✂️ Herramienta de Recorte y Encuadre</text>
    <text x="0" y="34" font-family="sans-serif" font-size="11" fill="#a1a1aa">Permite corregir bordes de fotos torcidas o extraer una foto individual de un escaneo múltiple.</text>
  </g>

  <!-- Simulación del área de recorte -->
  <g transform="translate(25, 70)">
    <!-- Marco de imagen escaneada -->
    <rect width="420" height="130" rx="6" fill="#18181b" stroke="#3f3f46" stroke-width="1.5" />
    <text x="210" y="70" font-family="sans-serif" font-size="12" fill="#52525b" text-anchor="middle">Área externa descartada (sombra oscura)</text>

    <!-- Caja de Selección de Recorte -->
    <rect x="70" y="20" width="280" height="90" fill="#27272a" stroke="#10b981" stroke-width="2" opacity="0.9" />

    <!-- Guías regla de tercios -->
    <line x1="163" y1="20" x2="163" y2="110" stroke="#10b981" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />
    <line x1="256" y1="20" x2="256" y2="110" stroke="#10b981" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />
    <line x1="70" y1="50" x2="350" y2="50" stroke="#10b981" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />
    <line x1="70" y1="80" x2="350" y2="80" stroke="#10b981" stroke-width="1" stroke-dasharray="3,3" opacity="0.6" />

    <!-- Cruz guía central -->
    <circle cx="210" cy="65" r="12" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.8" />
    <circle cx="210" cy="65" r="3" fill="#10b981" />
    <line x1="210" y1="20" x2="210" y2="110" stroke="#10b981" stroke-width="1" opacity="0.5" />
    <line x1="70" y1="65" x2="350" y2="65" stroke="#10b981" stroke-width="1" opacity="0.5" />

    <!-- Manijas táctiles en esquinas -->
    <rect x="66" y="16" width="8" height="8" fill="#10b981" />
    <rect x="346" y="16" width="8" height="8" fill="#10b981" />
    <rect x="66" y="106" width="8" height="8" fill="#10b981" />
    <rect x="346" y="106" width="8" height="8" fill="#10b981" />
  </g>

  <!-- Explicación de las 2 Opciones -->
  <g transform="translate(470, 70)">
    <!-- Opción 1: Aplicar Recorte -->
    <rect width="380" height="60" rx="8" fill="#132a22" stroke="#10b981" stroke-width="1.5" />
    <text x="15" y="24" font-family="sans-serif" font-size="12" font-weight="bold" fill="#34d399">Opción 1: [ Aplicar Recorte ]</text>
    <text x="15" y="42" font-family="sans-serif" font-size="11" fill="#a7f3d0">Ajusta la foto actual. Se sincroniza automáticamente en</text>
    <text x="15" y="54" font-family="sans-serif" font-size="10" fill="#6ee7b7">todas las variantes (Original, Rostros, 4x y Completa).</text>

    <!-- Opción 2: Extraer como Foto Nueva -->
    <g transform="translate(0, 70)">
      <rect width="380" height="60" rx="8" fill="#1e1e38" stroke="#818cf8" stroke-width="1.5" />
      <text x="15" y="24" font-family="sans-serif" font-size="12" font-weight="bold" fill="#a5b4fc">Opción 2: [ Extraer como foto nueva ]</text>
      <text x="15" y="42" font-family="sans-serif" font-size="11" fill="#c7d2fe">Crea una tarjeta fotográfica independiente y le aplica el</text>
      <text x="15" y="54" font-family="sans-serif" font-size="10" fill="#818cf8">motor de IA desde cero sin borrar la foto anterior.</text>
    </g>
  </g>
</svg>'''

(DIR_MANUAL / "diagrama_flujo.svg").write_text(svg_flujo, encoding="utf-8")
(DIR_MANUAL / "diagrama_ia.svg").write_text(svg_ia, encoding="utf-8")
(DIR_MANUAL / "diagrama_visor.svg").write_text(svg_visor, encoding="utf-8")
(DIR_MANUAL / "diagrama_red.svg").write_text(svg_red, encoding="utf-8")
(DIR_MANUAL / "diagrama_recorte.svg").write_text(svg_recorte, encoding="utf-8")

print("Generando PNGs con Inkscape a 300 DPI...")
for svg in DIR_MANUAL.glob("*.svg"):
    png = svg.with_suffix(".png")
    subprocess.run(["inkscape", str(svg), f"--export-filename={png}", "--export-dpi=300"], check=True)

print("✅ Todos los diagramas generados y exportados a PNG exitosamente.")
