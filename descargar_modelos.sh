#!/bin/bash
# ==============================================================================
# Descarga automática de binarios y pesos de IA para Desktopia Lab 2.0
# Excluidos de GitHub por superar el límite de tamaño (>100 MB).
# ==============================================================================
set -e

DIR_APP="$(cd "$(dirname "$0")" && pwd)"
DIR_IA="$DIR_APP/ia_engine"
DIR_MODELS="$DIR_IA/models"
DIR_GFPGAN="$DIR_APP/gfpgan/weights"

mkdir -p "$DIR_MODELS" "$DIR_GFPGAN"

descargar() {
    local url="$1"
    local destino="$2"
    local tmp="${destino}.tmp"

    echo "⬇️  Descargando $(basename "$destino")..."
    if command -v curl >/dev/null 2>&1; then
        curl -fL --progress-bar "$url" -o "$tmp"
    elif command -v wget >/dev/null 2>&1; then
        wget -q --show-progress "$url" -O "$tmp"
    else
        echo "❌ Error: necesitás tener instalado 'curl' o 'wget' para descargar modelos."
        exit 1
    fi
    mv "$tmp" "$destino"
    echo "✅ Listo: $destino"
}

echo "=================================================="
echo "  Verificando motores y modelos de IA..."
echo "=================================================="

# 1. Real-ESRGAN Vulkan ncnn (GPU)
if [ ! -x "$DIR_IA/realesrgan-ncnn-vulkan" ] || [ ! -s "$DIR_MODELS/realesrgan-x4plus.bin" ]; then
    TMP_DIR="$(mktemp -d)"
    ZIP_PATH="$TMP_DIR/realesrgan.zip"
    URL_REALESRGAN="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip"

    descargar "$URL_REALESRGAN" "$ZIP_PATH"

    echo "📦 Descomprimiendo Real-ESRGAN Vulkan..."
    if command -v unzip >/dev/null 2>&1; then
        unzip -oq "$ZIP_PATH" -d "$TMP_DIR/extract"
    else
        python3 -m zipfile -e "$ZIP_PATH" "$TMP_DIR/extract"
    fi

    BIN_FOUND="$(find "$TMP_DIR/extract" -name "realesrgan-ncnn-vulkan" -type f | head -n 1)"
    MODELS_FOUND="$(find "$TMP_DIR/extract" -type d -name "models" | head -n 1)"

    if [ -z "$BIN_FOUND" ] || [ -z "$MODELS_FOUND" ]; then
        rm -rf "$TMP_DIR"
        echo "❌ No se encontró el binario o la carpeta models dentro del zip descargado."
        exit 1
    fi

    cp "$BIN_FOUND" "$DIR_IA/realesrgan-ncnn-vulkan"
    chmod +x "$DIR_IA/realesrgan-ncnn-vulkan"
    cp -r "$MODELS_FOUND"/* "$DIR_MODELS/"

    rm -rf "$TMP_DIR"
    echo "✅ Motor Real-ESRGAN Vulkan instalado en ia_engine/"
else
    echo "✔ Motor Real-ESRGAN Vulkan ya disponible."
fi

# 2. GFPGAN v1.4 (Restauración facial CPU)
if [ ! -s "$DIR_GFPGAN/GFPGANv1.4.pth" ]; then
    descargar "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth" \
              "$DIR_GFPGAN/GFPGANv1.4.pth" || \
    descargar "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth" \
              "$DIR_GFPGAN/GFPGANv1.4.pth"
else
    echo "✔ Modelo GFPGANv1.4.pth ya disponible."
fi

# 3. Facexlib Detection (Detector de rostros)
if [ ! -s "$DIR_GFPGAN/detection_Resnet50_Final.pth" ]; then
    descargar "https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth" \
              "$DIR_GFPGAN/detection_Resnet50_Final.pth"
else
    echo "✔ Modelo detection_Resnet50_Final.pth ya disponible."
fi

# 4. Facexlib Parsing (Segmentación facial)
if [ ! -s "$DIR_GFPGAN/parsing_parsenet.pth" ]; then
    descargar "https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth" \
              "$DIR_GFPGAN/parsing_parsenet.pth"
else
    echo "✔ Modelo parsing_parsenet.pth ya disponible."
fi

echo "=================================================="
echo "  🚀 Todos los modelos de IA están listos."
echo "=================================================="
