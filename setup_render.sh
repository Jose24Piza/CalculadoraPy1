# setup_render.sh - Script para configurar entorno en Render

set -e
echo "🔧 Configurando entorno para Render..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar variables de entorno de Render
echo "📌 Verificando entorno de Render..."
if [ -n "$RENDER" ]; then
    echo -e "${GREEN}✅ Ejecutando en Render${NC}"
    echo "📊 Servicio: ${RENDER_SERVICE_NAME:-Unknown}"
    echo "🔗 Branch: ${RENDER_GIT_BRANCH:-Unknown}"
    echo "📦 Commit: ${RENDER_GIT_COMMIT:-Unknown}"
else
    echo -e "${YELLOW}⚠️ No se detectó entorno Render${NC}"
fi

# Instalar dependencias
echo "📌 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Instalar dependencias de desarrollo (para staging)
if [ "$FLASK_ENV" = "staging" ] || [ "$FLASK_ENV" = "development" ]; then
    echo "📌 Instalando dependencias de desarrollo..."
    pip install pytest pytest-cov flake8 black mypy
fi

# Crear directorios necesarios
echo "📌 Creando estructura de directorios..."
mkdir -p logs
mkdir -p reports

# Configurar logging
echo "📌 Configurando logging..."
if [ "$LOG_LEVEL" = "DEBUG" ]; then
    echo "🐛 Modo DEBUG activado"
elif [ "$LOG_LEVEL" = "INFO" ]; then
    echo "ℹ️ Modo INFO activado"
fi

# Ejecutar pruebas solo en staging
if [ "$FLASK_ENV" = "staging" ]; then
    echo "🧪 Ejecutando pruebas en entorno staging..."
    export PYTHONPATH="${PYTHONPATH}:${PWD}"
    python -m pytest tests/ -v --cov=. --cov-report=term-missing || {
        echo -e "${RED}❌ Pruebas fallaron en staging${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Pruebas pasaron exitosamente${NC}"
fi

# Verificar health check
echo "🏥 Verificando health check..."
if [ -f "app.py" ]; then
    if grep -q "/health" app.py; then
        echo -e "${GREEN}✅ Health check configurado correctamente${NC}"
    else
        echo -e "${YELLOW}⚠️ Health check no encontrado en app.py${NC}"
    fi
fi

# Información final
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Configuración completada en Render${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📊 Información del despliegue:"
echo "  - Servicio: ${RENDER_SERVICE_NAME:-Unknown}"
echo "  - Entorno: ${FLASK_ENV:-production}"
echo "  - Puerto: ${PORT:-5000}"
echo ""
echo "🔗 URLs de servicio:"
echo "  - Principal: https://${RENDER_SERVICE_NAME:-calculadorapy}.onrender.com"
echo "  - Health: https://${RENDER_SERVICE_NAME:-calculadorapy}.onrender.com/health"
echo "  - Metrics: https://${RENDER_SERVICE_NAME:-calculadorapy}.onrender.com/metrics"