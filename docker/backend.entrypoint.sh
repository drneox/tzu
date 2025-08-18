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

# Function to generate SECRET_KEY if not present
setup_environment() {
    echo "🔐 Checking environment configuration..."
    
    ENV_FILE="/app/.env"
    
    # Check if .env exists
    if [ ! -f "$ENV_FILE" ]; then
        echo "⚠️  .env file not found at $ENV_FILE"
        echo "📝 Please create .env file manually or copy from .env.example"
        echo "🔄 Continuing without environment file..."
        return
    fi
    
    echo "✅ Found .env file at $ENV_FILE"
    
    # Function to generate a secure random key
    generate_secret_key() {
        python3 -c "import secrets; print(secrets.token_urlsafe(32))"
    }
    
    # Check if SECRET_KEY exists in .env and is not empty
    if ! grep -q "^SECRET_KEY=" "$ENV_FILE" 2>/dev/null || [ -z "$(grep "^SECRET_KEY=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2)" ]; then
        echo "🔑 SECRET_KEY not found or empty. Generating new one..."
        echo "⚠️  WARNING: This will invalidate all existing JWT tokens!"
        
        # Generate a new SECRET_KEY
        NEW_SECRET_KEY=$(generate_secret_key)
        
        # Remove any existing empty SECRET_KEY line
        sed -i '/^SECRET_KEY=$/d' "$ENV_FILE" 2>/dev/null || true
        
        # Add the new SECRET_KEY
        echo "SECRET_KEY=$NEW_SECRET_KEY" >> "$ENV_FILE"
        
        echo "✅ Generated new SECRET_KEY (${#NEW_SECRET_KEY} characters)"
        echo "💾 SECRET_KEY saved to $ENV_FILE for persistence"
    else
        EXISTING_KEY=$(grep "^SECRET_KEY=" "$ENV_FILE" | cut -d'=' -f2)
        echo "✅ Using existing SECRET_KEY (${#EXISTING_KEY} characters)"
        echo "🔒 JWT tokens will remain valid across restarts"
    fi
    
    # Export environment variables
    set -a
    source "$ENV_FILE"
    set +a
    
    # Validate required API keys
    if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ ERROR: No AI API keys found"
        echo "📝 Please set at least one: OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file"
        echo "🔧 Copy .env.example to .env and configure your API keys"
        exit 1
    else
        echo "✅ AI API key(s) configured"
    fi
    
    echo "📋 Environment configuration completed"
}

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
setup_environment
wait_for_db
apply_migrations
initialize_data
health_check
start_server
