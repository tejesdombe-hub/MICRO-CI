# Running All Services with Docker

This guide runs the **entire platform in Docker** so you avoid port conflicts with locally started Maven/IDE services.

## Why Docker fixes port conflicts

| Approach | Problem |
|----------|---------|
| Run 11 services locally | Ports 8080–8088, 8761, 8888, 3306 all on host — easy to clash |
| **Docker Compose** | Only **8080, 8761, 8888, 3306** exposed on host; other services use internal network only |

## Prerequisites

- Docker Engine 20+
- Docker Compose v2 (`docker compose`)
- **8 GB+ RAM** recommended (11 JVMs)
- Stop any local instances using ports 8080, 8761, 8888
- Local MySQL on 3306 is OK — Docker MySQL uses host port **3307** to avoid conflict

## Quick start (3 commands)

```bash
cd /home/tejes.dombe/Downloads/MICRO

chmod +x docker-start.sh
./docker-start.sh
```

Or manually:

```bash
docker compose build
docker compose up -d
```

First build downloads Maven dependencies and compiles all modules (**10–15 min**). Later starts are faster.

## What gets started

| Container | Host port | Internal only |
|-----------|-----------|---------------|
| fd-mysql | **3307** (maps to 3306 inside Docker) | — |
| fd-discovery | 8761 | — |
| fd-config | 8888 | — |
| fd-gateway | **8080** | — |
| fd-auth | — | ✓ |
| fd-customer | — | ✓ |
| fd-restaurant | — | ✓ |
| fd-menu | — | ✓ |
| fd-order | — | ✓ |
| fd-delivery | — | ✓ |
| fd-payment | — | ✓ |
| fd-notification | — | ✓ |

## Startup order (automatic)

1. MySQL (healthy)
2. Eureka discovery-server (healthy)
3. Config server (healthy, mounts `config-repo/`)
4. All business services (parallel)
5. API Gateway (last)

## Test the APIs

All requests go through the gateway:

```bash
# Create customer
curl -s -X POST http://localhost:8080/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@mail.com","phone":"9876543210","address":"Mumbai"}'

# Register auth
curl -s -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"john@mail.com","password":"secret1","role":"CUSTOMER","referenceId":1}'

# Place order (after creating restaurant id=1)
curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId":1,"restaurantId":1,"totalAmount":499.0,"paymentMethod":"UPI"}'
```

## Useful commands

```bash
# Status of all containers
docker compose ps

# Logs for one service
docker compose logs -f order-service
docker compose logs -f api-gateway

# Restart one service
docker compose restart order-service

# Stop everything
docker compose down

# Stop and remove database volume (fresh DB)
docker compose down -v
```

## Troubleshooting

### Port already in use

```bash
# Find what uses port 8080
sudo lsof -i :8080

# Stop local Spring Boot runs in IDE/terminal, then:
docker compose down
docker compose up -d
```

### Service not registering in Eureka

Wait 2–3 minutes after `up -d`, then open http://localhost:8761

```bash
docker compose logs config-server
docker compose logs auth-service
```

### Config server unhealthy

```bash
docker compose logs config-server
curl http://localhost:8888/actuator/health
```

### Out of memory

Increase Docker Desktop memory to 8 GB, or start infrastructure only:

```bash
docker compose up -d mysql discovery-server config-server
# then add services one by one
```

### Rebuild after code changes

```bash
docker compose build --no-cache auth-service
docker compose up -d auth-service
```

## Do not mix Docker + local Maven

| Do this | Avoid this |
|---------|------------|
| `docker compose up -d` for everything | Running `mvn spring-boot:run` on host while Docker uses same ports |
| Use only http://localhost:8080 | Starting api-gateway locally on 8080 while Docker gateway runs |

## Configuration

- Docker profile: `config-repo/application-docker.yml` (Eureka → `discovery-server`)
- Per-service DB URLs set via environment in `docker-compose.yml`
- MySQL init script: `docker/mysql/init-databases.sql`

## Files added for Docker

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage build for any module |
| `docker-compose.yml` | Full stack orchestration |
| `docker-start.sh` | One-command startup |
| `.dockerignore` | Faster builds |
| `config-repo/application-docker.yml` | Docker hostnames |
