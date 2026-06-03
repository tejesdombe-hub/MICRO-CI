# Messaging in Microservices Architecture - Complete Guide

## Table of Contents
1. [What is Messaging in Distributed Systems](#what-is-messaging-in-distributed-systems)
2. [Why Messaging is Used in Microservices Architecture](#why-messaging-is-used-in-microservices-architecture)
3. [Synchronous vs Asynchronous Communication](#synchronous-vs-asynchronous-communication)
4. [Introduction to Message Brokers (Kafka / RabbitMQ)](#introduction-to-message-brokers-kafka--rabbitmq)
5. [Core Concepts: Producer, Consumer, Broker, Topic/Queue](#core-concepts-producer-consumer-broker-topicqueue)
6. [Event-Driven Architecture Basics](#event-driven-architecture-basics)
7. [Message Flow in a Real-World System](#message-flow-in-a-real-world-system)
8. [Loose Coupling Using Messaging](#loose-coupling-using-messaging)
9. [Handling Message Failures and Retries](#handling-message-failures-and-retries)
10. [Idempotency and Duplicate Message Handling](#idempotency-and-duplicate-message-handling)
11. [High-Level Comparison: Kafka vs RabbitMQ](#high-level-comparison-kafka-vs-rabbitmq)
12. [Real-World Use Cases](#real-world-use-cases)
13. [Implementation in This Project](#implementation-in-this-project)

---

## What is Messaging in Distributed Systems

**Messaging** in distributed systems refers to the asynchronous exchange of data between different services or components through a message broker. Unlike direct HTTP calls where the caller waits for a response, messaging allows services to communicate without being tightly coupled to each other's availability.

### Key Characteristics:
- **Asynchronous**: The sender doesn't wait for the receiver to process the message
- **Decoupled**: Services don't need to know about each other's implementation details
- **Reliable**: Messages can be persisted and retried if processing fails
- **Scalable**: Multiple consumers can process messages from the same queue

### How It Works:
```
Producer Service → Message Broker → Consumer Service
                    (Stores & Forwards)
```

The producer sends a message to a broker, which stores it until a consumer retrieves and processes it. This decouples the producer from the consumer in both time and space.

---

## Why Messaging is Used in Microservices Architecture

### 1. **Decoupling**
Services can evolve independently without breaking each other. If a consumer is down, the producer can still send messages without failing.

### 2. **Asynchronous Processing**
Long-running tasks don't block the main flow. For example, sending an email notification can happen asynchronously after an order is placed.

### 3. **Load Balancing**
Multiple instances of a consumer service can process messages from the same queue, automatically distributing the load.

### 4. **Reliability & Resilience**
Messages are persisted by the broker. If a consumer crashes, messages aren't lost—they can be retried later.

### 5. **Event-Driven Architecture**
Services react to events rather than polling for changes, leading to more responsive systems.

### 6. **Temporal Decoupling**
The producer and consumer don't need to be available at the same time. The producer can send messages when the consumer is offline.

---

## Synchronous vs Asynchronous Communication

### Synchronous Communication
**Definition**: The caller waits for the callee to complete processing and return a response.

**Example**: HTTP REST API calls
```java
// Order Service calls Payment Service synchronously
PaymentResponse response = paymentClient.processPayment(request);
// Waits here until payment service responds
```

**Pros**:
- Simple to implement and understand
- Immediate feedback (success/error)
- Easier debugging

**Cons**:
- Tight coupling between services
- Blocking - caller waits for response
- Cascading failures if downstream service is down
- Limited scalability

**Use Cases**:
- When immediate response is required
- Simple request-response patterns
- Real-time validation

### Asynchronous Communication
**Definition**: The caller sends a message and continues without waiting for the response.

**Example**: Message queues
```java
// Order Service sends event and continues
messageProducer.sendOrderEvent(orderEvent);
// Continues immediately without waiting
```

**Pros**:
- Loose coupling between services
- Non-blocking - caller continues immediately
- Better resilience - messages queued if consumer is down
- Better scalability
- Natural for event-driven patterns

**Cons**:
- More complex to implement
- No immediate feedback
- Harder debugging
- Eventual consistency

**Use Cases**:
- Notifications (email, SMS)
- Audit logging
- Data synchronization
- Long-running tasks
- Event-driven workflows

### Comparison Table

| Aspect | Synchronous | Asynchronous |
|--------|------------|--------------|
| Coupling | Tight | Loose |
| Blocking | Yes | No |
| Response Time | Immediate | Eventual |
| Complexity | Low | High |
| Resilience | Low | High |
| Scalability | Limited | High |
| Use Case | Real-time operations | Background processing |

---

## Introduction to Message Brokers (Kafka / RabbitMQ)

### What is a Message Broker?
A message broker is an intermediary that receives, stores, and forwards messages between producers and consumers. It provides reliable message delivery and decouples services.

### Apache Kafka
**Type**: Distributed streaming platform
**Model**: Log-based, append-only
**Use Case**: High-throughput event streaming, real-time data pipelines

**Key Features**:
- High throughput (millions of messages per second)
- Message retention (messages stored for configurable time)
- Partitioning for parallelism
- Consumer groups for load balancing
- Exactly-once semantics

**Best For**:
- Event sourcing
- Real-time analytics
- Log aggregation
- Stream processing

### RabbitMQ
**Type**: Traditional message broker
**Model**: Queue-based with routing
**Use Case**: Reliable message delivery, complex routing

**Key Features**:
- Flexible routing (exchanges, bindings)
- Message acknowledgments
- Dead letter queues
- TTL (Time To Live) on messages
- Multiple protocols (AMQP, MQTT, STOMP)

**Best For**:
- Traditional messaging patterns
- Complex routing requirements
- Reliable message delivery
- Work queues

### Why We Chose RabbitMQ for This Project
- **Simpler setup** for microservices
- **Better routing** capabilities with exchanges
- **Reliable message delivery** with acknowledgments
- **Dead letter queues** for failed messages
- **Mature ecosystem** with Spring Boot integration

---

## Core Concepts: Producer, Consumer, Broker, Topic/Queue

### Producer
**Definition**: A service that creates and sends messages to a message broker.

**Responsibilities**:
- Create messages with proper structure
- Send messages to exchanges/queues
- Handle publishing confirmations
- Implement retry logic for failed sends

**Example in Our Project**:
```java
// OrderService acts as a producer
@Component
public class OrderServiceImpl {
    private final MessageProducer messageProducer;
    
    public OrderResponseDto placeOrder(OrderRequestDto request) {
        // ... business logic ...
        OrderEvent event = OrderEvent.createOrderPlacedEvent(...);
        messageProducer.sendOrderEvent(event); // Produces message
    }
}
```

### Consumer
**Definition**: A service that receives and processes messages from a message broker.

**Responsibilities**:
- Subscribe to queues/topics
- Process messages
- Acknowledge successful processing
- Handle processing failures
- Implement idempotency

**Example in Our Project**:
```java
// NotificationService acts as a consumer
@Component
public class OrderEventConsumer {
    
    @RabbitListener(queues = "notification.queue")
    public void handleOrderEvent(OrderEvent event) {
        // Process the message
        notificationService.sendNotification(...);
    }
}
```

### Broker
**Definition**: The middleware that receives, stores, and forwards messages between producers and consumers.

**Responsibilities**:
- Accept messages from producers
- Store messages durably
- Route messages to appropriate queues
- Deliver messages to consumers
- Handle acknowledgments
- Manage connections

**In Our Project**: RabbitMQ running in Docker container

### Queue (RabbitMQ)
**Definition**: A buffer that stores messages until they are consumed.

**Characteristics**:
- First-in-first-out (FIFO) delivery
- Messages can be durable (persisted to disk)
- Multiple consumers can share a queue (work queue pattern)
- Each message delivered to one consumer

**Example in Our Project**:
```java
@Bean
public Queue notificationQueue() {
    return QueueBuilder.durable("notification.queue")
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", "notification.dlq")
            .build();
}
```

### Topic (Kafka)
**Definition**: A category or feed name to which messages are published.

**Characteristics**:
- Log-based storage
- Messages retained for configurable period
- Multiple consumer groups can read same messages
- Partitions for parallelism

### Exchange (RabbitMQ)
**Definition**: An entity that receives messages from producers and routes them to queues based on binding rules.

**Types**:
- **Direct**: Routes to queues with exact routing key match
- **Topic**: Routes to queues based on pattern matching
- **Fanout**: Routes to all bound queues (broadcast)
- **Headers**: Routes based on message headers

**Example in Our Project**:
```java
@Bean
public TopicExchange orderExchange() {
    return new TopicExchange("order.exchange");
}

@Bean
public Binding notificationBinding() {
    return BindingBuilder.bind(notificationQueue())
            .to(orderExchange())
            .with("notification.send");
}
```

---

## Event-Driven Architecture Basics

### What is Event-Driven Architecture?
Event-Driven Architecture (EDA) is a software architecture paradigm where services communicate by producing and consuming events. Events represent state changes or significant occurrences in the system.

### Key Concepts

#### 1. Events
Events are immutable facts about something that happened. They carry information about what occurred, when, and by whom.

**Types of Events**:
- **Domain Events**: Business-significant events (OrderPlaced, PaymentCompleted)
- **System Events**: Technical events (ServiceStarted, ErrorOccurred)
- **Integration Events**: Cross-service events (CustomerCreated, OrderShipped)

**Example**:
```java
public class OrderEvent {
    private String messageId;
    private String eventType;  // ORDER_PLACED, ORDER_CONFIRMED
    private Long orderId;
    private Long customerId;
    private LocalDateTime timestamp;
    // ... other fields
}
```

#### 2. Event Producers
Services that generate events when state changes occur.

#### 3. Event Consumers
Services that subscribe to and process events they're interested in.

#### 4. Event Channels
The mechanism that transports events from producers to consumers (message brokers).

### Event-Driven vs Request-Response

| Aspect | Request-Response | Event-Driven |
|--------|-----------------|--------------|
| Trigger | Explicit request | State change |
| Coupling | Tight | Loose |
| Timing | Synchronous | Asynchronous |
| Pattern | Call/Return | Publish/Subscribe |
| Knowledge | Caller knows callee | Producer doesn't know consumers |

### Benefits of Event-Driven Architecture

1. **Loose Coupling**: Services don't need to know about each other
2. **Scalability**: Easy to add new consumers without modifying producers
3. **Real-time**: Events processed as they occur
4. **Audit Trail**: All events logged for replay/analysis
5. **Flexibility**: Easy to add new event handlers

### Challenges

1. **Complexity**: Harder to debug and trace
2. **Eventual Consistency**: Data not immediately consistent across services
3. **Event Schema Evolution**: Need to handle changing event structures
4. **Monitoring**: Need specialized tools for event flow visibility

---

## Message Flow in a Real-World System

### Order Processing Flow Example

Let's trace how an order flows through our food delivery system using messaging:

```
┌─────────────────┐
│  Customer App   │
└────────┬────────┘
         │ 1. POST /api/orders
         ▼
┌─────────────────┐
│  Order Service  │ (Producer)
└────────┬────────┘
         │ 2. Save order to DB
         │ 3. Send ORDER_PLACED event
         ▼
┌─────────────────┐
│   RabbitMQ      │ (Broker)
└────────┬────────┘
         │ 4. Routes to queues
         ├─────────────────────┬──────────────────────┐
         ▼                     ▼                      ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Notification    │   │ Delivery        │   │ Analytics       │
│ Service         │   │ Partner Service │   │ Service         │
│ (Consumer)      │   │ (Consumer)      │   │ (Consumer)      │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                     │                      │
         │ 5. Send email       │ 6. Log assignment    │ 7. Update metrics
         ▼                     ▼                      ▼
    Customer notified     Partner assigned     Analytics updated
```

### Step-by-Step Flow

**Step 1**: Customer places order via API
```bash
POST /api/orders
{
  "customerId": 1,
  "restaurantId": 1,
  "totalAmount": 499.0,
  "paymentMethod": "UPI"
}
```

**Step 2**: Order Service receives request
```java
@PostMapping
public OrderResponseDto placeOrder(@RequestBody OrderRequestDto request) {
    return orderService.placeOrder(request);
}
```

**Step 3**: Order Service saves order and publishes event
```java
public OrderResponseDto placeOrder(OrderRequestDto request) {
    // Validate customer and restaurant
    customerClient.getCustomer(request.getCustomerId());
    restaurantClient.getRestaurant(request.getRestaurantId());
    
    // Save order
    Order order = Order.builder()
            .customerId(request.getCustomerId())
            .restaurantId(request.getRestaurantId())
            .totalAmount(request.getTotalAmount())
            .orderStatus(OrderStatus.PLACED)
            .build();
    order = orderRepository.save(order);
    
    // Publish event
    OrderEvent event = OrderEvent.createOrderPlacedEvent(
            order.getId(),
            order.getCustomerId(),
            order.getRestaurantId(),
            order.getTotalAmount()
    );
    messageProducer.sendOrderEvent(event);
    
    return orderMapper.toResponse(order);
}
```

**Step 4**: RabbitMQ receives and routes message
- Message sent to `order.exchange` with routing key `order.created`
- Exchange routes to bound queues based on routing key

**Step 5**: Notification Service consumes event
```java
@RabbitListener(queues = "notification.queue")
public void handleOrderEvent(OrderEvent event) {
    if (event.getEventType().equals("ORDER_PLACED")) {
        sendNotification(event.getCustomerId(), 
            "Order #" + event.getOrderId() + " placed successfully",
            "ORDER_PLACED");
    }
}
```

**Step 6**: Delivery Partner Service consumes event
```java
@RabbitListener(queues = "delivery.queue")
public void handleOrderEvent(OrderEvent event) {
    if (event.getEventType().equals("DELIVERY_ASSIGNED")) {
        updateDeliveryStatus(event.getDeliveryPartnerId(), 
            DeliveryStatus.ASSIGNED);
    }
}
```

**Step 7**: Analytics Service consumes event (if implemented)
```java
@RabbitListener(queues = "analytics.queue")
public void handleOrderEvent(OrderEvent event) {
    analyticsService.recordOrderEvent(event);
}
```

### Message Flow Diagram

```
Time →
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Order   │───▶│ RabbitMQ│───▶│ Notify  │───▶│ Email   │
│ Service │    │ Broker  │    │ Service │    │ Sent    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │
     │              └──────────────┼──────────────┐
     │                             │              │
     │                             ▼              ▼
     │                      ┌─────────┐    ┌─────────┐
     │                      │ Delivery │    │ Analytics│
     │                      │ Service  │    │ Service │
     │                      └─────────┘    └─────────┘
     │
     └──▶ Continues without waiting
```

---

## Loose Coupling Using Messaging

### What is Loose Coupling?
Loose coupling means services have minimal knowledge of each other's implementation details. Changes in one service don't require changes in others.

### How Messaging Achieves Loose Coupling

#### 1. **No Direct Dependencies**
Services don't call each other directly. They communicate through a broker.

**Before (Tight Coupling)**:
```java
// Order Service directly calls Notification Service
@RestController
public class OrderController {
    @Autowired
    private NotificationClient notificationClient;
    
    public void placeOrder(Order order) {
        // ... save order ...
        notificationClient.sendNotification(notification); // Direct call
    }
}
```

**After (Loose Coupling)**:
```java
// Order Service publishes event, doesn't know who consumes it
@Service
public class OrderServiceImpl {
    @Autowired
    private MessageProducer messageProducer;
    
    public void placeOrder(Order order) {
        // ... save order ...
        OrderEvent event = OrderEvent.createOrderPlacedEvent(...);
        messageProducer.sendOrderEvent(event); // Publishes to broker
    }
}
```

#### 2. **Independent Evolution**
- Order Service can change without affecting Notification Service
- New consumers can be added without modifying Order Service
- Consumers can be added/removed without affecting producers

#### 3. **Temporal Decoupling**
- Producer can send messages when consumer is down
- Consumer can process messages when producer is down
- Messages queued until consumer is available

#### 4. **Schema Independence**
- Producer and consumer agree on event schema
- Can evolve schema using versioning
- Consumers can ignore fields they don't need

### Example: Adding a New Service

**Scenario**: We want to add an Analytics Service to track order metrics.

**Without Messaging**:
1. Modify Order Service to call Analytics Service
2. Add Analytics Service dependency to Order Service
3. Handle failures in Order Service
4. Test both services together

**With Messaging**:
1. Create Analytics Service
2. Add consumer to listen to order events
3. No changes to Order Service needed
4. Deploy independently

```java
// New Analytics Service - no changes to Order Service needed!
@Component
public class AnalyticsEventConsumer {
    
    @RabbitListener(queues = "analytics.queue")
    public void handleOrderEvent(OrderEvent event) {
        analyticsService.recordOrderMetrics(event);
    }
}
```

### Coupling Comparison

| Aspect | Direct HTTP Calls | Messaging |
|--------|------------------|-----------|
| Service Knowledge | Knows specific endpoints | Knows only event schema |
| Deployment Order | Must deploy together | Can deploy independently |
| Failure Impact | Cascading failures | Isolated failures |
| Adding Consumers | Modify producer | Add consumer only |
| Removing Consumers | Modify producer | Remove consumer only |
| Version Management | API versioning | Event versioning |

---

## Handling Message Failures and Retries

### Types of Failures

1. **Transient Failures**: Temporary issues (network blip, broker restart)
2. **Permanent Failures**: Persistent issues (invalid data, bug in consumer)
3. **Broker Failures**: Broker unavailable or corrupted
4. **Consumer Failures**: Consumer crashes or throws exception

### Retry Strategies

#### 1. **Immediate Retry**
Retry immediately after failure. Good for transient issues.

#### 2. **Exponential Backoff**
Wait longer between each retry. Prevents overwhelming the system.

**Configuration in Our Project**:
```yaml
spring:
  rabbitmq:
    listener:
      simple:
        retry:
          enabled: true
          max-attempts: 3
          initial-interval: 1000    # 1 second
          multiplier: 2.0           # Double each time
          max-interval: 10000       # Max 10 seconds
```

**Retry Timeline**:
- Attempt 1: Immediate
- Attempt 2: Wait 1 second
- Attempt 3: Wait 2 seconds
- Attempt 4: Wait 4 seconds
- Attempt 5: Wait 8 seconds
- Attempt 6: Wait 10 seconds (max)

#### 3. **Dead Letter Queue (DLQ)**
After max retries, move message to DLQ for manual inspection.

**Configuration in Our Project**:
```java
@Bean
public Queue notificationQueue() {
    return QueueBuilder.durable("notification.queue")
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", "notification.dlq")
            .build();
}
```

**Message Flow with DLQ**:
```
Main Queue → Retry 1 → Retry 2 → Retry 3 → DLQ
```

### Failure Handling in Our Implementation

#### Producer Side
```java
public void sendOrderEvent(OrderEvent event) {
    try {
        amqpTemplate.convertAndSend(
                RabbitMQConfig.ORDER_EXCHANGE,
                RabbitMQConfig.ORDER_ROUTING_KEY,
                event
        );
        log.info("Order event sent successfully: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Failed to send order event: messageId={}", event.getMessageId(), e);
        throw new RuntimeException("Failed to send order event", e);
    }
}
```

#### Consumer Side
```java
@RabbitListener(queues = "notification.queue")
public void handleOrderEvent(OrderEvent event) {
    try {
        // Process message
        processEvent(event);
        
        // Auto-acknowledge on success
    } catch (Exception e) {
        log.error("Error processing order event: messageId={}", event.getMessageId(), e);
        throw e; // Re-throw to trigger retry
    }
}
```

### Publisher Confirms
Ensures message was received by broker.

```java
@Bean
public AmqpTemplate template(ConnectionFactory connectionFactory) {
    RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
    
    rabbitTemplate.setConfirmCallback((correlationData, ack, cause) -> {
        if (ack) {
            log.info("Message received by broker");
        } else {
            log.error("Message not received by broker: {}", cause);
        }
    });
    
    return rabbitTemplate;
}
```

### Monitoring Failed Messages

**DLQ Inspection**:
```bash
# RabbitMQ Management UI
http://localhost:15672

# Navigate to Queues → notification.dlq
# View failed messages
# Can requeue or delete
```

**Programmatic DLQ Processing**:
```java
@Component
public class DlqProcessor {
    
    @RabbitListener(queues = "notification.dlq")
    public void processDlqMessage(Message message) {
        // Log for investigation
        log.error("Message in DLQ: {}", message);
        
        // Send alert to operations team
        alertService.sendAlert("Message in DLQ: " + message);
    }
}
```

### Best Practices

1. **Set reasonable retry limits** (3-5 retries)
2. **Use exponential backoff** to prevent thundering herd
3. **Implement DLQ** for failed messages
4. **Monitor DLQ** and set up alerts
5. **Make consumers idempotent** to handle duplicates
6. **Log all failures** with sufficient context
7. **Implement circuit breakers** for permanent failures

---

## Idempotency and Duplicate Message Handling

### What is Idempotency?
An operation is idempotent if performing it multiple times has the same effect as performing it once.

**Mathematical Definition**: f(x) = f(f(x))

### Why Idempotency Matters in Messaging

Messages can be delivered multiple times due to:
- Network retries
- Consumer crashes after processing but before acknowledgment
- Broker redelivery
- Manual requeue from DLQ

Without idempotency, duplicate messages can cause:
- Duplicate database records
- Duplicate email notifications
- Incorrect financial transactions
- Data corruption

### Idempotency Strategies

#### 1. **Unique Message IDs**
Each message has a unique ID. Consumer tracks processed IDs.

**Implementation in Our Project**:
```java
@Component
public class IdempotencyHandler {
    
    private final ConcurrentMap<String, ProcessedMessage> processedMessages 
        = new ConcurrentHashMap<>();
    
    public boolean isMessageProcessed(String messageId) {
        ProcessedMessage processed = processedMessages.get(messageId);
        if (processed == null) {
            return false;
        }
        
        // Check if expired
        if (System.currentTimeMillis() - processed.getTimestamp() > MESSAGE_TTL_MS) {
            processedMessages.remove(messageId);
            return false;
        }
        
        return true;
    }
    
    public void markMessageAsProcessed(String messageId) {
        processedMessages.put(messageId, 
            new ProcessedMessage(messageId, System.currentTimeMillis()));
    }
}
```

**Usage in Consumer**:
```java
@RabbitListener(queues = "notification.queue")
public void handleOrderEvent(OrderEvent event) {
    // Check if already processed
    if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
        log.info("Skipping duplicate message: messageId={}", event.getMessageId());
        return;
    }
    
    try {
        // Process message
        sendNotification(...);
        
        // Mark as processed
        idempotencyHandler.markMessageAsProcessed(event.getMessageId());
    } catch (Exception e) {
        // Don't mark as processed on failure
        throw e;
    }
}
```

#### 2. **Database Unique Constraints**
Use database constraints to prevent duplicate records.

```sql
CREATE TABLE notifications (
    id BIGINT PRIMARY KEY,
    message_id VARCHAR(255) UNIQUE,  -- Ensures no duplicates
    user_id BIGINT,
    message TEXT,
    created_at TIMESTAMP
);
```

```java
try {
    notificationRepository.save(notification);
} catch (DuplicateKeyException e) {
    log.info("Duplicate notification, skipping: messageId={}", messageId);
}
```

#### 3. **Conditional Updates**
Check if operation already performed before executing.

```java
public void updateOrderStatus(Long orderId, OrderStatus status) {
    int updated = orderRepository.updateStatusIfNotAlready(
        orderId, 
        status, 
        status  // Only update if not already this status
    );
    
    if (updated == 0) {
        log.info("Order already has status: {}", status);
    }
}
```

#### 4. **Business Logic Idempotency**
Design operations to be naturally idempotent.

```java
// Not idempotent - adds amount each time
public void creditAccount(Long accountId, BigDecimal amount) {
    account.setBalance(account.getBalance().add(amount));
}

// Idempotent - sets to specific amount
public void setAccountBalance(Long accountId, BigDecimal amount) {
    account.setBalance(amount);
}
```

### Idempotency in Our Project

**Event Structure**:
```java
@Data
public class OrderEvent {
    private String messageId;      // Unique ID for idempotency
    private String eventType;
    private Long orderId;
    private Long customerId;
    private LocalDateTime timestamp;
    private String correlationId;  // For tracing
}
```

**Consumer Implementation**:
```java
@Component
public class OrderEventConsumer {
    
    private final IdempotencyHandler idempotencyHandler;
    
    @RabbitListener(queues = "notification.queue")
    public void handleOrderEvent(OrderEvent event) {
        // Idempotency check
        if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
            log.info("Skipping duplicate message: messageId={}", event.getMessageId());
            return;
        }
        
        try {
            // Process event
            processEvent(event);
            
            // Mark as processed only on success
            idempotencyHandler.markMessageAsProcessed(event.getMessageId());
        } catch (Exception e) {
            log.error("Error processing event: messageId={}", event.getMessageId(), e);
            throw e; // Trigger retry
        }
    }
}
```

### Message Deduplication vs Idempotency

| Aspect | Deduplication | Idempotency |
|--------|---------------|-------------|
| Focus | Prevent duplicate processing | Safe to process multiple times |
| Implementation | Filter duplicates before processing | Handle duplicates safely |
| Storage | Need to track processed IDs | May not need storage |
| Scope | Message-level | Operation-level |

**Best Practice**: Use both when possible
- Deduplication to avoid unnecessary processing
- Idempotency as safety net

### Handling Exactly-Once Semantics

True exactly-once delivery is difficult. The industry standard is:
- **At-least-once delivery** (messages may be duplicated)
- **Idempotent consumers** (handle duplicates safely)

This combination provides effective exactly-once semantics from the business perspective.

---

## High-Level Comparison: Kafka vs RabbitMQ

### Architecture Comparison

| Aspect | RabbitMQ | Kafka |
|--------|----------|-------|
| Type | Message Broker | Event Streaming Platform |
| Model | Queue-based | Log-based |
| Message Retention | Until consumed | Configurable time/size |
| Consumer Model | Competing consumers | Consumer groups |
| Ordering | Per-queue | Per-partition |
| Throughput | Medium (20K-50K msg/sec) | High (millions msg/sec) |
| Latency | Low (microseconds) | Low (milliseconds) |
| Persistence | Optional | Built-in |
| Routing | Flexible (exchanges) | Simple (topics) |
| Protocols | AMQP, MQTT, STOMP | Custom TCP |

### When to Use RabbitMQ

**Use RabbitMQ when**:
- You need complex routing patterns
- You require reliable message delivery with acknowledgments
- You need flexible message routing (direct, topic, fanout)
- You have moderate throughput requirements
- You need message TTL and dead letter queues
- You want simpler setup and management

**Ideal for**:
- Traditional messaging patterns
- Work queues
- Publish/subscribe with routing
- Request-reply patterns
- Transactional messaging

### When to Use Kafka

**Use Kafka when**:
- You need high throughput (millions of messages/sec)
- You need message replay (reprocess old messages)
- You need event sourcing
- You need stream processing
- You have multiple consumer groups reading same data
- You need durable log storage

**Ideal for**:
- Event streaming
- Real-time analytics
- Log aggregation
- Event sourcing
- Stream processing (Kafka Streams, ksqlDB)

### Feature Comparison

#### Message Retention
**RabbitMQ**:
- Messages removed after acknowledgment
- Optional persistence to disk
- TTL can expire messages

**Kafka**:
- Messages retained for configured period (default 7 days)
- All messages available for replay
- Can retain based on time or size

#### Consumer Model
**RabbitMQ**:
- Competing consumers on same queue
- Each message delivered to one consumer
- Multiple queues for different consumers

**Kafka**:
- Consumer groups
- Each group gets all messages
- Within group, partitions distributed

#### Ordering Guarantees
**RabbitMQ**:
- FIFO per queue
- Global ordering with single queue
- No ordering across multiple queues

**Kafka**:
- FIFO per partition
- Global ordering with single partition
- Parallel processing with multiple partitions

#### Complexity
**RabbitMQ**:
- Simpler to set up
- Easier to understand
- Good for traditional messaging

**Kafka**:
- More complex setup
- Requires understanding of partitions, offsets, consumer groups
- Steeper learning curve

### Performance Comparison

| Metric | RabbitMQ | Kafka |
|--------|----------|-------|
| Throughput | ~50K msg/sec | ~1M+ msg/sec |
| Latency | < 1ms | ~2-5ms |
| Storage | RAM + optional disk | Disk (log) |
| Network | TCP | TCP |
| CPU Usage | Low | Medium |
| Memory Usage | Medium | Low |

### Ecosystem

**RabbitMQ**:
- Management UI
- Spring Boot integration
- Multiple language clients
- Plugins for extensions

**Kafka**:
- Kafka Connect (integration)
- Kafka Streams (processing)
- ksqlDB (SQL interface)
- Schema Registry
- Multiple language clients

### Decision Matrix

| Requirement | RabbitMQ | Kafka |
|-------------|----------|-------|
| Simple messaging | ✅ | ✅ |
| Complex routing | ✅ | ❌ |
| High throughput | ❌ | ✅ |
| Message replay | ❌ | ✅ |
| Event sourcing | ❌ | ✅ |
| Stream processing | ❌ | ✅ |
| Simple setup | ✅ | ❌ |
| Low latency | ✅ | ✅ |
| Multiple consumer groups | ❌ | ✅ |

### Our Choice: RabbitMQ

**Reasons**:
1. **Simpler integration** with Spring Boot
2. **Flexible routing** for our use case
3. **Reliable delivery** with acknowledgments
4. **DLQ support** for failed messages
5. **Sufficient throughput** for food delivery use case
6. **Easier to learn** and maintain

---

## Real-World Use Cases

### 1. Order Processing

**Scenario**: When a customer places an order, multiple services need to be notified.

**Without Messaging**:
```java
// Order Service calls each service synchronously
public void placeOrder(Order order) {
    orderRepository.save(order);
    paymentService.processPayment(order);  // Blocks
    notificationService.sendNotification(order);  // Blocks
    inventoryService.updateInventory(order);  // Blocks
    analyticsService.trackOrder(order);  // Blocks
}
```

**Problems**:
- Slow response time (sum of all service times)
- If any service is down, order fails
- Tight coupling between services

**With Messaging**:
```java
// Order Service publishes event, continues immediately
public void placeOrder(Order order) {
    orderRepository.save(order);
    
    OrderEvent event = OrderEvent.createOrderPlacedEvent(order);
    messageProducer.sendOrderEvent(event);
    
    // Returns immediately
}
```

**Benefits**:
- Fast response time
- Order succeeds even if downstream services are down
- Easy to add new consumers

### 2. Notifications

**Scenario**: Send notifications via multiple channels (email, SMS, push).

**Implementation**:
```java
@Component
public class NotificationEventConsumer {
    
    @RabbitListener(queues = "notification.queue")
    public void handleNotificationEvent(NotificationEvent event) {
        switch (event.getChannel()) {
            case "EMAIL":
                emailService.send(event);
                break;
            case "SMS":
                smsService.send(event);
                break;
            case "PUSH":
                pushService.send(event);
                break;
        }
    }
}
```

**Benefits**:
- Can retry failed notifications
- Can add new channels without modifying order service
- Can prioritize channels (SMS urgent, email normal)

### 3. Audit Logging

**Scenario**: Track all important events for compliance and debugging.

**Implementation**:
```java
@Component
public class AuditEventConsumer {
    
    @RabbitListener(queues = "audit.queue")
    public void handleAuditEvent(Event event) {
        AuditLog log = AuditLog.builder()
                .eventType(event.getEventType())
                .payload(event.toString())
                .timestamp(event.getTimestamp())
                .userId(event.getUserId())
                .build();
        
        auditLogRepository.save(log);
    }
}
```

**Benefits**:
- Centralized audit trail
- Can replay events for debugging
- Compliance with regulations
- Can analyze patterns

### 4. Data Synchronization

**Scenario**: Keep search index in sync with main database.

**Implementation**:
```java
// When order updated, publish event
public void updateOrder(Order order) {
    orderRepository.save(order);
    
    OrderEvent event = OrderEvent.createOrderUpdatedEvent(order);
    messageProducer.sendOrderEvent(event);
}

// Search service updates index
@Component
public class SearchIndexConsumer {
    
    @RabbitListener(queues = "search.queue")
    public void handleOrderEvent(OrderEvent event) {
        searchIndexService.updateDocument(event);
    }
}
```

**Benefits**:
- Eventually consistent
- Can rebuild index from event log
- Decouples database from search

### 5. Payment Processing

**Scenario**: Process payments asynchronously with retries.

**Implementation**:
```java
@Component
public class PaymentEventConsumer {
    
    @RabbitListener(queues = "payment.queue")
    public void handlePaymentEvent(PaymentEvent event) {
        try {
            paymentGateway.process(event);
            
            // Mark as processed
            idempotencyHandler.markAsProcessed(event.getMessageId());
        } catch (PaymentGatewayException e) {
            // Retry automatically
            throw e;
        } catch (Exception e) {
            // Permanent failure, move to DLQ
            throw e;
        }
    }
}
```

**Benefits**:
- Automatic retries for transient failures
- Manual inspection of permanent failures
- Idempotency prevents duplicate charges

### 6. Delivery Tracking

**Scenario**: Track delivery status updates in real-time.

**Implementation**:
```java
// Delivery partner app sends location updates
public void updateLocation(DeliveryLocation location) {
    DeliveryEvent event = DeliveryEvent.createLocationUpdateEvent(location);
    messageProducer.sendDeliveryEvent(event);
}

// Multiple consumers track location
@Component
public class TrackingConsumer {
    @RabbitListener(queues = "tracking.queue")
    public void handleLocationEvent(DeliveryEvent event) {
        trackingService.updateRealTimeLocation(event);
    }
}

@Component
public class ETACalculatorConsumer {
    @RabbitListener(queues = "eta.queue")
    public void handleLocationEvent(DeliveryEvent event) {
        etaService.recalculateETA(event);
    }
}
```

**Benefits**:
- Real-time updates
- Multiple independent calculations
- Can add new tracking features easily

---

## Implementation in This Project

### Overview

We've implemented a complete messaging system using RabbitMQ in the food delivery microservices platform. Here's what was built:

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  MySQL   │  │ RabbitMQ │  │ Eureka   │  │  Config  │   │
│  │  :3307   │  │  :5672   │  │  :8761   │  │  :8888   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌──────▼────────┐  ┌──────▼────────┐
│ Order Service   │  │ Notification  │  │ Delivery      │
│ (Producer)      │  │ Service       │  │ Partner       │
│                 │  │ (Consumer)    │  │ Service       │
│ - Sends events  │  │ - Receives    │  │ (Consumer)    │
│ - ORDER_PLACED  │  │   events      │  │ - Receives    │
│ - ORDER_CONFIRM │  │ - Sends       │  │   events      │
│ - ORDER_DELIVER │  │   notifications│  │ - Updates     │
│ - DELIVERY_ASSGN│  │               │  │   status      │
└─────────────────┘  └───────────────┘  └────────────────┘
```

### Components Implemented

#### 1. Infrastructure (docker-compose.yml)

**RabbitMQ Service**:
```yaml
rabbitmq:
  image: rabbitmq:3.12-management
  container_name: fd-rabbitmq
  ports:
    - "5672:5672"   # AMQP port
    - "15672:15672" # Management UI
  environment:
    RABBITMQ_DEFAULT_USER: admin
    RABBITMQ_DEFAULT_PASS: admin
  healthcheck:
    test: ["CMD", "rabbitmq-diagnostics", "ping"]
```

**Access**:
- AMQP: `localhost:5672`
- Management UI: `http://localhost:15672` (admin/admin)

#### 2. Common Library (common-lib)

**RabbitMQ Configuration**:
```java
@Configuration
public class RabbitMQConfig {
    public static final String ORDER_EXCHANGE = "order.exchange";
    public static final String ORDER_QUEUE = "order.queue";
    public static final String NOTIFICATION_QUEUE = "notification.queue";
    public static final String DELIVERY_QUEUE = "delivery.queue";
    
    // Dead Letter Queues
    public static final String ORDER_DLQ = "order.dlq";
    public static final String NOTIFICATION_DLQ = "notification.dlq";
    public static final String DELIVERY_DLQ = "delivery.dlq";
    
    @Bean
    public TopicExchange orderExchange() {
        return new TopicExchange(ORDER_EXCHANGE);
    }
    
    @Bean
    public Queue notificationQueue() {
        return QueueBuilder.durable(NOTIFICATION_QUEUE)
                .withArgument("x-dead-letter-exchange", "")
                .withArgument("x-dead-letter-routing-key", NOTIFICATION_DLQ)
                .build();
    }
    
    // ... other queues and bindings
}
```

**Event DTOs**:
```java
// OrderEvent.java
@Data
public class OrderEvent {
    private String messageId;
    private String eventType;
    private Long orderId;
    private Long customerId;
    private Long restaurantId;
    private Long deliveryPartnerId;
    private BigDecimal totalAmount;
    private OrderStatus orderStatus;
    private LocalDateTime timestamp;
    private String correlationId;
    
    public static OrderEvent createOrderPlacedEvent(...) { ... }
    public static OrderEvent createOrderConfirmedEvent(...) { ... }
    public static OrderEvent createOrderDeliveredEvent(...) { ... }
    public static OrderEvent createDeliveryAssignmentEvent(...) { ... }
}
```

**Message Producer**:
```java
@Service
public class MessageProducer {
    private final AmqpTemplate amqpTemplate;
    
    public void sendOrderEvent(OrderEvent event) {
        log.info("Sending order event: {} for order: {}", 
            event.getEventType(), event.getOrderId());
        amqpTemplate.convertAndSend(
            RabbitMQConfig.ORDER_EXCHANGE,
            RabbitMQConfig.ORDER_ROUTING_KEY,
            event
        );
    }
}
```

**Retry Configuration**:
```java
@Configuration
public class RabbitMQRetryConfig {
    @Bean
    public RetryOperationsInterceptor retryInterceptor() {
        return RetryInterceptorBuilder.stateless()
                .maxAttempts(3)
                .backOffOptions(1000, 2.0, 10000)
                .recoverer(messageRecoverer())
                .build();
    }
}
```

**Idempotency Handler**:
```java
@Component
public class IdempotencyHandler {
    private final ConcurrentMap<String, ProcessedMessage> processedMessages;
    
    public boolean isMessageProcessed(String messageId) { ... }
    public void markMessageAsProcessed(String messageId) { ... }
    public void cleanupExpiredMessages() { ... }
}
```

#### 3. Order Service (Producer)

**Dependencies Added**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

**Configuration Updated**:
```yaml
# config-repo/order-service.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: admin
```

**Service Implementation**:
```java
@Service
public class OrderServiceImpl {
    private final MessageProducer messageProducer;
    
    public OrderResponseDto placeOrder(OrderRequestDto request) {
        // ... validate and save order ...
        
        // Send ORDER_PLACED event
        OrderEvent orderPlacedEvent = OrderEvent.createOrderPlacedEvent(
            order.getId(), order.getCustomerId(), 
            order.getRestaurantId(), order.getTotalAmount()
        );
        messageProducer.sendOrderEvent(orderPlacedEvent);
        
        // ... process payment ...
        
        // Send ORDER_CONFIRMED event
        OrderEvent orderConfirmedEvent = OrderEvent.createOrderConfirmedEvent(...);
        messageProducer.sendOrderEvent(orderConfirmedEvent);
        
        return orderMapper.toResponse(order);
    }
    
    public OrderResponseDto assignDelivery(Long id) {
        // ... assign delivery partner ...
        
        // Send DELIVERY_ASSIGNED event
        OrderEvent deliveryAssignmentEvent = OrderEvent.createDeliveryAssignmentEvent(...);
        messageProducer.sendOrderEvent(deliveryAssignmentEvent);
        
        return orderMapper.toResponse(order);
    }
    
    public OrderResponseDto updateStatus(Long id, OrderStatusUpdateRequestDto request) {
        // ... update status ...
        
        if (request.getOrderStatus() == OrderStatus.DELIVERED) {
            // Send ORDER_DELIVERED event
            OrderEvent orderDeliveredEvent = OrderEvent.createOrderDeliveredEvent(...);
            messageProducer.sendOrderEvent(orderDeliveredEvent);
        }
        
        return orderMapper.toResponse(order);
    }
}
```

#### 4. Notification Service (Consumer)

**Dependencies Added**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

**Configuration Updated**:
```yaml
# config-repo/notification-service.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: admin
```

**Event Consumer**:
```java
@Component
public class OrderEventConsumer {
    private final NotificationService notificationService;
    private final IdempotencyHandler idempotencyHandler;
    
    @RabbitListener(queues = "notification.queue")
    public void handleOrderEvent(OrderEvent event) {
        log.info("Received order event: {} for order: {}", 
            event.getEventType(), event.getOrderId());
        
        // Idempotency check
        if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
            log.info("Skipping duplicate message: messageId={}", event.getMessageId());
            return;
        }
        
        try {
            switch (event.getEventType()) {
                case "ORDER_PLACED":
                    sendNotification(event.getCustomerId(), 
                        "Order #" + event.getOrderId() + " placed successfully", 
                        "ORDER_PLACED");
                    break;
                case "ORDER_CONFIRMED":
                    sendNotification(event.getCustomerId(), 
                        "Order #" + event.getOrderId() + " confirmed by restaurant", 
                        "ORDER_CONFIRMED");
                    break;
                case "ORDER_DELIVERED":
                    sendNotification(event.getCustomerId(), 
                        "Order #" + event.getOrderId() + " has been delivered", 
                        "ORDER_DELIVERED");
                    break;
                default:
                    log.warn("Unknown event type: {}", event.getEventType());
            }
            
            // Mark as processed
            idempotencyHandler.markMessageAsProcessed(event.getMessageId());
            log.info("Successfully processed order event: messageId={}", event.getMessageId());
        } catch (Exception e) {
            log.error("Error processing order event: messageId={}, error={}", 
                event.getMessageId(), e.getMessage(), e);
            throw e; // Trigger retry
        }
    }
}
```

#### 5. Delivery Partner Service (Consumer)

**Dependencies Added**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

**Configuration Updated**:
```yaml
# config-repo/delivery-partner-service.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: admin
```

**Event Consumer**:
```java
@Component
public class OrderEventConsumer {
    private final DeliveryPartnerService deliveryPartnerService;
    private final IdempotencyHandler idempotencyHandler;
    
    @RabbitListener(queues = "delivery.queue")
    public void handleOrderEvent(OrderEvent event) {
        log.info("Received order event: {} for order: {}", 
            event.getEventType(), event.getOrderId());
        
        // Idempotency check
        if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
            log.info("Skipping duplicate message: messageId={}", event.getMessageId());
            return;
        }
        
        try {
            switch (event.getEventType()) {
                case "DELIVERY_ASSIGNED":
                    updateDeliveryStatus(event.getDeliveryPartnerId(), 
                        DeliveryStatus.ASSIGNED);
                    break;
                case "ORDER_DELIVERED":
                    updateDeliveryStatus(event.getDeliveryPartnerId(), 
                        DeliveryStatus.AVAILABLE);
                    break;
                default:
                    log.warn("Unknown event type: {}", event.getEventType());
            }
            
            // Mark as processed
            idempotencyHandler.markMessageAsProcessed(event.getMessageId());
            log.info("Successfully processed order event: messageId={}", event.getMessageId());
        } catch (Exception e) {
            log.error("Error processing order event: messageId={}, error={}", 
                event.getMessageId(), e.getMessage(), e);
            throw e; // Trigger retry
        }
    }
}
```

### Message Flow in Implementation

```
1. Customer places order
   ↓
2. Order Service saves order
   ↓
3. Order Service sends ORDER_PLACED event to RabbitMQ
   ↓
4. RabbitMQ routes to notification.queue and delivery.queue
   ↓
5. Notification Service consumes ORDER_PLACED
   - Checks idempotency
   - Sends email to customer
   - Marks message as processed
   ↓
6. Order Service processes payment
   ↓
7. Order Service sends ORDER_CONFIRMED event
   ↓
8. Notification Service consumes ORDER_CONFIRMED
   - Sends confirmation email
   ↓
9. Order Service assigns delivery partner
   ↓
10. Order Service sends DELIVERY_ASSIGNED event
   ↓
11. Delivery Partner Service consumes DELIVERY_ASSIGNED
   - Updates partner status to ASSIGNED
   ↓
12. Order delivered
   ↓
13. Order Service sends ORDER_DELIVERED event
   ↓
14. Notification Service consumes ORDER_DELIVERED
   - Sends delivery confirmation email
   ↓
15. Delivery Partner Service consumes ORDER_DELIVERED
   - Updates partner status to AVAILABLE
```

### Configuration Files

**RabbitMQ Configuration** (config-repo/rabbitmq.yml):
```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: admin
    listener:
      simple:
        acknowledge-mode: auto
        retry:
          enabled: true
          max-attempts: 3
          initial-interval: 1000
          multiplier: 2.0
          max-interval: 10000
        default-requeue-rejected: false
    publisher-confirm-type: correlated
    publisher-returns: true
```

### Testing the Implementation

**1. Start Services**:
```bash
docker-compose up -d
```

**2. Access RabbitMQ Management UI**:
```
http://localhost:15672
Username: admin
Password: admin
```

**3. Place an Order**:
```bash
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 1,
    "restaurantId": 1,
    "totalAmount": 499.0,
    "paymentMethod": "UPI"
  }'
```

**4. Monitor Queues in RabbitMQ UI**:
- Navigate to Queues tab
- View message rates
- Check for messages in DLQ

**5. Check Logs**:
```bash
docker logs fd-order
docker logs fd-notification
docker logs fd-delivery
```

### Key Features Implemented

✅ **Message Broker Integration**: RabbitMQ with management UI
✅ **Event-Driven Communication**: Order events published to multiple consumers
✅ **Retry Mechanism**: Automatic retries with exponential backoff
✅ **Dead Letter Queues**: Failed messages moved to DLQ for inspection
✅ **Idempotency**: Message ID tracking to prevent duplicate processing
✅ **Loose Coupling**: Services communicate through events, not direct calls
✅ **Publisher Confirms**: Ensures messages reach the broker
✅ **Flexible Routing**: Topic exchange with multiple queues
✅ **Configuration Management**: Centralized RabbitMQ configuration

### Benefits Achieved

1. **Decoupling**: Order Service doesn't need to know about notification or delivery services
2. **Resilience**: If notification service is down, orders still succeed
3. **Scalability**: Multiple consumer instances can process messages in parallel
4. **Reliability**: Messages persisted and retried on failure
5. **Observability**: RabbitMQ UI provides visibility into message flow
6. **Flexibility**: Easy to add new consumers without modifying producers

### Future Enhancements

1. **Event Sourcing**: Store all events in a database for replay
2. **Schema Registry**: Use Avro/Protobuf for event schema evolution
3. **Message Tracing**: Add distributed tracing (Zipkin/Jaeger)
4. **Metrics**: Add Prometheus metrics for message rates
5. **Circuit Breakers**: Add resilience patterns for consumer failures
6. **Batch Processing**: Process multiple messages together for efficiency
7. **Message Compression**: Compress large messages
8. **Security**: Add TLS encryption for message transport

---

## Summary

This messaging implementation provides a robust foundation for event-driven communication in the food delivery microservices platform. It demonstrates:

- **Core messaging concepts** (producer, consumer, broker, queues)
- **Event-driven architecture** patterns
- **Reliability mechanisms** (retries, DLQ, idempotency)
- **Loose coupling** between services
- **Real-world use cases** (order processing, notifications, delivery tracking)

The system is production-ready with proper error handling, monitoring, and configuration management. It can be extended to support additional consumers and event types as the platform grows.
