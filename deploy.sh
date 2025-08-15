#!/bin/bash

# Production deployment script

set -e

echo ""
echo "🚀 Starting deployment..."
echo ""

# Determine which environment file to use based on HOST variable
if [ "$(hostname)" = "simplex4learning" ]; then
    ENV_FILE=".env.simplex4learning"
    echo "🏢 HOST is simplex4learning - using $ENV_FILE"
else
    ENV_FILE=".env"
    echo "🏠 HOST is not simplex4learning - using $ENV_FILE"
fi

# Export ENV_FILE so docker-compose can use it
export ENV_FILE

# Load environment variables from the determined .env file
if [ -f "$ENV_FILE" ]; then
    echo "📋 Loading environment variables from $ENV_FILE file..."
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)
    echo "✅ Environment variables loaded from $ENV_FILE"
else
    echo "⚠️ Warning: $ENV_FILE file not found"
    echo ""
    exit 1
fi
echo ""

# Detect OS and set Docker Compose command
if [[ "$OSTYPE" == "darwin"* ]]; then
    DOCKER_COMPOSE_CMD="docker-compose"
    echo "🍎 macOS detected - using docker-compose command"
else
    DOCKER_COMPOSE_CMD="docker compose"
    echo "🐧 Linux/Other OS detected - using docker compose command"
fi
echo ""

echo "📊 Deployment Configuration:"
echo "  🌐 Server Hostname: ${SERVER_NAME}"
echo "  🔌 Proxy Port: ${PROXY_PORT}"
echo "  🔌 Frontend Port: ${FRONTEND_PORT}"
echo "  🔧 Backend Host: ${BACKEND_HOST}"
echo "  🔧 Backend Port: ${BACKEND_PORT}"
echo "  🗄️  Database Host: ${POSTGRES_HOST}"
echo "  🗄️  Database Port (External): ${POSTGRES_PORT_OUT}"
echo "  🗄️  Database Port (Internal): ${POSTGRES_PORT}"
echo "  📦 Database Name: ${POSTGRES_DB}"
echo "  👤 Database User: ${POSTGRES_USER}"
echo "  ⏱️  Proxy Timeout: ${PROXY_TIMEOUT}s"
echo "  📁 Text Data Path: ${TEXT_DATA_PATH}"
echo "  🔄 Fill Database: ${FILL_DATABASE}"
echo ""

# Stop existing containers
echo "🛑 Stopping existing containers..."
${DOCKER_COMPOSE_CMD} down
echo ""

# Build and start services
echo "🔨 Building and starting services..."
${DOCKER_COMPOSE_CMD} up --build -d
echo ""

if [ "$FILL_DATABASE" -eq 1 ]; then
    ./fill-database.sh
    echo ""
fi

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10
echo ""

# Check service health
echo "🔍 Checking service health..."
${DOCKER_COMPOSE_CMD} ps
echo ""

# Basic health checks
echo "🏥 Performing health checks..."
if curl -f "http://localhost:${BACKEND_PORT}/api/hello" >/dev/null 2>&1; then
    echo "✅ Backend API is responding on port ${BACKEND_PORT}"
else
    echo "⚠️  Backend API not yet ready on port ${BACKEND_PORT}"
fi

if curl -f "http://localhost:${FRONTEND_PORT}" >/dev/null 2>&1; then
    echo "✅ Frontend is responding on port ${FRONTEND_PORT}"
else
    echo "⚠️  Frontend not yet ready on port ${FRONTEND_PORT}"
fi

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your application should be available at: http://${SERVER_NAME}:${FRONTEND_PORT}"
echo ""
echo "📊 Useful commands:"
echo "   📋 Check logs: ${DOCKER_COMPOSE_CMD} logs -f"
echo "   📊 Check status: ${DOCKER_COMPOSE_CMD} ps"
echo "   🛑 Stop services: ${DOCKER_COMPOSE_CMD} down"
echo "   🔄 Restart: ${DOCKER_COMPOSE_CMD} restart" 
echo ""