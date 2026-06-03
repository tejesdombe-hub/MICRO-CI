# Swagger API Testing Guide

## Inter-service communication (brief)

| Caller | Calls (Feign) | When |
|--------|---------------|------|
| **order-service** | customer-service | `GET /customers/{id}` — validate customer on place order |
| **order-service** | restaurant-service | `GET /restaurants/{id}` — validate restaurant |
| **order-service** | payment-service | `POST /payments/process` — after order saved |
| **order-service** | notification-service | `POST /notifications` — ORDER_PLACED, ORDER_ACCEPTED, ORDER_DELIVERED |
| **order-service** | delivery-partner-service | `POST /delivery-partners/assign` — on assign-delivery |

**No Feign:** auth, menu, customer (when called directly), restaurant (when called directly), payment/notification/delivery (when called directly from Swagger).

Communication is **synchronous HTTP + DTOs only** (no shared entities).

```
You (Swagger) --> API Gateway :8080 --> single service
                      |
Order Service --------+--------> Feign --> other services (internal Docker network)
```

---

## Open Swagger UI

### Option A — All services in one UI (recommended)

**URL:** http://localhost:8080/swagger-ui.html  
(redirects to `/webjars/swagger-ui/index.html` — do **not** use `/swagger-ui/index.html` on the gateway)

Use the dropdown at the top to switch between 8 services.

If the page is blank, wait 2 minutes after `docker compose up -d`, then hard-refresh (Ctrl+F5).

### Option B — Per-service Swagger

| Service | Swagger URL |
|---------|-------------|
| Auth | http://localhost:8081/swagger-ui.html |
| Customer | http://localhost:8082/swagger-ui.html |
| Restaurant | http://localhost:8083/swagger-ui.html |
| Menu | http://localhost:8084/swagger-ui.html |
| Order | http://localhost:8085/swagger-ui.html |
| Delivery | http://localhost:8086/swagger-ui.html |
| Payment | http://localhost:8087/swagger-ui.html |
| Notification | http://localhost:8088/swagger-ui.html |

### Before testing

```bash
cd /home/tejes.dombe/Downloads/MICRO
docker compose build api-gateway auth-service customer-service order-service
docker compose up -d --force-recreate
docker compose ps   # wait until healthy (2–3 min)
```

**Rebuild is required** after Swagger changes — old gateway images do not include SpringDoc.

In each Swagger UI, select server: **API Gateway (use this in Swagger Try it out)** → `http://localhost:8080/api`

---

## Step-by-step test order

Follow this sequence so IDs exist and Feign calls succeed.

### Step 1 — Customer (no Feign)

**Service:** 2. Customer Service  

`POST /customers`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "address": "Mumbai, India"
}
```

**Save `id` from response** → e.g. `customerId = 1`

---

### Step 2 — Auth (no Feign)

**Service:** 1. Auth Service  

`POST /auth/register`

```json
{
  "email": "john@example.com",
  "password": "secret123",
  "role": "CUSTOMER",
  "referenceId": 1
}
```

`POST /auth/login` — same email/password  

**Copy `token`** from response.

For protected endpoints (later): click **Authorize** → paste `Bearer <token>` or just the token (Swagger adds Bearer for Auth service).

---

### Step 3 — Restaurant (no Feign)

**Service:** 3. Restaurant Service  

`POST /restaurants`

```json
{
  "restaurantName": "Pizza Hub",
  "ownerName": "Owner A",
  "address": "Delhi",
  "rating": 4.5
}
```

**Save `id`** → `restaurantId = 1`

---

### Step 4 — Menu (no Feign)

**Service:** 4. Menu Service  

`POST /menus`

```json
{
  "restaurantId": 1,
  "itemName": "Margherita Pizza",
  "description": "Cheese pizza",
  "price": 299.0,
  "availability": true
}
```

---

### Step 5 — Delivery partner (no Feign)

**Service:** 6. Delivery Partner  

`POST /delivery-partners`

```json
{
  "name": "Rider One",
  "phone": "9123456789",
  "vehicleNumber": "MH01AB1234",
  "availabilityStatus": true
}
```

**Save partner `id`** → e.g. `1`

---

### Step 6 — Place order (triggers Feign)

**Service:** 5. Order Service (Feign)

`POST /orders`

```json
{
  "customerId": 1,
  "restaurantId": 1,
  "totalAmount": 499.0,
  "paymentMethod": "UPI"
}
```

**What happens internally:**

1. Feign → customer-service (validate)
2. Feign → restaurant-service (validate)
3. Saves order
4. Feign → payment-service (SUCCESS)
5. Feign → notification-service (2 messages)

**Verify Feign worked:**

```bash
docker compose logs order-service --tail 30
docker compose logs payment-service --tail 20
docker compose logs notification-service --tail 20
```

`GET /payments/order/{orderId}` on Payment service — should show payment.

`GET /notifications/user/1` on Notification — should list notifications.

---

### Step 7 — Assign delivery (Feign)

**Service:** 5. Order Service  

`POST /orders/1/assign-delivery`

Feign → delivery-partner-service assign.

Check:

```bash
docker compose logs delivery-partner-service --tail 15
```

---

### Step 8 — Update delivery status (direct)

**Service:** 6. Delivery Partner  

`PATCH /delivery-partners/1/status`

```json
{
  "deliveryStatus": "PICKED_UP"
}
```

Repeat with: `OUT_FOR_DELIVERY`, then `DELIVERED`.

---

### Step 9 — Mark order delivered (notification Feign)

**Service:** 5. Order Service  

`PATCH /orders/1/status`

```json
{
  "orderStatus": "DELIVERED"
}
```

Feign → notification-service (ORDER_DELIVERED).

---

## Quick reference — all endpoints

| # | Method | Gateway path | Feign? |
|---|--------|--------------|--------|
| 1 | POST | /api/auth/register | No |
| 2 | POST | /api/auth/login | No |
| 3 | POST | /api/customers | No |
| 4 | GET | /api/customers/{id} | Used by Order |
| 5 | POST | /api/restaurants | No |
| 6 | GET | /api/restaurants/{id} | Used by Order |
| 7 | POST | /api/menus | No |
| 8 | GET | /api/menus/restaurant/{id} | No |
| 9 | POST | /api/delivery-partners | No |
| 10 | POST | /api/delivery-partners/assign | Used by Order |
| 11 | PATCH | /api/delivery-partners/{id}/status | No |
| 12 | POST | /api/orders | **Yes** (4 services) |
| 13 | GET | /api/orders/{id} | No |
| 14 | POST | /api/orders/{id}/assign-delivery | **Yes** |
| 15 | PATCH | /api/orders/{id}/status | **Yes** (if DELIVERED) |
| 16 | POST | /api/payments/process | Used by Order |
| 17 | GET | /api/payments/order/{orderId} | No |
| 18 | POST | /api/notifications | Used by Order |
| 19 | GET | /api/notifications/user/{userId} | No |

---

## Rebuild after Swagger changes

```bash
docker compose build api-gateway auth-service customer-service order-service
docker compose up -d
```

Open: http://localhost:8080/swagger-ui.html

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Swagger empty / failed to load | Wait 2 min; refresh config: `docker compose restart config-server api-gateway` |
| 404 on Try it out | Server must be **API Gateway** `http://localhost:8080/api` |
| Order fails 500 | Run steps 1–3 first; check `docker compose logs order-service` |
| Feign connection refused | `docker compose ps` — all services Up; check Eureka http://localhost:8761 |

---

## Eureka check

http://localhost:8761 — you should see all services **UP** before heavy testing.
