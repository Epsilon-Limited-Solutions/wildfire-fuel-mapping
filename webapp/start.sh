#!/bin/bash

# Wildfire Fuel Mapping WebApp Startup Script

set -e

echo "🔥 Wildfire Fuel Mapping WebApp"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"
echo -e "${GREEN}✓ Docker Compose is installed${NC}"
echo ""

# Check if data exists
if [ ! -d "../data/processed" ] || [ -z "$(ls -A ../data/processed)" ]; then
    echo -e "${YELLOW}⚠️  Warning: No processed data found${NC}"
    echo "Run the pipeline first: cd .. && python run.py --step all"
    echo ""
fi

# Check if maps exist
if [ ! -d "../outputs/maps" ] || [ -z "$(ls -A ../outputs/maps 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠️  Warning: No maps found${NC}"
    echo "Generate maps: cd .. && python run.py --step map"
    echo ""
fi

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true
echo ""

# Build and start
echo "Building and starting webapp..."
echo ""
docker-compose up --build -d

# Wait for container to be healthy
echo ""
echo "Waiting for webapp to start..."
sleep 5

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✅ WebApp is running!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "🌐 Open your browser to: http://localhost:5000"
    echo ""
    echo "Commands:"
    echo "  View logs:    docker-compose logs -f"
    echo "  Stop:         docker-compose down"
    echo "  Restart:      docker-compose restart"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Failed to start webapp${NC}"
    echo "Check logs: docker-compose logs"
    exit 1
fi
