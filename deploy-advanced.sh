#!/bin/bash

# Advanced production deployment script with .env support

set -e

echo ""
echo "🚀 Starting deployment..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to load .env file
load_env() {
    # Determine which environment file to use based on HOST variable
    if [ "$(hostname)" = "simplex4learning" ]; then
        ENV_FILE=".env.simplex4learning"
        echo -e "${BLUE}🏢 HOST is simplex4learning - using $ENV_FILE${NC}"
    else
        ENV_FILE=".env"
        echo -e "${BLUE}🏠 HOST is not simplex4learning - using $ENV_FILE${NC}"
    fi
    
    # Export ENV_FILE so docker-compose can use it
    export ENV_FILE
    
    if [ -f "$ENV_FILE" ]; then
        echo -e "${BLUE}📋 Loading environment variables from $ENV_FILE file...${NC}"
        
        # Method 1: Export all non-comment lines
        #export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)
        
        # Method 2: Source the file (alternative approach)
        set -a; source "$ENV_FILE"; set +a
        
        echo -e "${GREEN}✅ Environment variables loaded from $ENV_FILE${NC}"
    else
        echo -e "${YELLOW}⚠️  Warning: $ENV_FILE file not found. ${NC}"
        exit 1
    fi
}

# Function to validate required environment variables
validate_env() {
    echo -e "${BLUE}🔍 Validating environment variables...${NC}"
    
    required_vars=("SERVER_NAME" "PROXY_PORT" "FRONTEND_PORT" "BACKEND_HOST" "BACKEND_PORT" "POSTGRES_USER" "POSTGRES_DB" "POSTGRES_HOST" "POSTGRES_PORT" "POSTGRES_PORT_OUT")
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo -e "${RED}❌ Error: Required environment variable $var is not set${NC}"
            exit 1
        fi
    done
    
    echo -e "${GREEN}✅ All required environment variables are set${NC}"
}

# Function to display deployment info
show_deployment_info() {
    echo -e "${BLUE}📊 Deployment Configuration:${NC}"
    echo "  🌐 Server Name: ${SERVER_NAME}"
    echo "  🔌 Proxy Port: ${PROXY_PORT}"
    echo "  🔌 Frontend Port: ${FRONTEND_PORT}"
    echo "  🔧 Backend Host: ${BACKEND_HOST}"
    echo "  🔧 Backend Port: ${BACKEND_PORT}"
    echo "  🗄️  Database Host: ${POSTGRES_HOST}"
    echo "  🗄️  Database Port (Internal): ${POSTGRES_PORT}"
    echo "  🗄️  Database Port (External): ${POSTGRES_PORT_OUT}"
    echo "  📦 Database Name: ${POSTGRES_DB}"
    echo "  👤 Database User: ${POSTGRES_USER}"
    echo "  ⏱️  Proxy Timeout: ${PROXY_TIMEOUT}s"
    echo "  📁 Text Data Path: ${TEXT_DATA_PATH}"
    echo ""
}

# Function to check if services are healthy
check_health() {
    echo -e "${BLUE}🏥 Checking service health...${NC}"
    
    # Wait for services to start
    sleep 10
    
    # Check if containers are running
    if docker compose ps | grep -q "Up"; then
        echo -e "${GREEN}✅ Services are running${NC}"
        
        # Test specific endpoints if available
        if curl -f "http://localhost:${BACKEND_PORT}/api/hello" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend API is responding${NC}"
        else
            echo -e "${YELLOW}⚠️  Backend API not yet ready${NC}"
        fi
        
        if curl -f "http://localhost:${PROXY_PORT}" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend is responding on port ${PROXY_PORT}${NC}"
        else
            echo -e "${YELLOW}⚠️  Frontend not yet ready on port ${PROXY_PORT}${NC}"
        fi
    else
        echo -e "${RED}❌ Some services failed to start${NC}"
        docker compose ps
        exit 1
    fi
}

# Main deployment function
deploy() {
    echo -e "${GREEN}🚀 Starting production deployment...${NC}"
    
    # Load environment variables
    load_env
    
    # Validate environment
    validate_env
    
    # Show deployment info
    show_deployment_info
    
    # Stop existing containers
    echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
    docker compose down
    
    # Clean up old images (optional)
    if [ "${CLEAN_IMAGES:-false}" = "true" ]; then
        echo -e "${YELLOW}🧹 Cleaning up old Docker images...${NC}"
        docker system prune -f
    fi
    
    # Build and start services
    echo -e "${BLUE}🔨 Building and starting services...${NC}"
    docker compose up --build -d
    
    # Check health
    check_health
    
    # Show final status
    echo -e "${GREEN}✅ Deployment complete!${NC}"
    echo -e "${GREEN}🌐 Your application is available at: http://${SERVER_NAME}:${PROXY_PORT}${NC}"
    echo ""
    echo -e "${BLUE}📊 Useful commands:${NC}"
    echo "   📋 Check logs: docker compose logs -f"
    echo "   📊 Check status: docker compose ps"
    echo "   🛑 Stop services: docker compose down"
    echo "   🔄 Restart: docker compose restart"
}

# Script execution
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "status")
        load_env
        echo -e "${BLUE}📊 Current Status:${NC}"
        docker compose ps
        ;;
    "logs")
        docker compose logs -f "${2:-}"
        ;;
    "stop")
        echo -e "${YELLOW}🛑 Stopping all services...${NC}"
        docker compose down
        ;;
    "restart")
        load_env
        echo -e "${YELLOW}🔄 Restarting services...${NC}"
        docker compose restart
        ;;
    *)
        echo "Usage: $0 {deploy|status|logs|stop|restart}"
        echo "  deploy  - Full deployment (default)"
        echo "  status  - Show service status"
        echo "  logs    - Show logs (optionally specify service name)"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        exit 1
        ;;
esac 