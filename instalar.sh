#!/bin/bash
# ==============================================================================
# Instalador completo de Desktopia Lab 2.0 tras clonar desde GitHub
# ==============================================================================
set -e

DIR_APP="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR_APP"

echo "🛠️  Configurando Desktopia Lab 2.0 en $DIR_APP..."

# 1. Crear entorno virtual si no existe
if [ ! -d "$DIR_APP/venv" ]; then
    echo "🐍 Creando entorno virtual Python (venv)..."
    python3 -m venv "$DIR_APP/venv"
fi

# 2. Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
"$DIR_APP/venv/bin/pip" install --upgrade pip
"$DIR_APP/venv/bin/pip" install -r "$DIR_APP/requirements.txt"
"$DIR_APP/venv/bin/pip" install torch torchvision --index-url https://download.pytorch.org/whl/cpu
"$DIR_APP/venv/bin/pip" install gfpgan

# 3. Crear .env desde .env.example si no existe
if [ ! -f "$DIR_APP/.env" ] && [ -f "$DIR_APP/.env.example" ]; then
    cp "$DIR_APP/.env.example" "$DIR_APP/.env"
    echo "📝 Archivo .env creado desde .env.example (recordá configurar NAS_PASS si corresponde)."
fi

# 4. Descargar motores y pesos pesados de IA
chmod +x "$DIR_APP/descargar_modelos.sh" "$DIR_APP/iniciar_desktopia.sh"
"$DIR_APP/descargar_modelos.sh"

echo ""
echo "✅ Instalación finalizada. Podés iniciar el sistema con:"
echo "   ./iniciar_desktopia.sh"
