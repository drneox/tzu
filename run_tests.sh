#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              TZU - Test Runner                           ║"
echo "║         Ejecutando todos los tests de Python            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Configurar el directorio de trabajo
cd /Users/carlos/proyectos/test/tzu

# Configurar variables de entorno para los tests
export PYTHONPATH="/Users/carlos/proyectos/test/tzu"
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key-for-testing"
export ACCESS_TOKEN_EXPIRE_MINUTES="30"

# Activar el entorno virtual
source .venv/bin/activate

echo "🔧 Configuración del entorno:"
echo "  - PYTHONPATH: $PYTHONPATH"
echo "  - Python executable: $(which python)"
echo "  - Pytest version: $(python -m pytest --version)"
echo ""

echo "🧪 Ejecutando tests que funcionan correctamente..."
python -m pytest \
    api/tests/test_auth_endpoints.py \
    api/tests/test_system_endpoints.py \
    api/tests/test_threat_endpoints.py \
    api/tests/test_information_system_endpoints.py \
    api/tests/test_integration_flows.py \
    -v --tb=short

echo ""
echo "🔍 Intentando ejecutar tests con problemas de importación..."

# Ejecutar desde el directorio api para los tests problemáticos
cd api

echo "📁 Ejecutando desde directorio api..."
python -m pytest \
    tests/test_control_tags_endpoints.py \
    tests/test_control_tags_reports.py \
    tests/test_controls_endpoints.py \
    tests/test_frontend_control_tags.py \
    tests/test_integration_controls.py \
    tests/test_modular_controls.py \
    tests/test_reports_control_tags.py \
    tests/test_reports_functionality.py \
    -v --tb=short --continue-on-collection-errors

cd ..

echo ""
echo "✅ Ejecución de tests completada"
