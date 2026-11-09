#!/bin/bash
# ==========================================================
# Lanzador de Desktopia Lab (1 solo clic para los chicos)
# ==========================================================

DIR_APP="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "$DIR_APP" || exit 1

# 0. Descargar automáticamente motores y modelos de IA si faltan (primer uso tras clonar)
if [ ! -x "$DIR_APP/ia_engine/realesrgan-ncnn-vulkan" ] || \
   [ ! -s "$DIR_APP/ia_engine/models/realesrgan-x4plus.bin" ] || \
   [ ! -s "$DIR_APP/gfpgan/weights/GFPGANv1.4.pth" ] || \
   [ ! -s "$DIR_APP/gfpgan/weights/detection_Resnet50_Final.pth" ] || \
   [ ! -s "$DIR_APP/gfpgan/weights/parsing_parsenet.pth" ]; then
    "$DIR_APP/descargar_modelos.sh" >> "$DIR_APP/desktopia.log" 2>&1 || exit 1
fi

# 1. Cerrar instancias previas si quedaron abiertas
pkill -f "run.py" 2>/dev/null
pkill -f "uvicorn.*app.main:app" 2>/dev/null
sleep 0.5

# 2. Iniciar el servidor desacoplado en segundo plano
nohup ./venv/bin/python3 run.py > "$DIR_APP/desktopia.log" 2>&1 &

# 3. Esperar que el servidor FastAPI esté respondiendo (máximo 10s)
for i in {1..20}; do
    if curl -s http://127.0.0.1:7777/api/health >/dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

# 4. Abrir la interfaz web en el navegador predeterminado
nohup xdg-open "http://127.0.0.1:7777" >/dev/null 2>&1 &
