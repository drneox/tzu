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

# Detect Docker Compose command (prefer V2 plugin over legacy V1)
if command -v docker &> /dev/null && docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
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

# Function to check container status
check_container_status() {
    local compose_cmd="$1"
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for containers to start..."
    
    while [ $attempt -le $max_attempts ]; do
        cd docker
        
        # Get container status
        local containers_info=$($compose_cmd ps --format "table {{.Service}}\t{{.Status}}" 2>/dev/null)
        local all_running=true
        local failed_services=""

        # Check each expected service
        for service in postgresql backend frontend nginx; do
            local service_line=$(echo "$containers_info" | grep "^$service")

            if [[ -z "$service_line" ]]; then
                all_running=false
                failed_services="$failed_services $service(not_found)"
            elif [[ ! "$service_line" =~ Up ]] && [[ ! "$service_line" =~ running ]]; then
                all_running=false
                failed_services="$failed_services $service(not_running)"
            fi
        done
        
        cd ..
        
        if [ "$all_running" = true ]; then
            echo "✅ All containers are running"
            return 0
        else
            if [ $attempt -eq $max_attempts ]; then
                echo "❌ Container validation failed after $max_attempts attempts"
                echo "❌ Failed services:$failed_services"
                return 1
            fi
            echo "⏳ Attempt $attempt/$max_attempts: Waiting for containers to be ready..."
            sleep 5
            attempt=$((attempt + 1))
        fi
    done
}

# Function to check health status for services with healthchecks
check_health_status() {
    local compose_cmd="$1"
    
    echo "🔍 Checking service health..."
    
    cd docker
    
    # Check postgresql health (it has a healthcheck)
    local pg_health=$($compose_cmd ps postgresql --format "table {{.Status}}" 2>/dev/null | tail -n +2)
    
    cd ..
    
    if [[ "$pg_health" =~ "healthy" ]]; then
        echo "✅ PostgreSQL is healthy"
        return 0
    else
        echo "⚠️  PostgreSQL health check: $pg_health"
        # Don't fail here, just warn - container might still be starting
        return 0
    fi
}

# Function to wait for backend initialization to complete
wait_for_backend_initialization() {
    local compose_cmd="$1"
    local max_attempts=20
    local attempt=1
    
    echo "⏳ Waiting for backend initialization to complete..."
    
    while [ $attempt -le $max_attempts ]; do
        cd docker
        
        # Check if backend has completed initialization
        local backend_logs=$($compose_cmd logs backend 2>&1)
        
        cd ..
        
        # Look for signs that initialization is complete
        if echo "$backend_logs" | grep -q "Uvicorn running on" && echo "$backend_logs" | grep -q "Application startup complete"; then
            echo "✅ Backend initialization completed"
            # Give it a moment more to ensure all logs are captured
            sleep 3
            return 0
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            echo "⚠️  Backend initialization check timed out after $max_attempts attempts"
            echo "⚠️  Proceeding anyway - logs may be incomplete"
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts: Waiting for backend to complete initialization..."
        sleep 3
        attempt=$((attempt + 1))
    done
}

# Wait for containers to start and validate their status
echo "⏳ Waiting for system initialization..."
if ! check_container_status "$COMPOSE_CMD"; then
    echo "❌ Failed to start all containers properly"
    echo "💡 Try running: cd docker && $COMPOSE_CMD logs"
    echo "💡 Or check individual container status: cd docker && $COMPOSE_CMD ps"
    exit 1
fi

# Check health status
check_health_status "$COMPOSE_CMD"

# Wait for backend initialization to complete
wait_for_backend_initialization "$COMPOSE_CMD"

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
