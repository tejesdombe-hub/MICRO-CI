#!/usr/bin/env bash
# Start the full Food Delivery platform in Docker
set -e
cd "$(dirname "$0")"

echo "=============================================="
echo " Food Delivery Platform — Docker Startup"
echo "=============================================="

# Stop any locally running Maven services on conflicting ports (optional)
for port in 8080 8081 8082 8083 8084 8085 8086 8087 8088 8761 8888; do
  if command -v lsof >/dev/null 2>&1 && lsof -i :"$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "WARNING: Port $port is in use on the host. Stop local services or change docker-compose ports."
  fi
done

echo ""
echo "Building images (first run may take 10–15 minutes)..."
docker compose build

echo ""
echo "Starting all services..."
docker compose up -d

echo ""
echo "Waiting for core services to become healthy..."
sleep 5
docker compose ps

echo ""
echo "=============================================="
echo " Stack started. Access points:"
echo "   API Gateway:  http://localhost:8080"
echo "   Eureka UI:    http://localhost:8761"
echo "   Config:       http://localhost:8888"
echo "   MySQL:        localhost:3307 (root/root) — port 3307 avoids local MySQL conflict"
echo ""
echo " Useful commands:"
echo "   docker compose logs -f api-gateway"
echo "   docker compose logs -f order-service"
echo "   docker compose ps"
echo "   docker compose down        # stop all"
echo "   docker compose down -v     # stop + delete DB volume"
echo "=============================================="
