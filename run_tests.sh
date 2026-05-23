#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              TZU - Test Runner                           ║"
echo "║         Ejecutando todos los tests de Python            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Resolve project root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Detect python3 or python
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
    echo "❌ Error: no se encontró python3 ni python en el PATH"
    exit 1
fi

# Create virtualenv if missing
if [ ! -f ".venv/bin/activate" ]; then
    echo "📦 Creando entorno virtual..."
    $PYTHON -m venv .venv
fi

source .venv/bin/activate
PYTHON=$(command -v python3 || command -v python)

# Install dependencies if not already installed
if ! $PYTHON -c "import fastapi" 2>/dev/null; then
    echo "📥 Instalando dependencias desde api/requirements.txt..."
    $PYTHON -m pip install -q -r api/requirements.txt
fi

export PYTHONPATH="$SCRIPT_DIR/api"
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key-for-testing"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"

echo "🔧 Configuración del entorno:"
echo "  - PYTHONPATH: $PYTHONPATH"
echo "  - Python executable: $PYTHON"
echo "  - Pytest version: $($PYTHON -m pytest --version 2>&1)"
echo ""

echo "🧪 Ejecutando tests que funcionan correctamente..."
$PYTHON -m pytest \
    api/tests/test_auth_endpoints.py \
    api/tests/test_system_endpoints.py \
    api/tests/test_threat_endpoints.py \
    api/tests/test_information_system_endpoints.py \
    api/tests/test_integration_flows.py \
    -v --tb=short

echo ""
echo "🔍 Intentando ejecutar tests con problemas de importación..."

cd api
echo "📁 Ejecutando desde directorio api..."
$PYTHON -m pytest \
    tests/test_basic_system.py \
    tests/test_control_tags_api_endpoints.py \
    tests/test_control_tags_db.py \
    tests/test_direct_system.py \
    tests/test_enhanced_search_functionality.py \
    tests/test_reports_functionality.py \
    tests/test_tags_and_reports.py \
    -v --tb=short --continue-on-collection-errors
cd ..

echo ""
echo "✅ Ejecución de tests completada"
