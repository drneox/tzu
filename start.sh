#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              TZU - Threat Zero Utility                   ║"
echo "║         Security Risk Assessment Platform                ║"
echo "║                                                          ║"
echo "║              GitHub: drneox/tzu                          ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starting TZU with Docker..."

# Detect Docker Compose command
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Error: Docker Compose is not installed"
    exit 1
fi

echo "📦 Using: $COMPOSE_CMD"

# Clean previous containers but keep volumes
cd docker
$COMPOSE_CMD down
cd ..

# Start services
echo "🔧 Starting services..."
cd docker
$COMPOSE_CMD up -d --build
cd ..

# Wait briefly for services to come up
echo "⏳ Waiting for system initialization..."
sleep 10

# Get backend logs to capture credentials
echo "🔧 Capturing initialization credentials..."
cd docker
BACKEND_LOGS=$($COMPOSE_CMD logs backend 2>&1)
cd ..

echo "📋 Backend logs:"
echo "$BACKEND_LOGS"

PASSWORD=$(echo "$BACKEND_LOGS" | grep "Password:" | sed 's/.*Password: //')
CREATED=$(echo "$BACKEND_LOGS" | grep "DEFAULT USER CREDENTIALS CREATED")

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║                  🎉 TZU IS RUNNING!                      ║"
echo "║                                                          ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  📱 Application: http://localhost:3434                   ║"
echo "║  🔧 API Documentation: http://localhost:8000/docs        ║"
echo "║                                                          ║"
echo "║  👤 Access Credentials:                                  ║"
echo "║     📋 Username: admin                                   ║"

if [ ! -z "$CREATED" ] && [ ! -z "$PASSWORD" ] && [ "$PASSWORD" != "🔑 Password:" ]; then
    echo "║     🔑 Password: $PASSWORD                    ║"
    echo "║                                                          ║"
    echo "║  💡 These credentials were auto-generated                ║"
elif [ -z "$CREATED" ]; then
    echo "║     🔑 Password: [Hidden for security]                   ║"
    echo "║                                                          ║"
    echo "║  ℹ️  User already exists. To regenerate password:       ║"
    echo "║     cd docker && $COMPOSE_CMD exec backend python \\     ║"
    echo "║       /app/show_credentials.py                           ║"
fi

echo "║                                                          ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  🛑 To stop: cd docker && $COMPOSE_CMD down              ║"
echo "║  📚 Project: https://github.com/drneox/tzu               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
