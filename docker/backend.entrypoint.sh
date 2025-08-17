#!/bin/bash
set -e

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║              TZU - Threat Zero Utility                   ║"
echo "║           Backend Service Starting...                    ║"
echo "║                                                          ║"
echo "║              GitHub: drneox/tzu                          ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starting TZU Backend Service..."

# Function to wait for database
wait_for_db() {
    echo "🔄 Waiting for PostgreSQL to be available..."
    
    for i in {1..30}; do
        if nc -z postgresql 5432; then
            echo "✅ PostgreSQL is available"
            break
        fi
        
        if [ $i -eq 30 ]; then
            echo "❌ Timeout waiting for PostgreSQL"
            exit 1
        fi
        
        echo "⏳ Attempt $i/30: Waiting for PostgreSQL..."
        sleep 2
    done
}

# Function to apply migrations
apply_migrations() {
    echo "📊 Applying database migrations..."
    
    # Verify that Alembic is configured correctly
    if [ ! -f "alembic.ini" ]; then
        echo "❌ alembic.ini file not found"
        exit 1
    fi
    
    # Apply migrations with retries
    for i in {1..5}; do
        if alembic upgrade head; then
            echo "✅ Migrations applied successfully"
            break
        fi
        
        if [ $i -eq 5 ]; then
            echo "❌ Could not apply migrations after 5 attempts"
            exit 1
        fi
        
        echo "⚠️  Attempt $i/5 failed, retrying in 5 seconds..."
        sleep 5
    done
}

# Function to initialize data
initialize_data() {
    echo "👤 Initializing default data..."
    
    if python init_db.py; then
        echo "✅ Data initialized correctly"
    else
        echo "⚠️  Error initializing data, but continuing..."
    fi
}

# Function to verify health before starting
health_check() {
    echo "🔍 Verifying system health..."
    
    if python health_check.py; then
        echo "✅ Health check successful"
    else
        echo "❌ Health check failed"
        exit 1
    fi
}

# Function to start server
start_server() {
    echo "🌟 Starting FastAPI server..."
    exec uvicorn api:app --host 0.0.0.0 --port 8000 --reload
}

# Execute all functions in order
wait_for_db
apply_migrations
initialize_data
health_check
start_server
