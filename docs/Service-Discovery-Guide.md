# Service Discovery in Microservices Architecture
## A Comprehensive Guide with Netflix Eureka

---

## Table of Contents

1. [The Problem of Hardcoded Service URLs](#1-the-problem-of-hardcoded-service-urls)
2. [What is Service Discovery?](#2-what-is-service-discovery)
3. [Client-side vs Server-side Service Discovery](#3-client-side-vs-server-side-service-discovery)
4. [Introduction to Netflix Eureka](#4-introduction-to-netflix-eureka)
5. [Dynamic Service Registration](#5-dynamic-service-registration)
6. [Service Discovery and Load Balancing](#6-service-discovery-and-load-balancing)
7. [Heartbeat Mechanism and Automatic Deregistration](#7-heartbeat-mechanism-and-automatic-deregistration)
8. [Benefits of Service Discovery](#8-benefits-of-service-discovery)
9. [Common Mistakes and Configuration Issues](#9-common-mistakes-and-configuration-issues)
10. [Real-world Architecture Example](#10-real-world-architecture-example)

---

## 1. The Problem of Hardcoded Service URLs

### The Challenge

In a microservices architecture, services need to communicate with each other frequently. A naive approach is to hardcode the URLs of dependent services:

```java
// Bad practice - Hardcoded URL
String customerServiceUrl = "http://localhost:8081/api/customers";
String orderServiceUrl = "http://localhost:8082/api/orders";
```

### Problems with Hardcoded URLs

**1. Environment Dependency**
- Development: `localhost:8081`
- Staging: `staging-server:8081`
- Production: `prod-server-1:8081`, `prod-server-2:8081`

**2. Scalability Issues**
- When scaling horizontally, multiple instances run on different ports/hosts
- Hardcoded URLs cannot handle dynamic instance addition/removal

**3. Maintenance Overhead**
- Every service URL change requires code updates and redeployment
- Configuration becomes complex and error-prone

**4. Single Point of Failure**
- If a hardcoded instance fails, the calling service has no fallback mechanism
- No automatic failover to healthy instances

**5. Load Balancing Complexity**
- Manual load balancing requires custom implementation
- Difficult to distribute traffic evenly across instances

### Real-world Impact

In our Food Delivery Platform, without service discovery:
- Order Service needs to know Customer Service URL
- Order Service needs to know Restaurant Service URL
- Order Service needs to know Payment Service URL
- Each service would need configuration for every dependency

---

## 2. What is Service Discovery?

### Definition

Service Discovery is the process of automatically detecting devices and services on a computer network. In microservices, it refers to the mechanism where services can find and communicate with each other without hardcoded configuration.

### Why is Service Discovery Required?

**1. Dynamic Environment**
- Services scale up and down automatically
- Instances are created and destroyed dynamically (especially in cloud environments)
- IP addresses and ports change frequently

**2. High Availability**
- Services need to discover healthy instances automatically
- Automatic failover when instances fail
- No manual intervention required

**3. Load Distribution**
- Distribute requests across multiple instances
- Implement various load balancing strategies
- Optimize resource utilization

**4. Simplified Configuration**
- Services only need to know the service discovery server
- No need to configure individual service URLs
- Centralized service registry

**5. Cloud-Native Architecture**
- Essential for container orchestration (Kubernetes, Docker Swarm)
- Supports auto-scaling groups
- Enables zero-downtime deployments

### Core Components

```
┌─────────────────┐
│  Service A      │
│  (Producer)     │
└────────┬────────┘
         │ Registers
         ▼
┌─────────────────┐
│  Service        │
│  Registry       │
│  (Eureka)       │
└────────┬────────┘
         │ Discovers
         ▼
┌─────────────────┐
│  Service B      │
│  (Consumer)     │
└─────────────────┘
```

---

## 3. Client-side vs Server-side Service Discovery

### Client-side Service Discovery

**How it Works:**
- Client service queries the service registry
- Registry returns available service instances
- Client selects an instance (using load balancing)
- Client makes direct calls to the selected instance

**Architecture:**
```
Client → Service Registry → Select Instance → Direct Call
```

**Advantages:**
- Simpler architecture (no additional infrastructure)
- Client has control over load balancing
- Reduced network hops
- Better performance (direct calls)

**Disadvantages:**
- Client must implement service discovery logic
- Tight coupling between client and registry
- Complex client code
- Difficult to update discovery logic across all services

**Example: Netflix Eureka (Client-side)**

### Server-side Service Discovery

**How it Works:**
- Client makes requests to a load balancer
- Load balancer queries service registry
- Load balancer routes request to appropriate instance
- Client is unaware of service discovery

**Architecture:**
```
Client → Load Balancer → Service Registry → Instance
```

**Advantages:**
- Simpler client code
- Centralized load balancing logic
- Easy to update discovery strategy
- Better for heterogeneous clients

**Disadvantages:**
- Additional infrastructure component
- Extra network hop (potential latency)
- Single point of failure (load balancer)
- More complex infrastructure

**Example: AWS ALB, Kubernetes Service, Consul (Server-side)**

### Comparison Table

| Aspect | Client-side | Server-side |
|--------|-------------|-------------|
| Complexity | Client complexity | Infrastructure complexity |
| Performance | Better (direct calls) | Good (one extra hop) |
| Scalability | High | High |
| Maintenance | Per-service updates | Centralized updates |
| Flexibility | High | Medium |
| Use Case | Netflix Eureka | AWS ALB, K8s Service |

### Our Project's Approach

Our Food Delivery Platform uses **Client-side Service Discovery** with Netflix Eureka:
- API Gateway uses `lb://service-name` for load balancing
- Each service registers with Eureka server
- Services discover each other through Eureka
- Spring Cloud Load Balancer handles client-side load balancing

---

## 4. Introduction to Netflix Eureka

### What is Netflix Eureka?

Netflix Eureka is a REST-based service, primarily for load balancing of middle-tier servers. It acts as a client-side service discovery server where each client service registers with the Eureka server.

### Key Features

**1. Service Registration**
- Services register themselves on startup
- Provide metadata (host, port, health status)
- Automatic registration with minimal configuration

**2. Service Discovery**
- Clients query Eureka for service instances
- Returns list of available instances
- Supports filtering by metadata

**3. Load Balancing**
- Integrates with Ribbon (deprecated) and Spring Cloud Load Balancer
- Supports multiple load balancing strategies
- Client-side load balancing

**4. Fault Tolerance**
- Eureka server clustering for high availability
- Client-side caching of registry information
- Automatic failover

**5. Self-Preservation Mode**
- Prevents mass deregistration during network partitions
- Protects against false positives
- Configurable thresholds

### Eureka Architecture

```
                    ┌─────────────────┐
                    │  Eureka Server  │
                    │  (Registry)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    Register            Register            Register
         │                   │                   │
         ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Service A  │   │   Service B  │   │   Service C  │
│  Instance 1  │   │  Instance 1  │   │  Instance 1  │
│  Instance 2  │   │  Instance 2  │   │  Instance 2  │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Eureka Server Configuration

In our project, the Eureka server is configured in `discovery-server/src/main/resources/application.yml`:

```yaml
server:
  port: 8761

spring:
  application:
    name: discovery-server

eureka:
  client:
    register-with-eureka: false  # Server doesn't register with itself
    fetch-registry: false        # Server doesn't fetch registry
  server:
    enable-self-preservation: false  # Disable for development
```

**Key Configuration Points:**
- Port 8761 is the default Eureka port
- Server doesn't register with itself (it's the registry)
- Self-preservation disabled for development (enable in production)

### Eureka Client Configuration

Services register with Eureka using configuration from Config Server:

```yaml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    register-with-eureka: true
    fetch-registry: true
```

**Docker Configuration:**
```yaml
eureka:
  client:
    service-url:
      defaultZone: http://discovery-server:8761/eureka/
```

### Dependencies

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

For clients:
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

---

## 5. Dynamic Service Registration

### Registration Process

**1. Service Startup**
- Service initializes and reads configuration
- Connects to Config Server (if configured)
- Loads Eureka client configuration

**2. Registration**
- Service sends registration request to Eureka server
- Includes metadata:
  - Service name (spring.application.name)
  - Host IP address
  - Port number
  - Health check URL
  - Status page URL
  - Custom metadata

**3. Confirmation**
- Eureka server acknowledges registration
- Service is now discoverable
- Other services can now find this service

### Registration Flow

```
┌──────────────┐
│   Service    │
│   Startup    │
└──────┬───────┘
       │
       │ 1. Read Config
       ▼
┌──────────────┐
│ Load Eureka  │
│ Client Config│
└──────┬───────┘
       │
       │ 2. Register
       ▼
┌──────────────┐
│ Eureka Server│
│ (Registry)   │
└──────┬───────┘
       │
       │ 3. Acknowledge
       ▼
┌──────────────┐
│ Service      │
│ Registered   │
└──────────────┘
```

### Service Instance Metadata

When a service registers, it provides the following information:

```json
{
  "instanceId": "order-service:192.168.1.100:8082",
  "app": "ORDER-SERVICE",
  "hostName": "192.168.1.100",
  "ipAddr": "192.168.1.100",
  "status": "UP",
  "port": {
    "$": 8082,
    "@enabled": true
  },
  "healthCheckUrl": "http://192.168.1.100:8082/actuator/health",
  "statusPageUrl": "http://192.168.1.100:8082/actuator/info",
  "vipAddress": "order-service",
  "secureVipAddress": "order-service",
  "metadata": {
    "zone": "us-east-1",
    "version": "1.0.0"
  }
}
```

### Registration in Our Project

**Order Service Registration:**
```yaml
# order-service/src/main/resources/application.yml
spring:
  application:
    name: order-service
  config:
    import: optional:configserver:http://localhost:8888
```

The Eureka configuration is centralized in Config Server:
```yaml
# config-repo/application.yml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    register-with-eureka: true
    fetch-registry: true
```

### Dynamic Instance Addition

When a new instance starts:
1. It automatically registers with Eureka
2. Eureka updates its registry
3. Other services discover the new instance on next refresh
4. Load balancer includes new instance in rotation

**No manual configuration required!**

### Dynamic Instance Removal

When an instance shuts down:
1. It sends deregistration request to Eureka
2. Eureka removes it from registry
3. Other services stop routing to it
4. Graceful shutdown ensures no in-flight requests are lost

---

## 6. Service Discovery and Load Balancing

### Discovery Process

**1. Client Query**
- Service A needs to call Service B
- Service A queries Eureka for Service B instances
- Eureka returns list of available instances

**2. Instance Selection**
- Client uses load balancer to select instance
- Various strategies available (Round Robin, Random, etc.)
- Considers health status and metadata

**3. Service Call**
- Client makes HTTP call to selected instance
- If call fails, retries with another instance
- Circuit breaker pattern for fault tolerance

### Load Balancing Strategies

**1. Round Robin**
- Distributes requests sequentially
- Simple and fair distribution
- Good for similar capacity instances

**2. Random**
- Randomly selects instance
- Simple implementation
- Good statistical distribution

**3. Weighted Response Time**
- Considers instance response time
- Faster instances get more requests
- Optimizes overall performance

**4. Zone-aware**
- Prefers instances in same zone
- Reduces cross-zone latency
- Important for multi-region deployments

### Spring Cloud Load Balancer

Our project uses Spring Cloud Load Balancer (replaces Ribbon):

**Configuration in API Gateway:**
```yaml
spring:
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true
          lower-case-service-id: true
      routes:
        - id: order-service
          uri: lb://order-service  # Load balanced
          predicates:
            - Path=/api/orders/**
```

**Key Points:**
- `lb://service-name` indicates load-balanced call
- Spring Cloud Load Balancer resolves service name to instances
- Automatically selects instance using configured strategy
- Integrates with Eureka for instance discovery

### Feign Client with Service Discovery

Services can use Feign clients for declarative REST calls:

```java
@FeignClient(name = "customer-service")
public interface CustomerClient {
    
    @GetMapping("/api/customers/{id}")
    CustomerDTO getCustomerById(@PathVariable("id") Long id);
}
```

**How it works:**
1. Feign client uses service name (not URL)
2. Spring Cloud resolves service name via Eureka
3. Load balancer selects instance
4. Call is made to selected instance

### Discovery Cache

Eureka clients cache the registry locally:
- Reduces load on Eureka server
- Provides resilience during server outages
- Cache refreshes periodically (default 30 seconds)
- Configurable refresh interval

```yaml
eureka:
  client:
    registry-fetch-interval-seconds: 30
```

---

## 7. Heartbeat Mechanism and Automatic Deregistration

### Heartbeat (Renewal) Mechanism

**Purpose:**
- Eureka server needs to know which instances are still alive
- Services send periodic heartbeats to maintain registration
- Missed heartbeats indicate instance failure

**How it Works:**
1. Service registers with Eureka
2. Service sends heartbeat every 30 seconds (default)
3. Eureka updates last-renewal timestamp
4. If heartbeat not received within timeout, instance marked as DOWN

### Heartbeat Configuration

```yaml
eureka:
  instance:
    lease-renewal-interval-in-seconds: 30  # Heartbeat interval
    lease-expiration-duration-in-seconds: 90  # Timeout before deregistration
  client:
    registry-fetch-interval-seconds: 30  # Cache refresh interval
```

**Parameters:**
- `lease-renewal-interval-in-seconds`: How often to send heartbeat
- `lease-expiration-duration-in-seconds`: How long before instance is considered dead

### Automatic Deregistration

**Process:**
1. Instance stops sending heartbeats
2. Eureka waits for expiration duration
3. Instance status changes from UP to DOWN
4. Instance removed from registry after additional delay
5. Load balancer stops routing to instance

**Graceful Shutdown:**
```yaml
server:
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

With graceful shutdown:
- Service sends deregistration request before stopping
- In-flight requests complete
- No requests routed to shutting down instance

### Self-Preservation Mode

**What is it?**
Eureka's self-preservation mode prevents mass deregistration during network partitions.

**When it activates:**
- If >15% of instances fail to renew heartbeats
- Eureka assumes network partition (not instance failures)
- Stops expiring instances
- Protects against false positives

**Configuration:**
```yaml
eureka:
  server:
    enable-self-preservation: true
    renewal-percent-threshold: 0.85
```

**Trade-offs:**
- Pros: Prevents cascading failures
- Cons: May route to dead instances temporarily
- Recommendation: Enable in production, disable in development

### Health Checks

Eureka can use Spring Boot Actuator health checks:

```yaml
eureka:
  instance:
    health-check-url-path: /actuator/health
    status-page-url-path: /actuator/info
```

**Custom Health Indicators:**
```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    
    @Override
    public Health health() {
        if (databaseIsHealthy()) {
            return Health.up().build();
        }
        return Health.down().withDetail("error", "Database connection failed").build();
    }
}
```

### Monitoring Heartbeats

Eureka Dashboard shows:
- Instance status (UP/DOWN)
- Last heartbeat timestamp
- Renewal interval
- Number of registered instances

Access at: `http://localhost:8761`

---

## 8. Benefits of Service Discovery

### 1. Dynamic Scalability

**Horizontal Scaling:**
- Add instances without configuration changes
- Automatic registration of new instances
- Load balancer immediately includes new instances
- Supports auto-scaling policies

**Example:**
```bash
# Scale order-service to 3 instances
docker-compose up --scale order-service=3
```
All 3 instances automatically register and receive traffic.

### 2. High Availability

**Fault Tolerance:**
- Automatic failover to healthy instances
- No single point of failure (with Eureka clustering)
- Client-side caching provides resilience
- Graceful degradation

**Example:**
If order-service instance 1 fails:
- Eureka detects failure (missed heartbeats)
- Load balancer routes to instances 2 and 3
- Users experience no downtime

### 3. Simplified Configuration

**Centralized Registry:**
- No need to configure service URLs
- Services only need Eureka server location
- Configuration server can provide Eureka config
- Environment-specific configuration

**Before Service Discovery:**
```yaml
services:
  customer-service:
    url: http://customer-service-1:8081,http://customer-service-2:8081
  order-service:
    url: http://order-service-1:8082,http://order-service-2:8082
```

**With Service Discovery:**
```yaml
eureka:
  client:
    service-url:
      defaultZone: http://discovery-server:8761/eureka/
```

### 4. Load Balancing

**Built-in Load Distribution:**
- Automatic load balancing across instances
- Multiple strategies available
- Zone-aware routing for multi-region
- Weighted routing for heterogeneous instances

### 5. Cloud-Native Support

**Container Orchestration:**
- Works seamlessly with Docker
- Supports Kubernetes (though K8s has its own service discovery)
- Ideal for dynamic cloud environments
- Supports blue-green deployments

### 6. Operational Benefits

**Monitoring:**
- Centralized view of all services
- Health status dashboard
- Instance count tracking
- Metadata for organizational information

**Debugging:**
- Service dependency visualization
- Request tracing integration
- Instance-level metrics
- Centralized logging correlation

### 7. Developer Productivity

**Faster Development:**
- No need to manage service URLs
- Local development simplified
- Easy to add new services
- Reduced configuration errors

### 8. Cost Optimization

**Resource Efficiency:**
- Scale based on actual demand
- Avoid over-provisioning
- Automatic instance termination
- Better resource utilization

---

## 9. Common Mistakes and Configuration Issues

### 1. Hardcoded Service URLs

**Mistake:**
```java
String url = "http://localhost:8082/api/orders";
```

**Solution:**
```java
@FeignClient(name = "order-service")
public interface OrderClient {
    // Use service name, not URL
}
```

### 2. Incorrect Eureka Server URL

**Mistake:**
```yaml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka  # Missing trailing slash
```

**Solution:**
```yaml
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/  # Include trailing slash
```

### 3. Server Registering with Itself

**Mistake:**
```yaml
eureka:
  client:
    register-with-eureka: true  # Wrong for Eureka server
```

**Solution:**
```yaml
eureka:
  client:
    register-with-eureka: false  # Correct for Eureka server
```

### 4. Missing Spring Cloud Dependencies

**Mistake:**
```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
<!-- Missing dependency management -->
```

**Solution:**
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>2023.0.3</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 5. Wrong Application Name

**Mistake:**
```yaml
spring:
  application:
    name: order-service  # Must match exactly in all calls
```

But calling with:
```java
@FeignClient(name = "Order-Service")  // Case mismatch!
```

**Solution:**
Use consistent naming (lowercase with hyphens is recommended).

### 6. Ignoring Health Checks

**Mistake:**
Not configuring health checks, leading to routing to unhealthy instances.

**Solution:**
```yaml
eureka:
  instance:
    health-check-url-path: /actuator/health
```

### 7. Self-Preservation in Development

**Mistake:**
```yaml
eureka:
  server:
    enable-self-preservation: true  # Causes issues in dev
```

**Solution:**
```yaml
eureka:
  server:
    enable-self-preservation: false  # Disable in development
```

### 8. Short Lease Expiration

**Mistake:**
```yaml
eureka:
  instance:
    lease-expiration-duration-in-seconds: 10  # Too short!
```

**Solution:**
```yaml
eureka:
  instance:
    lease-expiration-duration-in-seconds: 90  # Reasonable default
```

### 9. Not Using Load Balancer Prefix

**Mistake:**
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: http://order-service  # Not load balanced!
```

**Solution:**
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: lb://order-service  # Load balanced!
```

### 10. Missing Instance ID

**Mistake:**
Multiple instances have same instance ID, causing conflicts.

**Solution:**
```yaml
eureka:
  instance:
    instance-id: ${spring.application.name}:${spring.application.instance_id:${random.value}}
```

### 11. Network Issues in Docker

**Mistake:**
Using `localhost` in Docker Compose configuration.

**Solution:**
```yaml
eureka:
  client:
    service-url:
      defaultZone: http://discovery-server:8761/eureka/  # Use service name
```

### 12. Not Clustering Eureka Server

**Mistake:**
Single Eureka server in production (single point of failure).

**Solution:**
Deploy Eureka server cluster with peer awareness.

---

## 10. Real-world Architecture Example

### Our Food Delivery Platform Architecture

```
                    ┌─────────────────────────────────┐
                    │         API Gateway             │
                    │         (Port 8080)             │
                    │  Uses lb:// for all services    │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────────┐
                    │                                 │
                    ▼                                 ▼
         ┌──────────────────┐              ┌──────────────────┐
         │  Discovery       │              │   Config Server  │
         │  Server          │              │   (Port 8888)    │
         │  (Port 8761)     │              └──────────────────┘
         │  Eureka          │
         └──────────────────┘
                    │
    ┌───────────────┼───────────────┬───────────────┐
    │               │               │               │
    ▼               ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Auth   │   │Customer │   │Restaurant│   │  Menu   │
│ Service │   │ Service │   │ Service  │   │ Service │
│ :8081   │   │ :8082   │   │ :8083    │   │ :8084   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │               │               │               │
    └───────────────┼───────────────┼───────────────┘
                    │               │
                    ▼               ▼
              ┌─────────┐   ┌─────────┐
              │  Order  │   │Payment  │
              │ Service │   │ Service │
              │ :8085   │   │ :8086   │
              └─────────┘   └─────────┘
                    │
                    ▼
              ┌─────────┐   ┌─────────┐
              │Delivery │   │Notification│
              │Partner  │   │ Service  │
              │ Service │   │ :8088    │
              │ :8087   │   └─────────┘
              └─────────┘
```

### Service Registration Flow

**1. Discovery Server Startup**
```bash
# Starts on port 8761
java -jar discovery-server/target/discovery-server.jar
```
- Acts as service registry
- Doesn't register with itself
- Provides dashboard at http://localhost:8761

**2. Config Server Startup**
```bash
# Starts on port 8888
java -jar config-server/target/config-server.jar
```
- Provides centralized configuration
- Serves Eureka client configuration
- All services fetch config from here

**3. Service Startup (e.g., Order Service)**
```bash
java -jar order-service/target/order-service.jar
```

**Registration Process:**
1. Order Service reads `application.yml`
2. Connects to Config Server at `localhost:8888`
3. Fetches Eureka configuration from Config Server
4. Registers with Discovery Server at `localhost:8761`
5. Sends heartbeat every 30 seconds
6. Now discoverable by other services

**4. API Gateway Startup**
```bash
java -jar api-gateway/target/api-gateway.jar
```
- Registers with Eureka
- Discovers all registered services
- Configures routes using `lb://service-name`
- Load balances requests across instances

### Service Discovery in Action

**Example: Order Service calling Customer Service**

**Without Service Discovery:**
```java
// Hardcoded - bad practice
String customerUrl = "http://localhost:8082/api/customers/" + customerId;
```

**With Service Discovery:**
```java
@FeignClient(name = "customer-service")
public interface CustomerClient {
    
    @GetMapping("/api/customers/{id}")
    CustomerDTO getCustomerById(@PathVariable("id") Long id);
}

// Usage
CustomerDTO customer = customerClient.getCustomerById(customerId);
```

**What happens behind the scenes:**
1. Feign client resolves "customer-service" via Eureka
2. Eureka returns: `[{host: "192.168.1.100", port: 8082}, {host: "192.168.1.101", port: 8082}]`
3. Spring Cloud Load Balancer selects instance (Round Robin)
4. Call made to: `http://192.168.1.100:8082/api/customers/123`
5. If fails, retries with next instance

### API Gateway Routing

**Configuration:**
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
```

**Request Flow:**
1. Client calls: `http://localhost:8080/api/orders`
2. API Gateway matches route
3. Resolves `lb://order-service` via Eureka
4. Load balancer selects order-service instance
5. Routes to: `http://order-service-instance:8085/api/orders`
6. Returns response to client

### Docker Deployment

**Docker Compose Configuration:**
```yaml
version: '3.8'
services:
  discovery-server:
    image: food-delivery/discovery-server
    ports:
      - "8761:8761"
  
  config-server:
    image: food-delivery/config-server
    ports:
      - "8888:8888"
  
  order-service:
    image: food-delivery/order-service
    depends_on:
      - discovery-server
      - config-server
    environment:
      - SPRING_PROFILES_ACTIVE=docker
```

**Docker Configuration:**
```yaml
# config-repo/application-docker.yml
eureka:
  client:
    service-url:
      defaultZone: http://discovery-server:8761/eureka/
```

**Key Points:**
- Services use Docker service names (not localhost)
- Eureka server accessible as `discovery-server:8761`
- All services register with Eureka
- API Gateway uses `lb://` for load balancing

### Scaling Example

**Scale Order Service:**
```bash
docker-compose up --scale order-service=3
```

**What happens:**
1. Three order-service containers start
2. Each registers with Eureka
3. Eureka shows 3 instances
4. API Gateway load balances across all 3
5. No configuration changes needed!

### Monitoring

**Eureka Dashboard:**
- URL: `http://localhost:8761`
- Shows all registered services
- Instance status (UP/DOWN)
- Last heartbeat timestamp
- Instance count per service

**Actuator Endpoints:**
- Health: `/actuator/health`
- Info: `/actuator/info`
- Metrics: `/actuator/metrics`
- Env: `/actuator/env`

### Benefits in Our Architecture

**1. Dynamic Service Addition**
- Add new service (e.g., Rating Service)
- Register with Eureka
- API Gateway automatically discovers it
- No configuration changes in other services

**2. Horizontal Scaling**
- Scale any service independently
- Auto-registration with Eureka
- Automatic load balancing
- Handle increased load

**3. Fault Tolerance**
- Instance failure detected via heartbeat
- Automatic failover to healthy instances
- No manual intervention required
- High availability

**4. Simplified Development**
- Developers don't need to know service URLs
- Use service names in Feign clients
- Easy local development
- Consistent across environments

**5. Production Ready**
- Supports Eureka clustering
- Self-preservation mode
- Zone-aware routing
- Comprehensive monitoring

---

## Conclusion

Service Discovery is a fundamental pattern in microservices architecture that addresses the challenges of dynamic, distributed systems. Netflix Eureka provides a robust, production-ready solution for service registration and discovery.

### Key Takeaways

1. **Eliminate Hardcoded URLs**: Use service names instead of hardcoded URLs
2. **Dynamic Registration**: Services automatically register on startup
3. **Load Balancing**: Built-in client-side load balancing
4. **Fault Tolerance**: Heartbeat mechanism and automatic failover
5. **Scalability**: Easy horizontal scaling without configuration changes
6. **Simplified Operations**: Centralized service registry and monitoring

### Best Practices

1. Enable self-preservation in production
2. Configure health checks for accurate instance status
3. Use appropriate lease expiration intervals
4. Cluster Eureka servers for high availability
5. Monitor Eureka dashboard regularly
6. Use zone-aware routing for multi-region deployments
7. Implement graceful shutdown
8. Test failover scenarios

### Our Food Delivery Platform

Our implementation demonstrates:
- Eureka server as centralized registry
- Config server for centralized configuration
- API Gateway with service discovery
- Feign clients for inter-service communication
- Docker deployment with service discovery
- Horizontal scaling capabilities

This architecture provides a solid foundation for a scalable, resilient microservices system.

---

## References

- [Spring Cloud Netflix Eureka Documentation](https://spring.io/projects/spring-cloud-netflix)
- [Netflix Eureka GitHub](https://github.com/Netflix/eureka)
- [Spring Cloud Load Balancer](https://spring.io/projects/spring-cloud-commons)
- [Microservices Patterns](https://microservices.io/patterns/service-registry.html)

---

*Document generated for Food Delivery Platform Microservices Architecture*
