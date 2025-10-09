#!/bin/bash

# Risko Platform Deployment Script
set -e

echo "🚀 Risko Platform Deployment Starting..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    log_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Environment selection
ENVIRONMENT=${1:-development}

if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Deploying to PRODUCTION environment"
    COMPOSE_FILE="docker-compose.prod.yml"
    
    # Check for required environment variables
    if [ ! -f "backend/.env" ]; then
        log_error "Production .env file not found. Please create backend/.env with production settings."
        exit 1
    fi
    
    # Check for SSL certificates
    if [ ! -d "ssl" ]; then
        log_warning "SSL certificates not found. Creating self-signed certificates for testing..."
        mkdir -p ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=TR/ST=Istanbul/L=Istanbul/O=Risko/CN=risko.local"
    fi
    
elif [ "$ENVIRONMENT" = "development" ]; then
    log_info "Deploying to DEVELOPMENT environment"
    COMPOSE_FILE="docker-compose.dev.yml"
else
    log_error "Invalid environment: $ENVIRONMENT. Use 'development' or 'production'"
    exit 1
fi

# Build and start services
log_info "Building and starting Docker containers..."
docker-compose -f $COMPOSE_FILE down --remove-orphans
docker-compose -f $COMPOSE_FILE build --no-cache
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
log_info "Waiting for services to be ready..."
sleep 10

# Health check
log_info "Performing health check..."
if [ "$ENVIRONMENT" = "production" ]; then
    HEALTH_URL="https://localhost/health"
else
    HEALTH_URL="http://localhost:8000/health"
fi

# Retry health check
for i in {1..30}; do
    if curl -f -s $HEALTH_URL > /dev/null 2>&1; then
        log_info "✅ Health check passed!"
        break
    elif [ $i -eq 30 ]; then
        log_error "❌ Health check failed after 30 attempts"
        log_error "Deployment might have issues. Check logs with: docker-compose -f $COMPOSE_FILE logs"
        exit 1
    else
        log_warning "Health check attempt $i/30 failed, retrying..."
        sleep 2
    fi
done

# Display service status
log_info "Service Status:"
docker-compose -f $COMPOSE_FILE ps

# Display access information
echo ""
log_info "🎉 Deployment completed successfully!"
echo ""
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🌐 API URL: https://localhost"
    echo "📚 API Documentation: https://localhost/docs"
    echo "❤️  Health Check: https://localhost/health"
else
    echo "🌐 API URL: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "❤️  Health Check: http://localhost:8000/health"
fi

echo ""
echo "📋 Useful Commands:"
echo "  View logs:        docker-compose -f $COMPOSE_FILE logs -f"
echo "  Stop services:    docker-compose -f $COMPOSE_FILE down"
echo "  Restart services: docker-compose -f $COMPOSE_FILE restart"
echo "  Update services:  docker-compose -f $COMPOSE_FILE pull && docker-compose -f $COMPOSE_FILE up -d"

echo ""
log_info "Example API Usage:"
if [ "$ENVIRONMENT" = "production" ]; then
    echo 'curl -X POST "https://localhost/api/v1/risk/analyze" -H "Content-Type: application/json" -d "{\"address\": \"Istanbul, Turkey\"}"'
else
    echo 'curl -X POST "http://localhost:8000/api/v1/risk/analyze" -H "Content-Type: application/json" -d "{\"address\": \"Istanbul, Turkey\"}"'
fi

log_info "Deployment completed! 🚀"