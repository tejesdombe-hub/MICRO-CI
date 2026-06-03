# AI Engineering Skill: Food Delivery Microservices Platform
# (Zomato / Swiggy Style — Java 17 + Spring Boot 3)

--
Always:

- use Java 17
- use Spring Boot 3
- use layered architecture
- use DTO pattern
- use constructor injection
- use validation annotations
- use ResponseEntity
- use global exception handling
- use clean code principles
- generate production-ready code

## Trigger Condition
Load this skill when:
- Creating or editing any file inside any service of this project
- Adding a new microservice to the platform
- Writing Feign clients, DTOs, mappers, entities, or security config
- Reviewing or refactoring any existing service

Do NOT apply this skill to: frontend code, shell scripts, CI/CD YAML, or infrastructure files.

---

## Project Identity

```
Platform     : FoodFlow — Food Delivery Backend
Style        : Zomato / Swiggy
Architecture : Microservices (Spring Cloud)
Language     : Java 17
Framework    : Spring Boot 3.x (Jakarta namespaces — NOT javax)
Build        : Maven (multi-module)
Database     : MySQL 8.x per service (Database-per-Service pattern)
Auth         : JWT (stateless) — Spring Security 6.x filter chain
Registry     : Netflix Eureka
Gateway      : Spring Cloud Gateway
Config       : Spring Cloud Config Server
HTTP Client  : OpenFeign (declarative, DTO-only)
Docs         : SpringDoc OpenAPI 3 (Swagger UI per service)
Boilerplate  : Lombok — constructors only (@RequiredArgsConstructor)
```

---

## Microservice Inventory

| Service              | Port  | Role                                      |
|----------------------|-------|-------------------------------------------|
| config-server        | 8888  | Centralized config source                 |
| eureka-server        | 8761  | Service registry                          |
| api-gateway          | 8080  | Entry point, routing, JWT pre-filter      |
| auth-service         | 8081  | Registration, login, JWT issuance         |
| customer-service     | 8082  | Customer profile management               |
| restaurant-service   | 8083  | Restaurant + owner management             |
| menu-service         | 8084  | Menu items per restaurant                 |
| order-service        | 8085  | Order lifecycle orchestration             |
| delivery-service     | 8086  | Partner management, delivery tracking     |
| payment-service      | 8087  | Payment processing simulation             |
| notification-service | 8088  | Notification persistence                  |

---

## Master Package Layout

Every service follows this structure exactly.
Replace `com.foodflow` with the actual base and `<service>` with the service name.

```
com.foodflow.<service>/
├── controller/          HTTP layer only — no logic
├── service/             Interface definitions
├── service/impl/        Business logic lives here
├── repository/          JPA repositories
├── entity/              JPA entities — never exposed outside service
├── dto/
│   ├── request/         XxxRequestDto — inbound API payloads
│   └── response/        XxxResponseDto — outbound API payloads
├── mapper/              Entity ↔ DTO conversions
├── exception/           ResourceNotFoundException, GlobalExceptionHandler
├── security/            JWT filter, SecurityConfig, UserDetailsService
├── config/              Feign config, OpenAPI config, app config beans
└── client/              Feign client interfaces (calls to other services)
```

**Exception**: `config-server`, `eureka-server`, `api-gateway` have no entity/service/repository/dto layers.
They contain only configuration classes.

---

## Non-Negotiable Hard Rules

### Architecture

1. Controllers are HTTP translators only. They parse the request, call one service method, return ResponseEntity. Zero business logic.
2. Business logic belongs exclusively in `service/impl/`. If a controller method does more than call a service, it is wrong.
3. JPA Entities NEVER leave their own service. No entity class is shared between services, referenced in a Feign client, or returned from a controller.
4. Services communicate ONLY through DTOs via Feign clients. No shared entity libraries. No direct DB access across services.
5. Each service owns its own database schema. Service A never queries Service B's database.
6. Mappers perform shape conversion only. No business logic, no database calls, no conditional branching inside a mapper.
7. Constructor injection always. Never `@Autowired` on a field. Never setter injection.

### Security

8. JWT tokens carry: `sub` (email), `role` (single role string), `userId` (Long), `referenceId` (Long — customerId / restaurantId / partnerId).
9. JWT validation happens at the API Gateway only. Individual services trust the forwarded headers — they do NOT re-validate the token.
10. The API Gateway forwards three headers downstream after validation:
    - `X-Auth-User-Id` — the userId from the token
    - `X-Auth-User-Role` — the role string
    - `X-Auth-Reference-Id` — the domain-specific ID
11. Individual services read identity from these headers, not from re-parsing a token.
12. BCrypt is the only password encoder. Never store or log plain-text passwords.
13. Role hierarchy: ADMIN > RESTAURANT_OWNER > CUSTOMER > DELIVERY_PARTNER. Enforce at method level with `@PreAuthorize`.

### Database

14. `spring.jpa.hibernate.ddl-auto=update` for development only. Production uses explicit migration scripts.
15. All entity primary keys use `@GeneratedValue(strategy = GenerationType.IDENTITY)`.
16. Unique constraints are declared both at the JPA level (`@Column(unique = true)`) and at the DB level (enforced by schema).
17. `@Transactional(readOnly = true)` on all read-only service methods. `@Transactional` on all write methods.

### HTTP & API

18. Every controller method returns `ResponseEntity<ApiResponse<T>>`. Never return a raw object, a plain String, or void.
19. Validation: every RequestDto must have Jakarta Validation annotations. Every controller endpoint receiving a body must use `@Valid`.
20. Pagination is required on all list endpoints. Default: `page=0, size=10, sort=id,asc`. Max size=50 — reject requests above this.
21. API versioning prefix: `/api/v1/` on all endpoints.

### Logging

22. Use SLF4J only. Never `System.out.println`.
23. Log at INFO at the start and end of every service method: what was called and with what ID.
24. Log at ERROR in every catch block with the full exception.
25. NEVER log: passwords, JWT tokens, full card numbers, or any PII (email and phone log only the first 3 chars + `***`).

---

## Universal Response Envelope

Every API response — success or error — uses this exact shape. No exceptions.

```json
// Success
{
  "success": true,
  "message": "Customer retrieved successfully",
  "data": { ... },
  "timestamp": "2024-01-15T10:30:00Z"
}

// Error
{
  "success": false,
  "message": "Customer not found with id: 42",
  "data": null,
  "timestamp": "2024-01-15T10:30:00Z",
  "errors": ["field: validation message"]   // populated for 400 only
}
```

Java class — lives in each service (no shared library for this):

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    private String timestamp;
    private List<String> errors;

    public static <T> ApiResponse<T> success(String message, T data) {
        return ApiResponse.<T>builder()
                .success(true).message(message).data(data)
                .timestamp(Instant.now().toString()).build();
    }

    public static <T> ApiResponse<T> error(String message, List<String> errors) {
        return ApiResponse.<T>builder()
                .success(false).message(message).errors(errors)
                .timestamp(Instant.now().toString()).build();
    }
}
```

---

## HTTP Status Code Contract

| Situation                        | Code |
|----------------------------------|------|
| Resource created                 | 201  |
| Successful read / update         | 200  |
| Successful delete                | 204  |
| Validation failure               | 400  |
| Missing / invalid JWT            | 401  |
| Valid JWT but insufficient role  | 403  |
| Resource not found               | 404  |
| Duplicate unique field           | 409  |
| Unexpected server error          | 500  |

---

## Exception Handling

Every service defines these three classes — no shared library.

```
exception/
├── ResourceNotFoundException.java   (404)
├── InvalidRequestException.java     (400)
├── UnauthorizedException.java       (403)
└── GlobalExceptionHandler.java      (@RestControllerAdvice)
```

`GlobalExceptionHandler` must handle:
- `ResourceNotFoundException` → 404
- `InvalidRequestException` → 400
- `MethodArgumentNotValidException` → 400 + list all field errors
- `UnauthorizedException` → 403
- `Exception` (catch-all) → 500

NEVER let a stack trace reach the API response in any environment.
NEVER swallow an exception with an empty catch block.

---

## Naming Conventions

| Artifact         | Convention                              | Example                        |
|------------------|-----------------------------------------|--------------------------------|
| Entity           | Singular PascalCase                     | `Customer`, `MenuItem`         |
| Table            | Plural snake_case                       | `customers`, `menu_items`      |
| RequestDto       | `<Entity>RequestDto`                    | `CustomerRequestDto`           |
| ResponseDto      | `<Entity>ResponseDto`                   | `CustomerResponseDto`          |
| Repository       | `<Entity>Repository`                    | `CustomerRepository`           |
| Service iface    | `<Entity>Service`                       | `CustomerService`              |
| Service impl     | `<Entity>ServiceImpl`                   | `CustomerServiceImpl`          |
| Mapper           | `<Entity>Mapper`                        | `CustomerMapper`               |
| Feign client     | `<TargetService>Client`                 | `OrderServiceClient`           |
| Controller       | `<Entity>Controller`                    | `CustomerController`           |
| Service methods  | `save`, `getById`, `getAll`, `update`, `delete` | `saveCustomer`, `getCustomerById` |
| Endpoint paths   | Plural kebab-case nouns                 | `/api/v1/customers`            |

---

## Feign Client Rules

1. Every Feign client interface lives in the CALLING service's `client/` package.
2. Feign clients pass only DTOs — never entities, never raw Maps.
3. Every Feign client must have a fallback class implementing it.
4. The `@FeignClient` annotation must declare both `name` (Eureka service name) and `fallback`.
5. Feign clients forward the JWT header using a `RequestInterceptor` config bean.
6. If a Feign call fails, classify the failure in the calling service — do NOT bubble up raw Feign exceptions to the controller.

```java
// Pattern — every Feign client looks like this:
@FeignClient(
        name = "customer-service",
        fallback = CustomerServiceClientFallback.class
)
public interface CustomerServiceClient {
    @GetMapping("/api/v1/customers/{id}")
    ApiResponse<CustomerResponseDto> getCustomerById(@PathVariable Long id);
}
```

---

## JWT Token Contract

```
Claims:
  sub         = user email (String)
  role        = "ROLE_CUSTOMER" | "ROLE_ADMIN" | "ROLE_RESTAURANT_OWNER" | "ROLE_DELIVERY_PARTNER"
  userId      = Long (maps to auth_users table)
  referenceId = Long (customerId / restaurantId / partnerId — 0 for ADMIN)
  iat         = issued at
  exp         = expiry (configurable, default 24h)

Header forwarded by Gateway:
  X-Auth-User-Id       : userId value
  X-Auth-User-Role     : role value
  X-Auth-Reference-Id  : referenceId value
```

Auth service generates tokens. All other services read identity from headers only.

---

## Order Status State Machine

Transitions are enforced in `OrderServiceImpl`. Any attempt to move to an invalid next state throws `InvalidRequestException`.

```
PLACED → CONFIRMED → PREPARING → READY_FOR_PICKUP
                                → PICKED_UP → OUT_FOR_DELIVERY → DELIVERED
                                                               → DELIVERY_FAILED
       → CANCELLED  (only from PLACED or CONFIRMED)
```

**Rules:**
- Once DELIVERED or CANCELLED, the order is frozen — no further transitions allowed.
- Only RESTAURANT_OWNER can move PLACED → CONFIRMED → PREPARING → READY_FOR_PICKUP.
- Only DELIVERY_PARTNER can move PICKED_UP → OUT_FOR_DELIVERY → DELIVERED / DELIVERY_FAILED.
- Only CUSTOMER or ADMIN can move to CANCELLED (from PLACED or CONFIRMED only).

---

## Delivery Status State Machine

```
ASSIGNED → PICKED_UP → OUT_FOR_DELIVERY → DELIVERED
                                        → DELIVERY_FAILED → REASSIGNED
```

- Only the assigned DELIVERY_PARTNER can update their own delivery status.
- ADMIN can override any status.

---

## Payment Status Contract

```
PENDING → SUCCESS
        → FAILED
        → REFUNDED  (only from SUCCESS, only by ADMIN)
```

Payment is simulated — no real gateway. On order placement, payment is created as PENDING.
The Order service calls Payment service to confirm — Payment service randomly marks SUCCESS or FAILED (for simulation).

---

## Service Responsibility Map

| Service              | Owns                                         | NEVER does                                              |
|----------------------|----------------------------------------------|---------------------------------------------------------|
| auth-service         | User credentials, JWT issuance, roles        | Customer profiles, business data                        |
| customer-service     | Customer profile CRUD                        | Auth, orders, payments                                  |
| restaurant-service   | Restaurant + owner profile                   | Menu items (delegates to menu-service)                  |
| menu-service         | Menu items per restaurant                    | Orders, pricing rules outside menu                      |
| order-service        | Order lifecycle orchestration                | Direct DB access to other services                      |
| delivery-service     | Partner profiles, delivery status            | Payment, notifications                                  |
| payment-service      | Payment record, status simulation            | Order status updates (returns result, order-service acts)|
| notification-service | Persist notifications, expose status         | Actually send emails/SMS (out of scope)                 |
| api-gateway          | JWT validation, routing, rate limiting       | Business logic                                          |
| eureka-server        | Service registry only                        | Business logic                                          |
| config-server        | Externalized config files only               | Business logic                                          |

---

## Order Service — Orchestration Flow

Order service is the most complex. It orchestrates synchronously via Feign in this order:

```
1. Receive OrderRequestDto from Customer (via Gateway)
2. Validate customerId   → call customer-service  → GET /api/v1/customers/{id}
3. Validate restaurantId → call restaurant-service → GET /api/v1/restaurants/{id}
4. Validate menu items   → call menu-service       → POST /api/v1/menu/validate (list of itemIds)
5. Calculate total amount (done locally in OrderServiceImpl — not delegated)
6. Persist order with status PLACED
7. Initiate payment      → call payment-service    → POST /api/v1/payments
8. On payment SUCCESS: keep status PLACED, trigger notification
9. On payment FAILED:  set status CANCELLED, trigger notification
10. Trigger notification → call notification-service → POST /api/v1/notifications
```

NEVER call payment-service from inside a @Transactional block that also persists the order.
Reason: if payment call hangs, the transaction holds a DB lock. Persist order first, commit, then call payment.

---

## Notification Service Contract

Notifications are fire-and-forget from the Order service.
The Notification service only persists — it does NOT send emails/SMS.

```java
// NotificationRequestDto
{
        "recipientId"   : Long,
        "recipientRole" : "CUSTOMER" | "RESTAURANT_OWNER" | "DELIVERY_PARTNER",
        "type"          : "ORDER_PLACED" | "ORDER_CONFIRMED" | "ORDER_DELIVERED" | "PAYMENT_SUCCESS" | "PAYMENT_FAILED",
        "message"       : String,
        "referenceId"   : Long   // orderId
}

// Notification entity status: PENDING → SENT (updated by future email worker)
```

---

## Mapper Rules

Each mapper has exactly these three methods — no more, no less unless a new use case is explicitly justified:

```java
public XxxResponseDto mapToResponseDto(Xxx entity);
public Xxx mapToEntity(XxxRequestDto dto);
public void updateEntity(XxxRequestDto dto, Xxx entity);  // for PUT operations
```

Mappers are `@Component` classes. Manual mapping preferred for clarity.
MapStruct is allowed if the team decides — but the method signatures above are non-negotiable.
NEVER use `BeanUtils.copyProperties` — it is type-unsafe and silently skips mismatched fields.

---

## Required Files Per Service (Minimum)

Every service (except infra services) MUST generate all of these before being considered done:

```
controller/         XxxController.java
service/            XxxService.java  (interface)
service/impl/       XxxServiceImpl.java
repository/         XxxRepository.java
entity/             Xxx.java
dto/request/        XxxRequestDto.java
dto/response/       XxxResponseDto.java
mapper/             XxxMapper.java
exception/          ResourceNotFoundException.java
exception/          GlobalExceptionHandler.java
security/           SecurityConfig.java
security/           JwtAuthFilter.java
config/             OpenApiConfig.java
resources/          application.yml  (pulls from config-server)
```

---

## Eureka Client Configuration (every business service)

```yaml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    fetch-registry: true
    register-with-eureka: true
  instance:
    prefer-ip-address: true
```

`spring.application.name` is the Eureka service name.
It MUST match exactly the `name` in `@FeignClient` annotations that call this service.

---

## Config Server Usage

Every business service has only this in its local `application.yml`:

```yaml
spring:
  application:
    name: customer-service
  config:
    import: "configserver:http://localhost:8888"
```

All other config (datasource, JWT secret, Eureka URL, Feign timeouts) lives in the Config Server's Git repo.
NEVER hardcode database credentials, JWT secrets, or service URLs in local properties.

---

## Validation Rules Per Entity

```
Customer:   name (notBlank), email (notBlank + @Email + unique), phone (pattern: 10 digits), address (notBlank)
Restaurant: restaurantName (notBlank), ownerName (notBlank), address (notBlank), rating (0.0–5.0)
MenuItem:   itemName (notBlank), price (@Positive), restaurantId (notNull)
Order:      customerId (notNull), restaurantId (notNull), items (notEmpty), deliveryAddress (notBlank)
Payment:    orderId (notNull), amount (@Positive), paymentMethod (notBlank)
DeliveryPartner: name (notBlank), phone (pattern: 10 digits), vehicleNumber (notBlank)
```

---

## Testing Requirements

| Layer              | Tool                   | Minimum coverage                              |
|--------------------|------------------------|-----------------------------------------------|
| Service (unit)     | JUnit 5 + Mockito      | Every public method: happy path + failure path|
| Controller (integ) | @SpringBootTest + MockMvc | Every endpoint: 200/201/400/404 cases      |
| Repository         | @DataJpaTest           | Custom query methods only                     |
| Feign clients      | WireMock               | Happy path + service-unavailable fallback     |

Test class naming: `XxxServiceImplTest`, `XxxControllerIntegrationTest`.
Test method naming: `should<ExpectedBehaviour>_when<Condition>` — e.g., `shouldThrowNotFoundException_whenCustomerDoesNotExist`.

---

## Anti-Patterns — NEVER Generate These

```
NEVER return a JPA entity from a controller or Feign client method.
NEVER use @Autowired field injection anywhere in the codebase.
NEVER call another service's database table directly.
NEVER put business logic (calculations, state checks, validations) in a controller.
NEVER put database queries in a controller or mapper.
NEVER share entity classes between services via a common library.
NEVER catch generic Exception and swallow it silently.
NEVER log the full JWT token, password, or raw PII.
NEVER use ddl-auto=create or create-drop outside a test context.
NEVER use BeanUtils.copyProperties for mapping.
NEVER allow an illegal order/delivery status transition — always validate the current state before updating.
NEVER call payment-service from inside the same @Transactional block that persists the order.
NEVER hardcode secrets, passwords, or service URLs in source code.
NEVER use @RequestParam for complex filter objects — use @ModelAttribute or a filter DTO.
```

---

## Code Review Checklist (AI must self-check before finalizing output)

- [ ] Every controller method returns `ResponseEntity<ApiResponse<T>>`
- [ ] Every service impl method has `@Transactional` or `@Transactional(readOnly=true)`
- [ ] Every RequestDto has Jakarta Validation annotations
- [ ] Every controller endpoint has `@Valid` on `@RequestBody`
- [ ] No entity class appears in any controller method signature or Feign client interface
- [ ] No `@Autowired` field injection anywhere
- [ ] JWT filter reads from header — not re-parsing token in business service
- [ ] State transitions validated before update (Order, Delivery)
- [ ] GlobalExceptionHandler handles all 5 required exception types
- [ ] Logging present at start/end of every service method
- [ ] Swagger `@Operation` annotation on every controller method
- [ ] Feign client has a fallback class
- [ ] No credentials or secrets in application.yml (must come from config-server)
- [ ] Mapper uses only the 3 defined method signatures

---

## Acceptance Criteria (definition of done for any feature)

1. `mvn clean compile` passes with zero errors
2. All unit tests pass
3. All integration tests pass
4. Endpoints return correct status codes per the HTTP contract table
5. Invalid payloads return 400 with field-level error list
6. Missing resources return 404 with the standard envelope
7. No JPA entity in any API response
8. Service registers correctly with Eureka
9. Swagger UI accessible at `/swagger-ui.html`
10. No hardcoded credentials in any file

---

## Resilience Patterns in Microservices Architecture

### What is Resilience in Microservices Architecture

Resilience is the ability of a system to continue functioning correctly even when some of its components fail or experience degraded performance. In microservices architecture, resilience is critical because:

- Services are distributed and communicate over the network
- Each service has its own failure domain
- A single service failure can cascade to dependent services
- Network latency and timeouts are inherent in distributed systems

Resilience patterns protect the system from:
- Service unavailability (down services)
- High latency (slow services)
- Network failures
- Resource exhaustion (thread pools, connections)

### Problems Caused by Cascading Failures

Cascading failures occur when a failure in one service triggers failures in dependent services, creating a domino effect that can bring down the entire system:

```
Example Scenario:
Payment Service slows down → Order Service threads block waiting
→ Order Service thread pool exhausts → API Gateway requests timeout
→ Customer retries → More requests flood the system
→ All services become unresponsive → System-wide outage
```

**Common cascading failure patterns:**
- Thread pool exhaustion from blocked calls
- Connection pool depletion from waiting connections
- Memory exhaustion from queued requests
- Database lock contention from long-running transactions
- Retry storms amplifying traffic to failing services

### What Happens When a Dependent Service is Slow or Down

**When a service is DOWN:**
- Connection attempts timeout
- Feign clients throw `ConnectException` or `SocketTimeoutException`
- Calling service experiences increased latency
- If no timeout is set, threads block indefinitely
- Thread pool fills up, rejecting new requests

**When a service is SLOW:**
- Requests complete but with high latency
- Response times exceed configured timeouts
- Backpressure builds up in calling services
- Resource pools (threads, connections) get exhausted
- User experience degrades across the system

**Impact on FoodFlow platform:**
- Order Service calling slow Payment Service → orders hang
- Restaurant Service calling slow Menu Service → menu loading fails
- Delivery Service calling slow Notification Service → delivery updates delayed

### Introduction to Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by detecting when a dependent service is failing and temporarily blocking calls to it, similar to an electrical circuit breaker that trips when there's a fault.

**Key benefits:**
- Fast failure when a service is known to be down
- Prevents resource exhaustion on the calling side
- Allows the failing service time to recover
- Provides fallback behavior for users

**How it works:**
1. Monitor calls to a dependent service
2. Count failures over a sliding time window
3. When failure threshold is reached, "trip" the circuit (OPEN state)
4. Block all calls immediately (fail fast)
5. After a wait duration, attempt a single call (HALF-OPEN state)
6. If successful, reset to CLOSED; if failed, stay OPEN

### How Circuit Breaker Prevents System-Wide Failures

```
Without Circuit Breaker:
Order Service → Payment Service (slow/down)
├─ Thread 1: waiting... (blocked)
├─ Thread 2: waiting... (blocked)
├─ Thread 3: waiting... (blocked)
└─ Thread pool exhausted → all new requests rejected

With Circuit Breaker:
Order Service → Payment Service (circuit OPEN)
├─ Thread 1: CircuitBreakerOpenException (immediate)
├─ Thread 2: CircuitBreakerOpenException (immediate)
├─ Thread 3: CircuitBreakerOpenException (immediate)
└─ Fallback: "Payment unavailable, try later" (graceful degradation)
```

**Protection mechanisms:**
- Immediate failure instead of waiting
- Resource conservation (threads, connections)
- Graceful degradation via fallbacks
- Automatic recovery detection

### States of Circuit Breaker: CLOSED, OPEN, HALF-OPEN

**CLOSED State (Normal Operation):**
- Circuit allows all requests to pass through
- Failure rate is monitored but below threshold
- Each failed request increments failure counter
- Successful requests reset failure counter
- Example: Payment Service responding normally

**OPEN State (Circuit Tripped):**
- All requests are blocked immediately
- No actual calls to the dependent service
- `CircuitBreakerOpenException` thrown for each call
- Fallback methods are invoked
- Wait duration timer starts (e.g., 60 seconds)
- Example: Payment Service down, circuit tripped after 50% failure rate

**HALF-OPEN State (Recovery Attempt):**
- After wait duration expires, circuit transitions to HALF-OPEN
- Allows a single request through to test if service recovered
- If request succeeds → transition to CLOSED (circuit reset)
- If request fails → transition back to OPEN (wait duration restarts)
- Example: Testing if Payment Service recovered after outage

### Difference Between Retry and Circuit Breaker

| Aspect               | Retry Pattern                          | Circuit Breaker Pattern               |
|----------------------|----------------------------------------|---------------------------------------|
| Purpose              | Handle transient failures              | Prevent cascading failures            |
| When to use          | Network glitches, temporary timeouts  | Service down, persistent failures     |
| Behavior             | Re-attempt the same request            | Block requests to failing service     |
| Resource usage       | Increases load (more requests)        | Decreases load (blocks requests)      |
| Failure handling     | Hope it works next time                | Accept failure, use fallback          |
| Example scenario     | Payment gateway timeout (retry once)   | Payment service down (stop calling)   |

**When to use together:**
- Retry first for transient failures (1-3 attempts)
- Circuit Breaker trips if retries consistently fail
- This combination handles both temporary and persistent failures

### Introduction to Resilience4j

Resilience4j is a fault tolerance library for Java that implements several resilience patterns:

- **Circuit Breaker**: Prevent cascading failures
- **Retry**: Handle transient failures
- **Rate Limiter**: Control request rate
- **Bulkhead**: Limit concurrent calls
- **Time Limiter**: Cancel long-running operations
- **Cache**: Cache responses to reduce load

**Why Resilience4j over Hystrix:**
- Active maintenance (Hystrix is in maintenance mode)
- Java 8+ compatibility
- Modular design (use only what you need)
- Better performance
- Reactive programming support

**Integration with Spring Boot:**
```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
    <version>2.1.0</version>
</dependency>
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-feign</artifactId>
    <version>2.1.0</version>
</dependency>
```

### Configuring Failure Threshold and Wait Duration

**Configuration in application.yml (from config-server):**

```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        slidingWindowSize: 10              # Number of calls in sliding window
        minimumNumberOfCalls: 5            # Minimum calls before calculating rate
        failureRateThreshold: 50           # Failure percentage to trip (50%)
        waitDurationInOpenState: 60s      # Time in OPEN before HALF-OPEN
        permittedNumberOfCallsInHalfOpenState: 3  # Test calls in HALF-OPEN
        slowCallRateThreshold: 100         # Slow call rate threshold
        slowCallDurationThreshold: 2s      # What qualifies as "slow"
        recordExceptions:
          - java.util.concurrent.TimeoutException
          - java.io.IOException
        ignoreExceptions:
          - com.foodflow.order.exception.BusinessException
```

**Key parameters explained:**
- `slidingWindowSize`: Window size for failure rate calculation (count-based or time-based)
- `failureRateThreshold`: Percentage of failures that triggers OPEN state
- `waitDurationInOpenState`: How long to stay OPEN before attempting recovery
- `slowCallRateThreshold`: Trip if calls are consistently slow (even if they succeed)
- `permittedNumberOfCallsInHalfOpenState`: How many test calls to allow in recovery

**Applying to Feign client:**
```java
@FeignClient(
    name = "payment-service",
    fallback = PaymentServiceClientFallback.class,
    configuration = FeignCircuitBreakerConfig.class
)
public interface PaymentServiceClient {
    @PostMapping("/api/v1/payments")
    ApiResponse<PaymentResponseDto> createPayment(@RequestBody PaymentRequestDto dto);
}
```

### Implementing Fallback Methods

**Fallback class for Feign client:**

```java
@Component
@Slf4j
public class PaymentServiceClientFallback implements PaymentServiceClient {

    @Override
    public ApiResponse<PaymentResponseDto> createPayment(PaymentRequestDto dto) {
        log.error("Payment service unavailable, using fallback for order: {}", dto.getOrderId());
        
        // Return a graceful response indicating payment service is down
        return ApiResponse.<PaymentResponseDto>error(
            "Payment service temporarily unavailable. Please try again later.",
            List.of("PAYMENT_SERVICE_UNAVAILABLE")
        );
    }
}
```

**Fallback strategies:**
1. **Return cached data**: Use last known good value
2. **Return default value**: Provide sensible defaults
3. **Return error message**: Inform user of unavailability
4. **Queue for later processing**: Store request, process when service recovers
5. **Call alternative service**: Use backup provider

**Programmatic Circuit Breaker with fallback:**

```java
@CircuitBreaker(
    name = "paymentService",
    fallbackMethod = "createPaymentFallback"
)
public PaymentResponseDto createPayment(PaymentRequestDto dto) {
    return paymentServiceClient.createPayment(dto).getData();
}

private PaymentResponseDto createPaymentFallback(PaymentRequestDto dto, Exception ex) {
    log.error("Circuit breaker triggered for payment service", ex);
    
    // Create a pending payment record to process later
    PaymentResponseDto fallback = new PaymentResponseDto();
    fallback.setOrderId(dto.getOrderId());
    fallback.setStatus("PENDING_RETRY");
    fallback.setMessage("Payment queued for retry");
    
    return fallback;
}
```

### Monitoring Circuit Breaker Health

**Metrics exposed by Resilience4j:**
- Circuit state (CLOSED, OPEN, HALF-OPEN)
- Failure rate
- Success rate
- Number of buffered calls
- Number of failed calls
- Number of slow calls

**Actuator endpoint integration:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,circuitbreakers
  endpoint:
    health:
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true
```

**Accessing metrics:**
```
GET /actuator/circuitbreakers
GET /actuator/metrics/resilience4j.circuitbreaker.state
GET /actuator/metrics/resilience4j.circuitbreaker.failure.rate
GET /actuator/prometheus
```

**Sample Prometheus queries:**
```promql
# Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)
resilience4j_circuitbreaker_state{name="paymentService"}

# Failure rate percentage
resilience4j_circuitbreaker_failure_rate{name="paymentService"}

# Number of successful calls
rate(resilience4j_circuitbreaker_successful_calls{name="paymentService"}[5m])
```

**Logging circuit state changes:**
```java
@Component
@Slf4j
public class CircuitBreakerEventListener {

    @EventListener
    public void onCircuitBreakerEvent(CircuitBreakerOnStateTransitionEvent event) {
        log.warn("Circuit breaker state transition: {} from {} to {}",
            event.getCircuitBreakerName(),
            event.getStateTransition().getFromState(),
            event.getStateTransition().getToState());
    }
}
```

### Real-World Examples of Resilience Patterns

**Example 1: Order Service calling Payment Service**
```java
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
@Retry(name = "paymentService", fallbackMethod = "paymentFallback")
@TimeLimiter(name = "paymentService")
public CompletableFuture<PaymentResponseDto> processPayment(PaymentRequestDto dto) {
    return CompletableFuture.supplyAsync(() -> 
        paymentServiceClient.createPayment(dto).getData()
    );
}

private CompletableFuture<PaymentResponseDto> paymentFallback(PaymentRequestDto dto, Exception ex) {
    // Queue payment for async processing
    paymentQueueService.enqueueForRetry(dto);
    
    return CompletableFuture.completedFuture(
        PaymentResponseDto.builder()
            .status("QUEUED")
            .message("Payment queued for processing")
            .build()
    );
}
```

**Example 2: Menu Service with Bulkhead (limit concurrent calls)**
```java
@Bulkhead(name = "menuService", type = Bulkhead.Type.THREADPOOL)
public List<MenuItemResponseDto> getMenuItems(Long restaurantId) {
    return menuServiceClient.getMenuByRestaurant(restaurantId).getData();
}
```

**Example 3: Rate Limiter on public API**
```java
@RateLimiter(name = "publicApi", fallbackMethod = "rateLimitFallback")
public ResponseEntity<ApiResponse<RestaurantResponseDto>> getRestaurant(Long id) {
    return ResponseEntity.ok(restaurantService.getRestaurantById(id));
}

private ResponseEntity<ApiResponse<RestaurantResponseDto>> rateLimitFallback(Long id, Exception ex) {
    return ResponseEntity.status(429).body(
        ApiResponse.error("Too many requests, please try again later", null)
    );
}
```

**Example 4: Cache with Circuit Breaker**
```java
@Cacheable(value = "restaurants", key = "#id")
@CircuitBreaker(name = "restaurantService", fallbackMethod = "restaurantFallback")
public RestaurantResponseDto getRestaurant(Long id) {
    return restaurantServiceClient.getRestaurantById(id).getData();
}

private RestaurantResponseDto restaurantFallback(Long id, Exception ex) {
    // Try to get from cache even if circuit is open
    return cacheManager.getCache("restaurants").get(id, RestaurantResponseDto.class);
}
```

### Common Configuration Mistakes and Overuse of Retry

**Common mistakes:**

1. **Setting failure threshold too high**
   - Mistake: 90% failure rate before tripping
   - Impact: Too many failures before circuit opens
   - Fix: Use 50-60% threshold

2. **Wait duration too short**
   - Mistake: 5 seconds wait before HALF-OPEN
   - Impact: Circuit flips rapidly, doesn't give service time to recover
   - Fix: Use 30-60 seconds minimum

3. **No timeout on Feign clients**
   - Mistake: Relying only on circuit breaker
   - Impact: Threads block indefinitely on slow services
   - Fix: Always set connect and read timeouts

4. **Retry without exponential backoff**
   - Mistake: Retry immediately with fixed delay
   - Impact: Retry storms overwhelm failing service
   - Fix: Use exponential backoff (1s, 2s, 4s, 8s)

5. **Circuit breaker on non-critical paths**
   - Mistake: Circuit breaker on logging service
   - Impact: Unnecessary complexity
   - Fix: Use fallback only, no circuit breaker for non-critical services

6. **Ignoring specific exceptions**
   - Mistake: Ignoring all exceptions
   - Impact: Circuit never trips on real failures
   - Fix: Only ignore business exceptions, not system exceptions

**Overuse of retry:**

```yaml
# BAD: Excessive retry configuration
resilience4j:
  retry:
    instances:
      paymentService:
        maxAttempts: 10              # Too many retries
        waitDuration: 100ms         # Too fast between retries
        retryExceptions:
          - java.lang.Exception    # Retry on everything

# GOOD: Balanced retry configuration
resilience4j:
  retry:
    instances:
      paymentService:
        maxAttempts: 3              # Reasonable limit
        waitDuration: 1s           # Give service time
        exponentialBackoffMultiplier: 2  # Exponential backoff
        retryExceptions:
          - java.net.SocketTimeoutException
          - java.io.IOException
        ignoreExceptions:
          - com.foodflow.payment.exception.InsufficientFundsException
```

**When NOT to use retry:**
- Non-idempotent operations (POST without idempotency key)
- Business logic failures (insufficient funds, invalid data)
- Authentication failures (wrong password)
- Rate limit exceeded (429 status)
- Validation errors (400 status)

**Best practices summary:**
- Use Circuit Breaker for all cross-service calls
- Use Retry only for transient network failures
- Always configure timeouts on Feign clients
- Implement meaningful fallbacks (not just null returns)
- Monitor circuit state and metrics
- Test failure scenarios in integration tests
- Don't over-engineer for non-critical paths

---

## Async Processing in Spring Boot Microservices

### When to Use Async Processing

Use `@Async` for operations that:
- Are I/O-bound (network calls, database queries, file operations)
- Take more than 500ms to complete
- Don't need to block the main request-response flow
- Can be processed independently (fire-and-forget)
- Have retry logic or can tolerate failures

**Common async use cases in FoodFlow:**
- Email sending (notification-service)
- SMS/push notifications (notification-service)
- Report generation (notification-service, order-service)
- Payment processing (payment-service - already async via Feign)
- Image processing (future: menu-service)
- Data export/sync operations

**DO NOT use async for:**
- Fast database queries (< 100ms)
- Simple calculations
- Operations that must complete before returning response
- Operations that need immediate error feedback

### Enabling @Async in a Service

**Step 1: Add @EnableAsync to main application class**

```java
@SpringBootApplication(scanBasePackages = "com.fooddelivery")
@EnableDiscoveryClient
@EnableAsync  // Add this annotation
public class NotificationServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(NotificationServiceApplication.class, args);
    }
}
```

**Step 2: Create AsyncConfig with ThreadPoolTaskExecutor**

Every service using `@Async` MUST have an `AsyncConfig` class:

```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    private static final Logger log = LoggerFactory.getLogger(AsyncConfig.class);

    @Bean(name = "taskExecutor")
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        
        // Core pool size: minimum threads always alive
        executor.setCorePoolSize(5);
        
        // Max pool size: maximum threads that can be created
        executor.setMaxPoolSize(10);
        
        // Queue capacity: tasks waiting before creating new threads
        executor.setQueueCapacity(100);
        
        // Thread name prefix for debugging
        executor.setThreadNamePrefix("AsyncNotification-");
        
        // Keep alive time: seconds to keep idle threads alive
        executor.setKeepAliveSeconds(60);
        
        // Graceful shutdown: wait for tasks to complete
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(60);
        
        // Rejection policy: what to do when queue is full
        executor.setRejectedExecutionHandler(
            new java.util.concurrent.ThreadPoolExecutor.CallerRunsPolicy()
        );
        
        executor.initialize();
        
        log.info("Async Task Executor configured with corePoolSize={}, maxPoolSize={}, queueCapacity={}",
                executor.getCorePoolSize(), executor.getMaxPoolSize(), executor.getQueueCapacity());
        
        return executor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (throwable, method, params) -> {
            log.error("Async method execution failed - Method: {}, Params: {}, Exception: {}",
                    method.getName(), Arrays.toString(params), throwable.getMessage(), throwable);
        };
    }
}
```

**Step 3: Annotate async methods with @Async**

```java
@Service
public class NotificationServiceImpl implements NotificationService {

    @Async("taskExecutor")
    public CompletableFuture<Void> sendAsync(NotificationRequestDto request) {
        log.info("Starting async notification send for user {} on thread: {}", 
                request.getUserId(), Thread.currentThread().getName());
        
        try {
            // Simulate processing delay
            Thread.sleep(500);
            
            Notification saved = repository.save(mapper.toEntity(request));
            log.info("Async notification sent successfully to user {}", request.getUserId());
            
            return CompletableFuture.completedFuture(null);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Async notification send interrupted for user {}", request.getUserId(), e);
            return CompletableFuture.failedFuture(e);
        } catch (Exception e) {
            log.error("Async notification send failed for user {}", request.getUserId(), e);
            return CompletableFuture.failedFuture(e);
        }
    }
}
```

### Thread Pool Configuration Guidelines

**For I/O-bound tasks (most async operations):**
```
Core Pool Size: 5-10 threads
Max Pool Size: 10-20 threads
Queue Capacity: 100-500 tasks
Keep Alive: 60 seconds
```

**For CPU-bound tasks (report generation, image processing):**
```
Core Pool Size: Number of CPU cores
Max Pool Size: Number of CPU cores * 2
Queue Capacity: 50-100 tasks
Keep Alive: 30 seconds
```

**Formula for I/O-bound optimal threads:**
```
Optimal threads = Number of cores * (1 + Wait time / Compute time)

Example: 8 cores, 2000ms wait, 100ms compute = 168 threads
```

### Exception Handling in Async Methods

**Problem:** Exceptions in async methods occur in different threads and are not propagated to the caller.

**Solution 1: Use CompletableFuture**

```java
@Async("taskExecutor")
public CompletableFuture<Void> sendAsync(NotificationRequestDto request) {
    try {
        // processing
        return CompletableFuture.completedFuture(null);
    } catch (Exception e) {
        log.error("Async operation failed", e);
        return CompletableFuture.failedFuture(e);
    }
}
```

**Solution 2: AsyncUncaughtExceptionHandler (configured in AsyncConfig)**

```java
@Override
public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
    return (throwable, method, params) -> {
        log.error("Async method failed - Method: {}, Exception: {}",
                method.getName(), throwable.getMessage(), throwable);
        // Send alert, increment metrics, etc.
    };
}
```

**Critical: Always handle InterruptedException**

```java
catch (InterruptedException e) {
    Thread.currentThread().interrupt(); // Restore interrupt status
    log.error("Operation interrupted", e);
    throw new RuntimeException("Interrupted", e);
}
```

### Logging and Debugging Async Execution

**Thread naming is critical for debugging:**

```java
executor.setThreadNamePrefix("AsyncNotification-");
// Output: AsyncNotification-1, AsyncNotification-2, etc.
```

**Log at start and end of async methods:**

```java
@Async("taskExecutor")
public CompletableFuture<Void> sendAsync(NotificationRequestDto request) {
    log.info("Starting async notification for user {} on thread: {}", 
            request.getUserId(), Thread.currentThread().getName());
    
    try {
        // processing
        log.info("Async notification completed successfully for user {}", request.getUserId());
        return CompletableFuture.completedFuture(null);
    } catch (Exception e) {
        log.error("Async notification failed for user {}", request.getUserId(), e);
        return CompletableFuture.failedFuture(e);
    }
}
```

**Monitor thread pool metrics:**

```java
@Scheduled(fixedRate = 5000)
public void logThreadPoolMetrics() {
    ThreadPoolTaskExecutor executor = (ThreadPoolTaskExecutor) taskExecutor;
    log.info("ThreadPool: active={}, poolSize={}, queueSize={}, completed={}",
            executor.getActiveCount(),
            executor.getPoolSize(),
            executor.getQueue().size(),
            executor.getThreadPoolExecutor().getCompletedTaskCount());
}
```

### @Async vs CompletableFuture

| Feature | @Async | CompletableFuture |
|---------|--------|-------------------|
| Simplicity | High | Medium |
| Composition | No | Yes |
| Exception handling | Limited | Rich |
| Return type | Void, Future | CompletableFuture |
| Chaining | No | Yes |
| Use case | Simple fire-and-forget | Complex async flows |

**Best practice: Combine both**

```java
@Async("taskExecutor")
public CompletableFuture<NotificationResult> sendNotificationAsync() {
    // @Async provides thread management
    // CompletableFuture provides composition
    try {
        NotificationResult result = processNotification();
        return CompletableFuture.completedFuture(result);
    } catch (Exception e) {
        return CompletableFuture.failedFuture(e);
    }
}

// Caller can chain operations
sendNotificationAsync()
    .thenCompose(result -> sendEmailAsync(result))
    .thenAccept(email -> log.info("Email sent"))
    .exceptionally(ex -> {
        log.error("Failed", ex);
        return null;
    });
```

### Common Mistakes to Avoid

1. **Calling @Async method from same class**
   - Problem: Spring proxy bypassed, runs synchronously
   - Solution: Inject self and call `self.asyncMethod()`

2. **Not configuring ThreadPoolTaskExecutor**
   - Problem: Uses SimpleAsyncTaskExecutor (creates new thread per task)
   - Solution: Always configure custom executor

3. **Ignoring exceptions**
   - Problem: Exceptions lost in background thread
   - Solution: Use CompletableFuture or AsyncUncaughtExceptionHandler

4. **Blocking in async method**
   - Problem: Defeats purpose of async
   - Solution: Use non-blocking operations or nested async calls

5. **Not handling InterruptedException**
   - Problem: Thread interrupt status lost
   - Solution: Always restore with `Thread.currentThread().interrupt()`

6. **Overusing @Async**
   - Problem: Unnecessary overhead for fast operations
   - Solution: Use only for slow I/O operations (>500ms)

7. **Private @Async methods**
   - Problem: Won't work (proxy can't intercept)
   - Solution: Must be public

8. **@Async on @Transactional methods**
   - Problem: Transaction context lost in new thread
   - Solution: Use @Transactional on the calling method, not the async method

### Implementation Examples from FoodFlow

**Notification Service - Async email sending:**

```java
@Async("taskExecutor")
public CompletableFuture<Void> sendEmailAsync(String to, String subject, String body) {
    log.info("Starting async email send to {} on thread: {}", to, Thread.currentThread().getName());
    
    try {
        Thread.sleep(2000); // Simulate email sending delay
        
        log.info("Email sent successfully to {} with subject: {}", to, subject);
        
        // Save as notification record
        NotificationRequestDto notification = new NotificationRequestDto();
        notification.setUserId(0L);
        notification.setMessage("Email sent: " + subject);
        notification.setType("EMAIL");
        repository.save(mapper.toEntity(notification));
        
        return CompletableFuture.completedFuture(null);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        log.error("Async email send interrupted for {}", to, e);
        return CompletableFuture.failedFuture(e);
    } catch (Exception e) {
        log.error("Async email send failed for {}", to, e);
        return CompletableFuture.failedFuture(e);
    }
}
```

**Order Service - Async notification calls:**

```java
@Async("taskExecutor")
private void sendNotification(Long userId, String message, String type) {
    log.info("Sending async notification to user {} on thread: {}", userId, Thread.currentThread().getName());
    try {
        NotificationRequestDto notification = new NotificationRequestDto();
        notification.setUserId(userId);
        notification.setMessage(message);
        notification.setType(type);
        notificationClient.sendNotification(notification);
        log.info("Async notification sent successfully to user {}", userId);
    } catch (Exception e) {
        log.error("Failed to send async notification to user {}", userId, e);
    }
}

// Usage in order processing
@Override
@Transactional
public OrderResponseDto placeOrder(OrderRequestDto request) {
    // ... order processing
    
    // These run asynchronously without blocking
    sendNotification(order.getCustomerId(), "Order placed", "ORDER_PLACED");
    sendNotification(order.getCustomerId(), "Order accepted", "ORDER_ACCEPTED");
    
    return orderMapper.toResponse(order); // Returns immediately
}
```

**Controller endpoints for async operations:**

```java
@RestController
@RequestMapping("/notifications")
public class NotificationController {

    // Fire-and-forget async
    @PostMapping("/async")
    public ResponseEntity<String> sendAsync(@Valid @RequestBody NotificationRequestDto request) {
        log.info("Received async notification request for user {}", request.getUserId());
        service.sendAsync(request);
        return ResponseEntity.accepted().body("Notification is being processed asynchronously");
    }

    // Async with CompletableFuture (waits for result)
    @GetMapping("/report/{userId}")
    public CompletableFuture<ResponseEntity<String>> generateReport(@PathVariable Long userId) {
        log.info("Received report generation request for user {}", userId);
        return service.generateReportAsync(userId)
                .thenApply(report -> ResponseEntity.ok(report));
    }
}
```

### Performance Impact

**Before async (synchronous):**
- Order placement time: ~2.5 seconds (includes notification calls)
- Throughput: ~24 orders/minute per thread
- Thread blocking: Yes

**After async:**
- Order placement time: ~0.5 seconds (notifications async)
- Throughput: ~120 orders/minute per thread (5x improvement)
- Thread blocking: No

### Configuration in Config Server

Add to service-specific YAML in config-repo:

```yaml
# notification-service.yml
resilience4j:
  circuitbreaker:
    instances:
      notificationService:
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 30s

# Thread pool monitoring
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,threaddump
  metrics:
    export:
      prometheus:
        enabled: true
```

---

## Final Output Checklist (what AI must deliver after generating a service)

- [ ] List of all created files with their full package path
- [ ] `application.yml` sample (local override only — no secrets)
- [ ] Sample cURL commands for every endpoint
- [ ] Any manual steps (schema creation, config-server setup)
- [ ] Short summary of what business rules are enforced and where

*(End of FoodFlow Skill Spec)*   how much did you rate this skills.md file out of 10 