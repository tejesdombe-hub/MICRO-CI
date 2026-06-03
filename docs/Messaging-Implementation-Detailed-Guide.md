# Messaging Implementation Detailed Guide

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [RabbitMQ Configuration](#rabbitmq-configuration)
4. [Message Events](#message-events)
5. [Message Producer](#message-producer)
6. [Message Consumers](#message-consumers)
7. [Idempotency Handling](#idempotency-handling)
8. [Retry Mechanism](#retry-mechanism)
9. [Dead Letter Queue](#dead-letter-queue)
10. [Configuration Files](#configuration-files)
11. [Message Flow](#message-flow)
12. [Best Practices](#best-practices)

---

## Overview

This messaging system implements an event-driven architecture using **RabbitMQ** as the message broker. It enables asynchronous communication between microservices in the food delivery system, allowing services to communicate without direct coupling.

### Key Components

- **RabbitMQ**: Message broker that routes messages between producers and consumers
- **Exchanges**: Receive messages from producers and route them to queues
- **Queues**: Store messages until they are consumed
- **Bindings**: Rules that connect exchanges to queues using routing keys
- **Message Producer**: Service that publishes events to RabbitMQ
- **Message Consumers**: Services that listen to and process messages from queues
- **Idempotency Handler**: Ensures messages are processed only once
- **Retry Mechanism**: Automatically retries failed message processing
- **Dead Letter Queue (DLQ)**: Stores messages that failed after all retry attempts

### Why RabbitMQ?

RabbitMQ was chosen because:
- **Reliability**: Guarantees message delivery with acknowledgments
- **Flexibility**: Supports multiple messaging patterns (direct, topic, fanout)
- **Scalability**: Handles high throughput with clustering
- **Durability**: Messages survive broker restarts
- **Routing**: Complex routing rules with exchanges and bindings
- **Protocol Support**: AMQP protocol for standardized messaging

---

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Order Service                              │
│                   (Message Producer)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Publishes Events
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RabbitMQ Broker                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              order.exchange (Topic Exchange)            │  │
│  └──────────────┬──────────────────────────┬────────────────┘  │
│                 │                          │                    │
│                 │ Routing Keys             │                    │
│                 │                          │                    │
│         ┌───────▼────────┐        ┌────────▼────────┐           │
│         │ order.created  │        │notification.send │          │
│         └───────┬────────┘        └────────┬────────┘           │
│                 │                          │                    │
│         ┌───────▼────────┐        ┌────────▼────────┐           │
│         │  order.queue   │        │notification.queue│          │
│         └───────┬────────┘        └────────┬────────┘           │
│                 │                          │                    │
│         ┌───────▼────────┐        ┌────────▼────────┐           │
│         │   DLQ          │        │     DLQ         │           │
│         └────────────────┘        └─────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
         │                          │
         │ Consumes                 │ Consumes
         │                          │
         ↓                          ↓
┌──────────────────┐    ┌──────────────────────┐
│ Delivery Partner  │    │ Notification Service │
│     Service       │    │   (Consumer)         │
└──────────────────┘    └──────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Order Service** | Produces events when order state changes |
| **RabbitMQ** | Routes and stores messages reliably |
| **Delivery Partner Service** | Consumes delivery-related events |
| **Notification Service** | Consumes events to send notifications |
| **Common Library** | Shared messaging infrastructure |

---

## RabbitMQ Configuration

### File: `RabbitMQConfig.java`

Location: `common-lib/src/main/java/com/fooddelivery/common/messaging/config/RabbitMQConfig.java`

This configuration class sets up all RabbitMQ components required for the messaging system.

### Package Declaration

```java
package com.fooddelivery.common.messaging.config;
```

- **Purpose**: Declares the package where this class resides
- **Package Path**: `com.fooddelivery.common.messaging.config`
- **Explanation**: This class is part of the common library's messaging configuration package, making it available to all microservices that depend on the common library.

### Imports

```java
import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
```

- **`org.springframework.amqp.core.*`**: Imports core AMQP (Advanced Message Queuing Protocol) classes including Exchange, Queue, Binding, and other fundamental RabbitMQ components
- **`ConnectionFactory`**: Interface for creating connections to RabbitMQ broker
- **`RabbitTemplate`**: Template class for simplifying RabbitMQ operations (sending and receiving messages)
- **`Jackson2JsonMessageConverter`**: Converts Java objects to JSON format for message serialization
- **`MessageConverter`**: Interface for message conversion between Java objects and AMQP messages
- **`@Bean`**: Spring annotation that indicates a method produces a bean to be managed by the Spring container
- **`@Configuration`**: Spring annotation that indicates this class contains configuration definitions

### Class Declaration

```java
@Configuration
public class RabbitMQConfig {
```

- **`@Configuration`**: Marks this class as a configuration class, allowing Spring to process it for bean definitions
- **`public`**: Access modifier allowing this class to be accessed from anywhere
- **`class`**: Keyword indicating this is a class definition
- **`RabbitMQConfig`**: Name of the configuration class

### Constants - Exchange and Queue Names

```java
public static final String ORDER_EXCHANGE = "order.exchange";
public static final String ORDER_QUEUE = "order.queue";
public static final String ORDER_ROUTING_KEY = "order.created";
public static final String NOTIFICATION_QUEUE = "notification.queue";
public static final String NOTIFICATION_ROUTING_KEY = "notification.send";
public static final String DELIVERY_QUEUE = "delivery.queue";
public static final String DELIVERY_ROUTING_KEY = "delivery.assign";
public static final String ORDER_DLQ = "order.dlq";
public static final String NOTIFICATION_DLQ = "notification.dlq";
public static final String DELIVERY_DLQ = "delivery.dlq";
```

#### Detailed Explanation of Each Constant:

**`ORDER_EXCHANGE = "order.exchange"`**
- **Purpose**: Name of the main exchange for order-related events
- **Type**: Topic Exchange (allows flexible routing with wildcard patterns)
- **Explanation**: All order-related events are published to this exchange, which then routes them to appropriate queues based on routing keys

**`ORDER_QUEUE = "order.queue"`**
- **Purpose**: Queue that holds order-related messages
- **Explanation**: Messages with routing key "order.created" are routed to this queue for processing

**`ORDER_ROUTING_KEY = "order.created"`**
- **Purpose**: Routing key for order creation events
- **Explanation**: When a message is published with this routing key, the exchange routes it to the order queue

**`NOTIFICATION_QUEUE = "notification.queue"`**
- **Purpose**: Queue that holds notification-related messages
- **Explanation**: Messages with routing key "notification.send" are routed to this queue for the notification service to process

**`NOTIFICATION_ROUTING_KEY = "notification.send"`**
- **Purpose**: Routing key for notification events
- **Explanation**: When a message is published with this routing key, the exchange routes it to the notification queue

**`DELIVERY_QUEUE = "delivery.queue"`**
- **Purpose**: Queue that holds delivery-related messages
- **Explanation**: Messages with routing key "delivery.assign" are routed to this queue for the delivery partner service to process

**`DELIVERY_ROUTING_KEY = "delivery.assign"`**
- **Purpose**: Routing key for delivery assignment events
- **Explanation**: When a message is published with this routing key, the exchange routes it to the delivery queue

**`ORDER_DLQ = "order.dlq"`**
- **Purpose**: Dead Letter Queue for order messages
- **Explanation**: Messages that fail processing after all retry attempts are moved to this queue for manual inspection and reprocessing

**`NOTIFICATION_DLQ = "notification.dlq"`**
- **Purpose**: Dead Letter Queue for notification messages
- **Explanation**: Failed notification messages are stored here

**`DELIVERY_DLQ = "delivery.dlq"`**
- **Purpose**: Dead Letter Queue for delivery messages
- **Explanation**: Failed delivery messages are stored here

### Message Converter Bean

```java
@Bean
public MessageConverter converter() {
    return new Jackson2JsonMessageConverter();
}
```

#### Detailed Explanation:

**`@Bean`**
- **Purpose**: Tells Spring to register the return value of this method as a bean in the Spring application context
- **Explanation**: This bean will be available for dependency injection throughout the application

**`MessageConverter converter()`**
- **Return Type**: `MessageConverter` - Interface for converting between Java objects and AMQP messages
- **Method Name**: `converter` - Descriptive name for the bean
- **Implementation**: Returns `new Jackson2JsonMessageConverter()`

**`Jackson2JsonMessageConverter`**
- **Purpose**: Converts Java objects to JSON format when sending messages and converts JSON back to Java objects when receiving messages
- **Why Jackson**: Jackson is a popular, high-performance JSON library for Java
- **Benefits**:
  - Automatic serialization/deserialization of Java objects
  - Support for complex object graphs
  - Customizable with annotations
  - Human-readable message format for debugging
- **How It Works**:
  1. When sending: Java object → JSON byte array → AMQP message
  2. When receiving: AMQP message → JSON byte array → Java object

### RabbitTemplate Bean

```java
@Bean
public AmqpTemplate template(ConnectionFactory connectionFactory) {
    final RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
    rabbitTemplate.setMessageConverter(converter());
    return rabbitTemplate;
}
```

#### Detailed Explanation:

**`AmqpTemplate template(ConnectionFactory connectionFactory)`**
- **Return Type**: `AmqpTemplate` - Interface that defines basic RabbitMQ operations (send and receive)
- **Parameter**: `ConnectionFactory connectionFactory` - Spring automatically injects the connection factory bean
- **Method Name**: `template` - Descriptive name for the RabbitMQ template bean

**`new RabbitTemplate(connectionFactory)`**
- **Purpose**: Creates a new RabbitTemplate instance with the provided connection factory
- **ConnectionFactory**: Establishes connections to the RabbitMQ broker
- **Explanation**: The template uses this connection factory to create connections for sending and receiving messages

**`rabbitTemplate.setMessageConverter(converter())`**
- **Purpose**: Configures the message converter to be used by this template
- **Method Call**: `converter()` - Calls the converter() bean method defined earlier
- **Explanation**: This ensures that all messages sent through this template are automatically converted to JSON, and received messages are converted back to Java objects

### Exchange Bean

```java
@Bean
public TopicExchange orderExchange() {
    return new TopicExchange(ORDER_EXCHANGE);
}
```

#### Detailed Explanation:

**`TopicExchange orderExchange()`**
- **Return Type**: `TopicExchange` - A type of exchange that routes messages based on wildcard matching of routing keys
- **Method Name**: `orderExchange` - Descriptive name for the exchange bean
- **Parameter**: `ORDER_EXCHANGE` - The constant "order.exchange" defined earlier

**`TopicExchange`**
- **Purpose**: Exchange type that allows flexible routing with wildcard patterns
- **Routing Patterns**:
  - `*` (star): Matches exactly one word
  - `#` (hash): Matches zero or more words
- **Example Routing**:
  - `order.created` matches `order.*`
  - `order.created` matches `order.#`
  - `order.created.customer` matches `order.#` but not `order.*`
- **Why Topic Exchange**: Provides flexibility for future routing patterns while maintaining simplicity for current needs

**`new TopicExchange(ORDER_EXCHANGE)`**
- **Purpose**: Creates a new topic exchange with the specified name
- **Durability**: By default, exchanges are durable (survive broker restart)
- **Auto-Delete**: By default, exchanges are not auto-deleted

### Queue Beans

#### Order Queue

```java
@Bean
public Queue orderQueue() {
    return QueueBuilder.durable(ORDER_QUEUE)
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", ORDER_DLQ)
            .build();
}
```

**Detailed Explanation:**

**`Queue orderQueue()`**
- **Return Type**: `Queue` - Represents a queue in RabbitMQ
- **Method Name**: `orderQueue` - Descriptive name for the order queue bean

**`QueueBuilder.durable(ORDER_QUEUE)`**
- **Purpose**: Creates a durable queue with the specified name
- **Durable**: The queue survives broker restarts
- **Queue Name**: `ORDER_QUEUE` constant ("order.queue")
- **QueueBuilder**: Builder pattern for creating queues with various configurations

**`.withArgument("x-dead-letter-exchange", "")`**
- **Purpose**: Configures the Dead Letter Exchange (DLX) for this queue
- **Key**: `"x-dead-letter-exchange"` - RabbitMQ's built-in argument for specifying DLX
- **Value**: `""` (empty string) - Uses the default exchange (unnamed exchange)
- **Explanation**: When messages fail processing and are rejected or expire, they are routed to the dead letter exchange

**`.withArgument("x-dead-letter-routing-key", ORDER_DLQ)`**
- **Purpose**: Configures the routing key for dead-lettered messages
- **Key**: `"x-dead-letter-routing-key"` - RabbitMQ's built-in argument for specifying DLQ routing key
- **Value**: `ORDER_DLQ` constant ("order.dlq")
- **Explanation**: Failed messages will be routed to the queue named "order.dlq" using the default exchange

**`.build()`**
- **Purpose**: Finalizes the queue configuration and creates the Queue object

#### Order Dead Letter Queue

```java
@Bean
public Queue orderDLQ() {
    return QueueBuilder.durable(ORDER_DLQ).build();
}
```

**Detailed Explanation:**

**`Queue orderDLQ()`**
- **Return Type**: `Queue` - Represents the dead letter queue
- **Method Name**: `orderDLQ` - Descriptive name for the order DLQ bean

**`QueueBuilder.durable(ORDER_DLQ)`**
- **Purpose**: Creates a durable queue for storing failed messages
- **Queue Name**: `ORDER_DLQ` constant ("order.dlq")
- **Explanation**: This queue has no dead letter configuration because it's the final destination for failed messages

#### Notification Queue

```java
@Bean
public Queue notificationQueue() {
    return QueueBuilder.durable(NOTIFICATION_QUEUE)
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", NOTIFICATION_DLQ)
            .build();
}
```

**Detailed Explanation:**

Similar to order queue, but configured for notification messages:
- **Queue Name**: `NOTIFICATION_QUEUE` ("notification.queue")
- **DLX**: Default exchange (empty string)
- **DLQ Routing Key**: `NOTIFICATION_DLQ` ("notification.dlq")

#### Notification Dead Letter Queue

```java
@Bean
public Queue notificationDLQ() {
    return QueueBuilder.durable(NOTIFICATION_DLQ).build();
}
```

**Detailed Explanation:**

Stores failed notification messages:
- **Queue Name**: `NOTIFICATION_DLQ` ("notification.dlq")
- **Purpose**: Final destination for failed notification messages

#### Delivery Queue

```java
@Bean
public Queue deliveryQueue() {
    return QueueBuilder.durable(DELIVERY_QUEUE)
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", DELIVERY_DLQ)
            .build();
}
```

**Detailed Explanation:**

Similar to order queue, but configured for delivery messages:
- **Queue Name**: `DELIVERY_QUEUE` ("delivery.queue")
- **DLX**: Default exchange (empty string)
- **DLQ Routing Key**: `DELIVERY_DLQ` ("delivery.dlq")

#### Delivery Dead Letter Queue

```java
@Bean
public Queue deliveryDLQ() {
    return QueueBuilder.durable(DELIVERY_DLQ).build();
}
```

**Detailed Explanation:**

Stores failed delivery messages:
- **Queue Name**: `DELIVERY_DLQ` ("delivery.dlq")
- **Purpose**: Final destination for failed delivery messages

### Binding Beans

#### Order Binding

```java
@Bean
public Binding orderBinding() {
    return BindingBuilder.bind(orderQueue()).to(orderExchange()).with(ORDER_ROUTING_KEY);
}
```

**Detailed Explanation:**

**`Binding orderBinding()`**
- **Return Type**: `Binding` - Represents a relationship between a queue and an exchange
- **Method Name**: `orderBinding` - Descriptive name for the order binding bean

**`BindingBuilder.bind(orderQueue())`**
- **Purpose**: Starts building a binding for the order queue
- **Method Call**: `orderQueue()` - References the order queue bean defined earlier
- **Explanation**: Specifies which queue to bind

**`.to(orderExchange())`**
- **Purpose**: Specifies the exchange to bind the queue to
- **Method Call**: `orderExchange()` - References the order exchange bean defined earlier
- **Explanation**: Specifies which exchange the queue will receive messages from

**`.with(ORDER_ROUTING_KEY)`**
- **Purpose**: Specifies the routing key for this binding
- **Value**: `ORDER_ROUTING_KEY` constant ("order.created")
- **Explanation**: Messages published to the exchange with routing key "order.created" will be routed to the order queue

**How It Works**:
1. Producer publishes message to "order.exchange" with routing key "order.created"
2. Exchange checks bindings
3. Finds binding: order.queue bound to order.exchange with routing key "order.created"
4. Routes message to order.queue

#### Notification Binding

```java
@Bean
public Binding notificationBinding() {
    return BindingBuilder.bind(notificationQueue()).to(orderExchange()).with(NOTIFICATION_ROUTING_KEY);
}
```

**Detailed Explanation:**

Binds notification queue to the order exchange:
- **Queue**: `notificationQueue()` - Notification queue
- **Exchange**: `orderExchange()` - Order exchange (same exchange used for all events)
- **Routing Key**: `NOTIFICATION_ROUTING_KEY` ("notification.send")

**Why Same Exchange?**
- Centralizes all order-related events in one exchange
- Simplifies monitoring and management
- Allows for future routing patterns (e.g., routing all events to a monitoring queue)

#### Delivery Binding

```java
@Bean
public Binding deliveryBinding() {
    return BindingBuilder.bind(deliveryQueue()).to(orderExchange()).with(DELIVERY_ROUTING_KEY);
}
```

**Detailed Explanation:**

Binds delivery queue to the order exchange:
- **Queue**: `deliveryQueue()` - Delivery queue
- **Exchange**: `orderExchange()` - Order exchange
- **Routing Key**: `DELIVERY_ROUTING_KEY` ("delivery.assign")

---

## Message Events

### Overview

Message events are data structures that carry information between microservices. They represent domain events that occur in the system, such as an order being placed, confirmed, or delivered.

### Event Design Principles

1. **Immutable**: Events cannot be changed once created
2. **Serializable**: Can be converted to JSON for transmission
3. **Self-contained**: Contains all necessary data for processing
4. **Timestamped**: Includes when the event occurred
5. **Identified**: Has unique message ID for tracking
6. **Correlated**: Includes correlation ID for tracing related events

### OrderEvent

**File**: `common-lib/src/main/java/com/fooddelivery/common/messaging/event/OrderEvent.java`

#### Package Declaration

```java
package com.fooddelivery.common.messaging.event;
```

- **Purpose**: Declares the package for event classes
- **Package Path**: `com.fooddelivery.common.messaging.event`

#### Imports

```java
import com.fooddelivery.common.enums.OrderStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;
```

- **`OrderStatus`**: Enum representing order status values
- **`@AllArgsConstructor`**: Lombok annotation to generate constructor with all parameters
- **`@Builder`**: Lombok annotation to generate builder pattern for object creation
- **`@Data`**: Lombok annotation to generate getters, setters, toString, equals, and hashCode
- **`@NoArgsConstructor`**: Lombok annotation to generate no-argument constructor
- **`BigDecimal`**: For precise monetary calculations
- **`LocalDateTime`**: For timestamp without timezone
- **`UUID`**: For generating unique identifiers

#### Class Declaration

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderEvent {
```

- **`@Data`**: Generates all boilerplate code (getters, setters, etc.)
- **`@Builder`**: Enables builder pattern for fluent object creation
- **`@NoArgsConstructor`**: Required for JSON deserialization
- **`@AllArgsConstructor`**: Convenient for creating objects with all fields
- **`public class OrderEvent`**: Event class for order-related events

#### Fields

```java
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
```

**Detailed Field Explanation:**

**`messageId`**
- **Type**: `String`
- **Purpose**: Unique identifier for this specific message
- **Format**: UUID string (e.g., "550e8400-e29b-41d4-a716-446655440000")
- **Usage**: Used for idempotency checking to prevent duplicate processing
- **Generation**: Generated using `UUID.randomUUID().toString()`

**`eventType`**
- **Type**: `String`
- **Purpose**: Indicates the type of event that occurred
- **Values**: "ORDER_PLACED", "ORDER_CONFIRMED", "ORDER_DELIVERED", "DELIVERY_ASSIGNED"
- **Usage**: Consumers use this to determine how to process the event

**`orderId`**
- **Type**: `Long`
- **Purpose**: ID of the order this event relates to
- **Usage**: Links the event to a specific order in the database

**`customerId`**
- **Type**: `Long`
- **Purpose**: ID of the customer who placed the order
- **Usage**: Used for sending notifications to the customer

**`restaurantId`**
- **Type**: `Long`
- **Purpose**: ID of the restaurant preparing the order
- **Usage**: Used for restaurant-specific processing

**`deliveryPartnerId`**
- **Type**: `Long`
- **Purpose**: ID of the delivery partner assigned to the order
- **Usage**: Used for delivery partner status updates
- **Nullable**: May be null if no delivery partner is assigned yet

**`totalAmount`**
- **Type**: `BigDecimal`
- **Purpose**: Total monetary value of the order
- **Usage**: Used for financial calculations and notifications
- **Why BigDecimal**: Precise decimal arithmetic for monetary values

**`orderStatus`**
- **Type**: `OrderStatus` (enum)
- **Purpose**: Current status of the order
- **Values**: PLACED, CONFIRMED, PREPARING, OUT_FOR_DELIVERY, DELIVERED, CANCELLED
- **Usage**: Indicates the state transition that triggered this event

**`timestamp`**
- **Type**: `LocalDateTime`
- **Purpose**: When this event was created
- **Usage**: For auditing, debugging, and time-based processing
- **Format**: ISO-8601 format (e.g., "2024-05-26T10:30:45")

**`correlationId`**
- **Type**: `String`
- **Purpose**: Links related events together in a distributed transaction
- **Format**: UUID string
- **Usage**: Traces a sequence of events (e.g., order placed → confirmed → delivered)

#### Factory Methods

**createOrderPlacedEvent**

```java
public static OrderEvent createOrderPlacedEvent(Long orderId, Long customerId, Long restaurantId, BigDecimal totalAmount) {
    return OrderEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("ORDER_PLACED")
            .orderId(orderId)
            .customerId(customerId)
            .restaurantId(restaurantId)
            .totalAmount(totalAmount)
            .orderStatus(OrderStatus.PLACED)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Factory method to create an ORDER_PLACED event
- **Parameters**:
  - `orderId`: The ID of the newly placed order
  - `customerId`: The ID of the customer who placed the order
  - `restaurantId`: The ID of the restaurant that will prepare the order
  - `totalAmount`: The total cost of the order
- **Builder Pattern**: Uses fluent API for readable object construction
- **Field Initialization**:
  - `messageId`: New UUID for this message
  - `eventType`: "ORDER_PLACED" - indicates order creation
  - `orderId`, `customerId`, `restaurantId`, `totalAmount`: From parameters
  - `orderStatus`: `OrderStatus.PLACED` - initial status
  - `timestamp`: Current time when event is created
  - `correlationId`: New UUID for tracking this order's lifecycle
- **Usage**: Called when an order is successfully created in the order service

**createOrderConfirmedEvent**

```java
public static OrderEvent createOrderConfirmedEvent(Long orderId, Long customerId, Long restaurantId, BigDecimal totalAmount) {
    return OrderEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("ORDER_CONFIRMED")
            .orderId(orderId)
            .customerId(customerId)
            .restaurantId(restaurantId)
            .totalAmount(totalAmount)
            .orderStatus(OrderStatus.CONFIRMED)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Factory method to create an ORDER_CONFIRMED event
- **Parameters**: Same as createOrderPlacedEvent
- **Field Initialization**:
  - `eventType`: "ORDER_CONFIRMED" - indicates restaurant accepted the order
  - `orderStatus`: `OrderStatus.CONFIRMED` - updated status
- **Usage**: Called when the restaurant confirms the order

**createOrderDeliveredEvent**

```java
public static OrderEvent createOrderDeliveredEvent(Long orderId, Long customerId, Long deliveryPartnerId) {
    return OrderEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("ORDER_DELIVERED")
            .orderId(orderId)
            .customerId(customerId)
            .deliveryPartnerId(deliveryPartnerId)
            .orderStatus(OrderStatus.DELIVERED)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Factory method to create an ORDER_DELIVERED event
- **Parameters**:
  - `orderId`: The ID of the delivered order
  - `customerId`: The ID of the customer
  - `deliveryPartnerId`: The ID of the delivery partner who delivered the order
- **Field Initialization**:
  - `eventType`: "ORDER_DELIVERED" - indicates successful delivery
  - `deliveryPartnerId`: Set from parameter (who delivered)
  - `orderStatus`: `OrderStatus.DELIVERED` - final status
- **Usage**: Called when the order is successfully delivered to the customer

**createDeliveryAssignmentEvent**

```java
public static OrderEvent createDeliveryAssignmentEvent(Long orderId, Long deliveryPartnerId) {
    return OrderEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("DELIVERY_ASSIGNED")
            .orderId(orderId)
            .deliveryPartnerId(deliveryPartnerId)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Factory method to create a DELIVERY_ASSIGNED event
- **Parameters**:
  - `orderId`: The ID of the order
  - `deliveryPartnerId`: The ID of the assigned delivery partner
- **Field Initialization**:
  - `eventType`: "DELIVERY_ASSIGNED" - indicates delivery partner assignment
  - `deliveryPartnerId`: Set from parameter
  - `orderStatus`: Not set (this is about delivery, not order status)
- **Usage**: Called when a delivery partner is assigned to an order

### NotificationEvent

**File**: `common-lib/src/main/java/com/fooddelivery/common/messaging/event/NotificationEvent.java`

#### Class Declaration

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NotificationEvent {
```

- **Purpose**: Event class for notification-related events
- **Annotations**: Same as OrderEvent for consistency

#### Fields

```java
private String messageId;
private String eventType;
private Long userId;
private String message;
private String type;
private String channel;
private LocalDateTime timestamp;
private String correlationId;
```

**Detailed Field Explanation:**

**`messageId`**
- **Type**: `String`
- **Purpose**: Unique identifier for this notification message
- **Usage**: Idempotency checking

**`eventType`**
- **Type**: `String`
- **Purpose**: Type of notification event
- **Value**: "NOTIFICATION_SEND"

**`userId`**
- **Type**: `Long`
- **Purpose**: ID of the user to receive the notification
- **Usage**: Identifies the recipient

**`message`**
- **Type**: `String`
- **Purpose**: The actual notification message content
- **Usage**: Text to be sent to the user

**`type`**
- **Type**: `String`
- **Purpose**: Category of notification
- **Values**: "ORDER_PLACED", "ORDER_CONFIRMED", "ORDER_DELIVERED", etc.
- **Usage**: Determines notification template/priority

**`channel`**
- **Type**: `String`
- **Purpose**: Delivery channel for the notification
- **Values**: "EMAIL", "SMS", "PUSH"
- **Usage**: Routes notification to appropriate delivery mechanism

**`timestamp`**
- **Type**: `LocalDateTime`
- **Purpose**: When the notification event was created

**`correlationId`**
- **Type**: `String`
- **Purpose**: Links to related events

#### Factory Method

```java
public static NotificationEvent createNotificationEvent(Long userId, String message, String type) {
    return NotificationEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("NOTIFICATION_SEND")
            .userId(userId)
            .message(message)
            .type(type)
            .channel("EMAIL")
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Factory method to create a notification event
- **Parameters**:
  - `userId`: Recipient of the notification
  - `message`: Notification content
  - `type`: Notification type/category
- **Field Initialization**:
  - `channel`: Hardcoded to "EMAIL" (can be extended)
  - Other fields: Generated or from parameters
- **Usage**: Called when a notification needs to be sent

### DeliveryEvent

**File**: `common-lib/src/main/java/com/fooddelivery/common/messaging/event/DeliveryEvent.java`

#### Class Declaration

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DeliveryEvent {
```

- **Purpose**: Event class for delivery-related events

#### Fields

```java
private String messageId;
private String eventType;
private Long orderId;
private Long deliveryPartnerId;
private DeliveryStatus deliveryStatus;
private LocalDateTime timestamp;
private String correlationId;
```

**Detailed Field Explanation:**

**`messageId`**
- **Type**: `String`
- **Purpose**: Unique identifier for this delivery message

**`eventType`**
- **Type**: `String`
- **Purpose**: Type of delivery event
- **Values**: "DELIVERY_ASSIGNMENT", "DELIVERY_STATUS_UPDATE"

**`orderId`**
- **Type**: `Long`
- **Purpose**: ID of the order related to this delivery event

**`deliveryPartnerId`**
- **Type**: `Long`
- **Purpose**: ID of the delivery partner

**`deliveryStatus`**
- **Type**: `DeliveryStatus` (enum)
- **Purpose**: Current status of the delivery
- **Values**: AVAILABLE, ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED

**`timestamp`**
- **Type**: `LocalDateTime`
- **Purpose**: When the delivery event was created

**`correlationId`**
- **Type**: `String`
- **Purpose**: Links to related events

#### Factory Methods

**createDeliveryAssignmentEvent**

```java
public static DeliveryEvent createDeliveryAssignmentEvent(Long orderId, Long deliveryPartnerId) {
    return DeliveryEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("DELIVERY_ASSIGNMENT")
            .orderId(orderId)
            .deliveryPartnerId(deliveryPartnerId)
            .deliveryStatus(DeliveryStatus.ASSIGNED)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Creates an event when a delivery partner is assigned
- **Parameters**:
  - `orderId`: The order being assigned
  - `deliveryPartnerId`: The partner being assigned
- **Field Initialization**:
  - `eventType`: "DELIVERY_ASSIGNMENT"
  - `deliveryStatus`: `DeliveryStatus.ASSIGNED`

**createDeliveryStatusUpdateEvent**

```java
public static DeliveryEvent createDeliveryStatusUpdateEvent(Long orderId, Long deliveryPartnerId, DeliveryStatus status) {
    return DeliveryEvent.builder()
            .messageId(UUID.randomUUID().toString())
            .eventType("DELIVERY_STATUS_UPDATE")
            .orderId(orderId)
            .deliveryPartnerId(deliveryPartnerId)
            .deliveryStatus(status)
            .timestamp(LocalDateTime.now())
            .correlationId(UUID.randomUUID().toString())
            .build();
}
```

**Detailed Explanation:**

- **Purpose**: Creates an event when delivery status changes
- **Parameters**:
  - `orderId`: The order
  - `deliveryPartnerId`: The delivery partner
  - `status`: The new delivery status
- **Field Initialization**:
  - `eventType`: "DELIVERY_STATUS_UPDATE"
  - `deliveryStatus`: From parameter

---

## Message Producer

### File: `MessageProducer.java`

Location: `common-lib/src/main/java/com/fooddelivery/common/messaging/producer/MessageProducer.java`

This service is responsible for publishing events to RabbitMQ.

### Package Declaration

```java
package com.fooddelivery.common.messaging.producer;
```

- **Purpose**: Package for producer classes
- **Package Path**: `com.fooddelivery.common.messaging.producer`

### Imports

```java
import com.fooddelivery.common.messaging.config.RabbitMQConfig;
import com.fooddelivery.common.messaging.event.DeliveryEvent;
import com.fooddelivery.common.messaging.event.NotificationEvent;
import com.fooddelivery.common.messaging.event.OrderEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.stereotype.Service;
```

- **`RabbitMQConfig`**: Configuration class with exchange and routing key constants
- **Event classes**: OrderEvent, NotificationEvent, DeliveryEvent
- **`@RequiredArgsConstructor`**: Lombok annotation to generate constructor with required fields (final fields)
- **`@Slf4j`**: Lombok annotation to generate SLF4J logger
- **`AmqpTemplate`**: Spring's template for RabbitMQ operations
- **`@Service`**: Spring annotation indicating this is a service component

### Class Declaration

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class MessageProducer {
```

- **`@Service`**: Marks this class as a Spring service (component scan will pick it up)
- **`@RequiredArgsConstructor`**: Generates constructor with final field (amqpTemplate)
- **`@Slf4j`**: Generates logger field named `log`
- **`public class MessageProducer`**: Service class for producing messages

### Field

```java
private final AmqpTemplate amqpTemplate;
```

**Detailed Explanation:**

- **`private`**: Access modifier - field is only accessible within this class
- **`final`**: Field cannot be reassigned after initialization (ensures immutability)
- **`AmqpTemplate`**: Type of the field - Spring's template for RabbitMQ operations
- **`amqpTemplate`**: Name of the field
- **Injection**: Spring automatically injects the RabbitTemplate bean defined in RabbitMQConfig
- **Usage**: Used to send messages to RabbitMQ exchanges

### sendOrderEvent Method

```java
public void sendOrderEvent(OrderEvent event) {
    log.info("Sending order event: {} for order: {}", event.getEventType(), event.getOrderId());
    try {
        amqpTemplate.convertAndSend(
                RabbitMQConfig.ORDER_EXCHANGE,
                RabbitMQConfig.ORDER_ROUTING_KEY,
                event
        );
        log.info("Order event sent successfully: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Failed to send order event: messageId={}, error={}", event.getMessageId(), e.getMessage(), e);
        throw new RuntimeException("Failed to send order event", e);
    }
}
```

**Detailed Explanation:**

**Method Signature**
- **`public`**: Accessible from anywhere
- **`void`**: No return value
- **`sendOrderEvent`**: Method name
- **`OrderEvent event`**: Parameter - the event to send

**Logging Before Send**
```java
log.info("Sending order event: {} for order: {}", event.getEventType(), event.getOrderId());
```
- **Purpose**: Logs the start of the send operation
- **Level**: INFO - important for tracking
- **Parameters**: Event type and order ID for context

**Try-Catch Block**
```java
try {
    // Send logic
} catch (Exception e) {
    // Error handling
}
```
- **Purpose**: Handles potential errors during message sending
- **Exception Type**: `Exception` - catches all exceptions

**Message Sending**
```java
amqpTemplate.convertAndSend(
        RabbitMQConfig.ORDER_EXCHANGE,
        RabbitMQConfig.ORDER_ROUTING_KEY,
        event
);
```

**`amqpTemplate.convertAndSend()`**
- **Purpose**: Converts the object to a message and sends it to RabbitMQ
- **Parameters**:
  1. `RabbitMQConfig.ORDER_EXCHANGE` - "order.exchange" - the exchange to publish to
  2. `RabbitMQConfig.ORDER_ROUTING_KEY` - "order.created" - the routing key
  3. `event` - the OrderEvent object to send

**How It Works:**
1. `convertAndSend` calls the message converter (Jackson2JsonMessageConverter)
2. Converter transforms OrderEvent object to JSON byte array
3. RabbitTemplate creates AMQP message with JSON payload
4. Message is published to "order.exchange" with routing key "order.created"
5. Exchange routes message to queues bound with that routing key

**Logging After Send**
```java
log.info("Order event sent successfully: messageId={}", event.getMessageId());
```
- **Purpose**: Confirms successful message transmission
- **Level**: INFO - important for confirmation

**Error Handling**
```java
catch (Exception e) {
    log.error("Failed to send order event: messageId={}, error={}", event.getMessageId(), e.getMessage(), e);
    throw new RuntimeException("Failed to send order event", e);
}
```

**`log.error()`**
- **Purpose**: Logs the error with context
- **Level**: ERROR - indicates a problem
- **Parameters**: Message ID, error message, and exception stack trace

**`throw new RuntimeException()`**
- **Purpose**: Propagates the error to the caller
- **Message**: "Failed to send order event" - descriptive error message
- **Cause**: Original exception `e` - preserves stack trace
- **Why Throw**: Allows caller to handle the failure (e.g., retry, rollback transaction)

### sendNotificationEvent Method

```java
public void sendNotificationEvent(NotificationEvent event) {
    log.info("Sending notification event: {} for user: {}", event.getEventType(), event.getUserId());
    try {
        amqpTemplate.convertAndSend(
                RabbitMQConfig.ORDER_EXCHANGE,
                RabbitMQConfig.NOTIFICATION_ROUTING_KEY,
                event
        );
        log.info("Notification event sent successfully: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Failed to send notification event: messageId={}, error={}", event.getMessageId(), e.getMessage(), e);
        throw new RuntimeException("Failed to send notification event", e);
    }
}
```

**Detailed Explanation:**

Similar to sendOrderEvent, but for notification events:

**Key Differences:**
- **Routing Key**: `RabbitMQConfig.NOTIFICATION_ROUTING_KEY` ("notification.send")
- **Log Context**: Uses user ID instead of order ID
- **Event Type**: NotificationEvent instead of OrderEvent

**Flow:**
1. Logs notification send attempt
2. Publishes to "order.exchange" with routing key "notification.send"
3. Exchange routes to notification.queue
4. Logs success or throws exception on failure

### sendDeliveryEvent Method

```java
public void sendDeliveryEvent(DeliveryEvent event) {
    log.info("Sending delivery event: {} for order: {}", event.getEventType(), event.getOrderId());
    try {
        amqpTemplate.convertAndSend(
                RabbitMQConfig.ORDER_EXCHANGE,
                RabbitMQConfig.DELIVERY_ROUTING_KEY,
                event
        );
        log.info("Delivery event sent successfully: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Failed to send delivery event: messageId={}, error={}", event.getMessageId(), e.getMessage(), e);
        throw new RuntimeException("Failed to send delivery event", e);
    }
}
```

**Detailed Explanation:**

Similar to sendOrderEvent, but for delivery events:

**Key Differences:**
- **Routing Key**: `RabbitMQConfig.DELIVERY_ROUTING_KEY` ("delivery.assign")
- **Event Type**: DeliveryEvent instead of OrderEvent

**Flow:**
1. Logs delivery event send attempt
2. Publishes to "order.exchange" with routing key "delivery.assign"
3. Exchange routes to delivery.queue
4. Logs success or throws exception on failure

---

## Message Consumers

### Overview

Message consumers listen to RabbitMQ queues and process messages as they arrive. They use Spring AMQP's `@RabbitListener` annotation to automatically handle message consumption.

### Notification Service Consumer

**File**: `notification-service/src/main/java/com/fooddelivery/notification/consumer/OrderEventConsumer.java`

#### Package Declaration

```java
package com.fooddelivery.notification.consumer;
```

- **Purpose**: Package for consumer classes in notification service
- **Package Path**: `com.fooddelivery.notification.consumer`

#### Imports

```java
import com.fooddelivery.common.messaging.event.OrderEvent;
import com.fooddelivery.common.messaging.idempotency.IdempotencyHandler;
import com.fooddelivery.notification.dto.NotificationRequestDto;
import com.fooddelivery.notification.service.NotificationService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
```

- **`OrderEvent`**: Event class from common library
- **`IdempotencyHandler`**: Handler for checking duplicate messages
- **`NotificationRequestDto`**: DTO for notification requests
- **`NotificationService`**: Service for sending notifications
- **`@RabbitListener`**: Spring AMQP annotation for message listener methods
- **`@Component`**: Spring annotation for component registration

#### Class Declaration

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class OrderEventConsumer {
```

- **`@Component`**: Registers this class as a Spring component
- **`@RequiredArgsConstructor`**: Generates constructor with final fields
- **`@Slf4j`**: Generates logger
- **`public class OrderEventConsumer`**: Consumer class for order events

#### Fields

```java
private final NotificationService notificationService;
private final IdempotencyHandler idempotencyHandler;
```

**Detailed Explanation:**

**`notificationService`**
- **Type**: `NotificationService`
- **Purpose**: Service for sending notifications to users
- **Injection**: Spring injects the notification service bean
- **Usage**: Called to actually send notifications when events are received

**`idempotencyHandler`**
- **Type**: `IdempotencyHandler`
- **Purpose**: Checks if a message has already been processed
- **Injection**: Spring injects the idempotency handler bean from common library
- **Usage**: Prevents duplicate processing of the same message

#### handleOrderEvent Method

```java
@RabbitListener(queues = "${rabbitmq.queue.notification:notification.queue}")
public void handleOrderEvent(OrderEvent event) {
    log.info("Received order event: {} for order: {}", event.getEventType(), event.getOrderId());

    // Idempotency check - skip if message already processed
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
        
        // Mark message as processed after successful handling
        idempotencyHandler.markMessageAsProcessed(event.getMessageId());
        log.info("Successfully processed order event: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Error processing order event: messageId={}, error={}", 
            event.getMessageId(), e.getMessage(), e);
        throw e; // Re-throw to trigger retry mechanism
    }
}
```

**Detailed Explanation:**

**`@RabbitListener` Annotation**
```java
@RabbitListener(queues = "${rabbitmq.queue.notification:notification.queue}")
```

- **Purpose**: Marks this method as a message listener
- **`queues`**: Specifies which queue(s) to listen to
- **Value**: `"${rabbitmq.queue.notification:notification.queue}"`
  - **`${rabbitmq.queue.notification}`**: Property placeholder - reads from configuration
  - **`:notification.queue`**: Default value if property not found
- **How It Works**:
  1. Spring AMQP creates a message listener container
  2. Container connects to RabbitMQ
  3. Listens for messages on the specified queue
  4. When message arrives, deserializes it to OrderEvent
  5. Calls this method with the deserialized event

**Method Signature**
```java
public void handleOrderEvent(OrderEvent event)
```
- **`public`**: Accessible from anywhere
- **`void`**: No return value
- **`handleOrderEvent`**: Method name
- **`OrderEvent event`**: Parameter - the received event

**Initial Logging**
```java
log.info("Received order event: {} for order: {}", event.getEventType(), event.getOrderId());
```
- **Purpose**: Logs message receipt
- **Context**: Event type and order ID

**Idempotency Check**
```java
if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
    log.info("Skipping duplicate message: messageId={}", event.getMessageId());
    return;
}
```

**Purpose**: Prevents duplicate processing of the same message

**How It Works:**
1. Checks if the message ID is in the processed messages cache
2. If already processed, logs and returns early
3. If not processed, continues with normal processing

**Why Needed:**
- RabbitMQ may redeliver messages (e.g., consumer crashes)
- Network issues can cause duplicate deliveries
- Ensures each message is processed exactly once

**Switch Statement**
```java
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
```

**Purpose**: Routes different event types to appropriate notification messages

**Case "ORDER_PLACED"**
- **Trigger**: When a new order is created
- **Action**: Sends notification to customer
- **Message**: "Order #123 placed successfully"
- **Type**: "ORDER_PLACED"

**Case "ORDER_CONFIRMED"**
- **Trigger**: When restaurant accepts the order
- **Action**: Sends notification to customer
- **Message**: "Order #123 confirmed by restaurant"
- **Type**: "ORDER_CONFIRMED"

**Case "ORDER_DELIVERED"**
- **Trigger**: When order is delivered to customer
- **Action**: Sends notification to customer
- **Message**: "Order #123 has been delivered"
- **Type**: "ORDER_DELIVERED"

**Default Case**
- **Trigger**: Unknown event type
- **Action**: Logs warning
- **Purpose**: Defensive programming for future event types

**Mark as Processed**
```java
idempotencyHandler.markMessageAsProcessed(event.getMessageId());
log.info("Successfully processed order event: messageId={}", event.getMessageId());
```

**Purpose**: Marks the message as successfully processed

**How It Works:**
1. Adds message ID to processed messages cache
2. Logs successful processing
3. Future messages with same ID will be skipped

**Error Handling**
```java
catch (Exception e) {
    log.error("Error processing order event: messageId={}, error={}", 
        event.getMessageId(), e.getMessage(), e);
    throw e; // Re-throw to trigger retry mechanism
}
```

**Purpose**: Handles errors during message processing

**Logging Error**
- **Level**: ERROR
- **Context**: Message ID and error message
- **Stack Trace**: Full exception details

**Re-throw Exception**
- **Purpose**: Triggers RabbitMQ's retry mechanism
- **How It Works**:
  1. Exception propagates to RabbitMQ listener container
  2. Container sees exception and doesn't acknowledge message
  3. RabbitMQ re-queues the message
  4. Message is redelivered after retry delay
  5. After max retries, message goes to DLQ

#### sendNotification Helper Method

```java
private void sendNotification(Long userId, String message, String type) {
    NotificationRequestDto request = new NotificationRequestDto();
    request.setUserId(userId);
    request.setMessage(message);
    request.setType(type);
    notificationService.sendNotification(request);
}
```

**Detailed Explanation:**

**Purpose**: Helper method to create and send notification request

**Parameters:**
- `userId`: ID of the user to notify
- `message`: Notification message content
- `type`: Notification type/category

**Steps:**
1. Creates new NotificationRequestDto
2. Sets user ID
3. Sets message content
4. Sets notification type
5. Calls notification service to send

### Delivery Partner Service Consumer

**File**: `delivery-partner-service/src/main/java/com/fooddelivery/delivery/consumer/OrderEventConsumer.java`

#### Package Declaration

```java
package com.fooddelivery.delivery.consumer;
```

#### Imports

```java
import com.fooddelivery.common.messaging.event.OrderEvent;
import com.fooddelivery.common.messaging.idempotency.IdempotencyHandler;
import com.fooddelivery.delivery.dto.DeliveryStatusUpdateRequestDto;
import com.fooddelivery.delivery.service.DeliveryPartnerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
```

#### Class Declaration

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class OrderEventConsumer {
```

#### Fields

```java
private final DeliveryPartnerService deliveryPartnerService;
private final IdempotencyHandler idempotencyHandler;
```

**Detailed Explanation:**

**`deliveryPartnerService`**
- **Type**: `DeliveryPartnerService`
- **Purpose**: Service for managing delivery partners
- **Usage**: Updates delivery partner status based on events

**`idempotencyHandler`**
- **Type**: `IdempotencyHandler`
- **Purpose**: Checks for duplicate messages
- **Usage**: Same as notification consumer

#### handleOrderEvent Method

```java
@RabbitListener(queues = "${rabbitmq.queue.delivery:delivery.queue}")
public void handleOrderEvent(OrderEvent event) {
    log.info("Received order event: {} for order: {}", event.getEventType(), event.getOrderId());

    // Idempotency check - skip if message already processed
    if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
        log.info("Skipping duplicate message: messageId={}", event.getMessageId());
        return;
    }

    try {
        switch (event.getEventType()) {
            case "DELIVERY_ASSIGNED":
                log.info("Delivery assignment event received for order: {}, partner: {}", 
                    event.getOrderId(), event.getDeliveryPartnerId());
                // Update delivery partner status to ASSIGNED if needed
                updateDeliveryStatus(event.getDeliveryPartnerId(), com.fooddelivery.common.enums.DeliveryStatus.ASSIGNED);
                break;
            case "ORDER_DELIVERED":
                log.info("Order delivered event received for order: {}, partner: {}", 
                    event.getOrderId(), event.getDeliveryPartnerId());
                // Update delivery partner status to AVAILABLE after delivery
                updateDeliveryStatus(event.getDeliveryPartnerId(), com.fooddelivery.common.enums.DeliveryStatus.AVAILABLE);
                break;
            default:
                log.warn("Unknown event type: {}", event.getEventType());
        }
        
        // Mark message as processed after successful handling
        idempotencyHandler.markMessageAsProcessed(event.getMessageId());
        log.info("Successfully processed order event: messageId={}", event.getMessageId());
    } catch (Exception e) {
        log.error("Error processing order event: messageId={}, error={}", 
            event.getMessageId(), e.getMessage(), e);
        throw e; // Re-throw to trigger retry mechanism
    }
}
```

**Detailed Explanation:**

**`@RabbitListener` Annotation**
```java
@RabbitListener(queues = "${rabbitmq.queue.delivery:delivery.queue}")
```
- **Queue**: `delivery.queue` (or from property)
- **Purpose**: Listens for delivery-related events

**Switch Statement**

**Case "DELIVERY_ASSIGNED"**
- **Trigger**: When a delivery partner is assigned to an order
- **Action**: Updates delivery partner status to ASSIGNED
- **Log**: Logs assignment details

**Case "ORDER_DELIVERED"**
- **Trigger**: When order is delivered
- **Action**: Updates delivery partner status to AVAILABLE
- **Purpose**: Makes partner available for new deliveries
- **Log**: Logs delivery completion

#### updateDeliveryStatus Helper Method

```java
private void updateDeliveryStatus(Long partnerId, com.fooddelivery.common.enums.DeliveryStatus status) {
    try {
        DeliveryStatusUpdateRequestDto request = new DeliveryStatusUpdateRequestDto();
        request.setDeliveryStatus(status);
        deliveryPartnerService.updateStatus(partnerId, request);
    } catch (Exception e) {
        log.error("Failed to update delivery partner status: partnerId={}, status={}", 
            partnerId, status, e);
    }
}
```

**Detailed Explanation:**

**Purpose**: Updates delivery partner status

**Parameters:**
- `partnerId`: ID of the delivery partner
- `status`: New status to set

**Steps:**
1. Creates DeliveryStatusUpdateRequestDto
2. Sets the delivery status
3. Calls delivery partner service to update
4. Catches and logs errors (doesn't throw to avoid failing message processing)

**Why Catch Exception:**
- Status update failure shouldn't fail the entire message processing
- Logs error for monitoring
- Message still marked as processed

---

## Idempotency Handling

### File: `IdempotencyHandler.java`

Location: `common-lib/src/main/java/com/fooddelivery/common/messaging/idempotency/IdempotencyHandler.java`

### Overview

Idempotency ensures that processing the same message multiple times produces the same result as processing it once. This is critical in distributed systems where messages may be delivered multiple times due to network issues, consumer crashes, or broker redelivery.

### Why Idempotency is Needed

1. **Network Issues**: Temporary network failures can cause message redelivery
2. **Consumer Crashes**: If consumer crashes after processing but before acknowledging, message is redelivered
3. **Broker Redelivery**: RabbitMQ may redeliver messages under certain conditions
4. **Manual Reprocessing**: Messages from DLQ may be manually reprocessed
5. **Duplicate Publishing**: Producer might accidentally publish the same event twice

### Package Declaration

```java
package com.fooddelivery.common.messaging.idempotency;
```

### Imports

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
```

- **`@Slf4j`**: Lombok annotation for logger
- **`@Component`**: Spring component annotation
- **`ConcurrentHashMap`**: Thread-safe hash map for concurrent access
- **`ConcurrentMap`**: Interface for concurrent map operations

### Class Declaration

```java
@Component
@Slf4j
public class IdempotencyHandler {
```

- **`@Component`**: Spring component - automatically registered
- **`@Slf4j`**: Generates logger
- **`public class IdempotencyHandler`**: Handler for idempotency checks

### Fields

```java
private final ConcurrentMap<String, ProcessedMessage> processedMessages = new ConcurrentHashMap<>();
private static final long MESSAGE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
```

**Detailed Explanation:**

**`processedMessages`**
- **Type**: `ConcurrentMap<String, ProcessedMessage>`
- **Purpose**: Thread-safe cache of processed message IDs
- **Key**: Message ID (String)
- **Value**: ProcessedMessage object with timestamp
- **Why ConcurrentHashMap**: Thread-safe for concurrent access from multiple threads
- **Scope**: Instance field - each service instance has its own cache

**`MESSAGE_TTL_MS`**
- **Type**: `long`
- **Value**: `24 * 60 * 60 * 1000` = 86,400,000 milliseconds = 24 hours
- **Purpose**: Time-to-live for processed message entries
- **Why 24 Hours**: Reasonable window for message redelivery scenarios
- **Calculation**: 24 hours × 60 minutes × 60 seconds × 1000 milliseconds

### isMessageProcessed Method

```java
public boolean isMessageProcessed(String messageId) {
    ProcessedMessage processed = processedMessages.get(messageId);
    
    if (processed == null) {
        return false;
    }

    // Check if message has expired
    if (System.currentTimeMillis() - processed.getTimestamp() > MESSAGE_TTL_MS) {
        processedMessages.remove(messageId);
        return false;
    }

    log.info("Duplicate message detected: messageId={}", messageId);
    return true;
}
```

**Detailed Explanation:**

**Method Signature**
- **`public`**: Accessible from anywhere
- **`boolean`**: Returns true if message was already processed
- **`isMessageProcessed`**: Method name
- **`String messageId`**: Message ID to check

**Step 1: Lookup Message**
```java
ProcessedMessage processed = processedMessages.get(messageId);
```
- **Purpose**: Looks up message ID in cache
- **`get()`**: Thread-safe retrieval from ConcurrentHashMap
- **Return**: ProcessedMessage object or null if not found

**Step 2: Check if Not Found**
```java
if (processed == null) {
    return false;
}
```
- **Purpose**: Message not in cache - not processed yet
- **Return**: `false` - message should be processed
- **Explanation**: First time seeing this message ID

**Step 3: Check Expiration**
```java
if (System.currentTimeMillis() - processed.getTimestamp() > MESSAGE_TTL_MS) {
    processedMessages.remove(messageId);
    return false;
}
```

**`System.currentTimeMillis()`**
- **Purpose**: Gets current time in milliseconds since epoch
- **Return**: Current timestamp

**`processed.getTimestamp()`**
- **Purpose**: Gets when the message was first processed
- **Return**: Timestamp in milliseconds

**Time Difference Calculation**
```java
System.currentTimeMillis() - processed.getTimestamp()
```
- **Purpose**: Calculates time elapsed since first processing
- **Result**: Elapsed time in milliseconds

**Expiration Check**
```java
> MESSAGE_TTL_MS
```
- **Purpose**: Checks if elapsed time exceeds TTL
- **Condition**: If elapsed > 24 hours
- **Action**: Remove expired entry and return false

**Why Remove Expired:**
- Prevents memory leak
- Allows reprocessing of very old messages
- Keeps cache size manageable

**Step 4: Log Duplicate**
```java
log.info("Duplicate message detected: messageId={}", messageId);
```
- **Purpose**: Logs duplicate detection for monitoring
- **Level**: INFO - important for tracking
- **Context**: Message ID

**Step 5: Return True**
```java
return true;
```
- **Purpose**: Indicates message was already processed
- **Effect**: Consumer will skip processing this message

### markMessageAsProcessed Method

```java
public void markMessageAsProcessed(String messageId) {
    ProcessedMessage processed = new ProcessedMessage(messageId, System.currentTimeMillis());
    processedMessages.put(messageId, processed);
    log.debug("Message marked as processed: messageId={}", messageId);
}
```

**Detailed Explanation:**

**Method Signature**
- **`public`**: Accessible from anywhere
- **`void`**: No return value
- **`markMessageAsProcessed`**: Method name
- **`String messageId`**: Message ID to mark

**Step 1: Create ProcessedMessage**
```java
ProcessedMessage processed = new ProcessedMessage(messageId, System.currentTimeMillis());
```
- **Purpose**: Creates object to store message info
- **Parameters**:
  - `messageId`: The message ID
  - `System.currentTimeMillis()`: Current timestamp
- **Explanation**: Records when the message was processed

**Step 2: Store in Cache**
```java
processedMessages.put(messageId, processed);
```
- **Purpose**: Adds message to processed cache
- **`put()`**: Thread-safe insertion into ConcurrentHashMap
- **Effect**: Future checks will find this message as processed

**Step 3: Log**
```java
log.debug("Message marked as processed: messageId={}", messageId);
```
- **Purpose**: Logs marking for debugging
- **Level**: DEBUG - detailed information
- **Context**: Message ID

### cleanupExpiredMessages Method

```java
public void cleanupExpiredMessages() {
    long now = System.currentTimeMillis();
    processedMessages.entrySet().removeIf(entry -> {
        boolean expired = now - entry.getValue().getTimestamp() > MESSAGE_TTL_MS;
        if (expired) {
            log.debug("Removed expired message: messageId={}", entry.getKey());
        }
        return expired;
    });
}
```

**Detailed Explanation:**

**Purpose**: Manually cleanup expired messages from cache

**When to Call:**
- Scheduled task (e.g., hourly)
- On application startup
- When cache size exceeds threshold

**Step 1: Get Current Time**
```java
long now = System.currentTimeMillis();
```
- **Purpose**: Gets current timestamp for comparison

**Step 2: Remove Expired Entries**
```java
processedMessages.entrySet().removeIf(entry -> {
    boolean expired = now - entry.getValue().getTimestamp() > MESSAGE_TTL_MS;
    if (expired) {
        log.debug("Removed expired message: messageId={}", entry.getKey());
    }
    return expired;
});
```

**`entrySet()`**
- **Purpose**: Gets set of map entries (key-value pairs)

**`removeIf()`**
- **Purpose**: Removes entries that match a predicate
- **Thread-Safe**: Atomic operation on ConcurrentHashMap

**Predicate Logic**
```java
entry -> {
    boolean expired = now - entry.getValue().getTimestamp() > MESSAGE_TTL_MS;
    if (expired) {
        log.debug("Removed expired message: messageId={}", entry.getKey());
    }
    return expired;
}
```

**Calculate Expiration**
```java
boolean expired = now - entry.getValue().getTimestamp() > MESSAGE_TTL_MS;
```
- **Purpose**: Checks if entry is expired
- **Logic**: Current time - entry timestamp > 24 hours

**Log if Expired**
```java
if (expired) {
    log.debug("Removed expired message: messageId={}", entry.getKey());
}
```
- **Purpose**: Logs removal for debugging
- **Context**: Message ID being removed

**Return Result**
```java
return expired;
```
- **Purpose**: Returns true to remove entry if expired

### ProcessedMessage Inner Class

```java
private static class ProcessedMessage {
    private final String messageId;
    private final long timestamp;

    public ProcessedMessage(String messageId, long timestamp) {
        this.messageId = messageId;
        this.timestamp = timestamp;
    }

    public String getMessageId() {
        return messageId;
    }

    public long getTimestamp() {
        return timestamp;
    }
}
```

**Detailed Explanation:**

**Purpose**: Data class to store processed message information

**`private static class`**
- **`private`**: Only accessible within IdempotencyHandler
- **`static`**: Doesn't require outer class instance
- **`class`**: Inner class definition

**Fields**
```java
private final String messageId;
private final long timestamp;
```

**`messageId`**
- **Type**: `String`
- **Purpose**: The message ID
- **`final`**: Cannot be changed after construction

**`timestamp`**
- **Type**: `long`
- **Purpose**: When the message was processed
- **`final`**: Cannot be changed after construction

**Constructor**
```java
public ProcessedMessage(String messageId, long timestamp) {
    this.messageId = messageId;
    this.timestamp = timestamp;
}
```
- **Purpose**: Initializes the object
- **Parameters**: Message ID and timestamp

**Getters**
```java
public String getMessageId() {
    return messageId;
}

public long getTimestamp() {
    return timestamp;
}
```
- **Purpose**: Accessor methods for fields
- **Return**: Field values

### Limitations and Considerations

**Current Implementation Limitations:**

1. **In-Memory Only**: Cache is lost on application restart
2. **Per-Instance**: Each service instance has its own cache
3. **No Persistence**: Not durable across restarts
4. **Memory Bound**: Cache grows with processed messages

**When to Use This Implementation:**
- Single-instance deployments
- Short TTL requirements (24 hours)
- Acceptable to lose cache on restart
- Low to medium message volume

**When to Consider Alternatives:**
- Multi-instance deployments (use Redis)
- Long TTL requirements (use database)
- High message volume (use distributed cache)
- Need persistence (use database)

**Alternative Implementations:**
1. **Redis**: Distributed cache with TTL support
2. **Database**: Persistent storage with cleanup jobs
3. **Hazelcast**: Distributed in-memory data grid
4. **Cassandra**: Distributed NoSQL database

---

## Retry Mechanism

### File: `RabbitMQRetryConfig.java`

Location: `common-lib/src/main/java/com/fooddelivery/common/messaging/config/RabbitMQRetryConfig.java`

### Overview

The retry mechanism automatically retries failed message processing with exponential backoff. This handles transient failures (e.g., temporary database issues, network glitches) without manual intervention.

### Why Retry Mechanism is Needed

1. **Transient Failures**: Temporary issues that resolve quickly
2. **Database Locks**: Temporary contention that resolves
3. **Network Glitches**: Momentary network issues
4. **Service Unavailability**: Temporary service downtime
5. **Rate Limiting**: Temporary API rate limits

### Package Declaration

```java
package com.fooddelivery.common.messaging.config;
```

### Imports

```java
import org.springframework.amqp.rabbit.config.RetryInterceptorBuilder;
import org.springframework.amqp.rabbit.retry.MessageRecoverer;
import org.springframework.amqp.rabbit.retry.RepublishMessageRecoverer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.retry.interceptor.RetryOperationsInterceptor;
```

- **`RetryInterceptorBuilder`**: Builder for retry interceptors
- **`MessageRecoverer`**: Interface for recovering failed messages
- **`RepublishMessageRecoverer`**: Implementation that republishes to DLQ
- **`@Autowired`**: Spring annotation for dependency injection
- **`RetryOperationsInterceptor`**: Interceptor that adds retry logic
- **`ConnectionFactory`**: RabbitMQ connection factory
- **`RabbitTemplate`**: Template for RabbitMQ operations

### Class Declaration

```java
@Configuration
public class RabbitMQRetryConfig {
```

- **`@Configuration`**: Configuration class
- **`public class RabbitMQRetryConfig`**: Retry configuration

### Field

```java
@Autowired
private ConnectionFactory connectionFactory;
```

**Detailed Explanation:**

**`@Autowired`**
- **Purpose**: Tells Spring to inject this dependency
- **Injection**: Spring injects the ConnectionFactory bean

**`connectionFactory`**
- **Type**: `ConnectionFactory`
- **Purpose**: Factory for creating RabbitMQ connections
- **Usage**: Used by RepublishMessageRecoverer to republish messages

### rabbitTemplate Bean

```java
@Bean
public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
    RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
    
    // Enable publisher confirms
    rabbitTemplate.setConfirmCallback((correlationData, ack, cause) -> {
        if (ack) {
            System.out.println("Message received by broker");
        } else {
            System.out.println("Message not received by broker: " + cause);
        }
    });

    // Enable returns for unroutable messages
    rabbitTemplate.setReturnsCallback(returned -> {
        System.out.println("Message returned: " + returned.getMessage());
    });

    return rabbitTemplate;
}
```

**Detailed Explanation:**

**Method Signature**
- **`@Bean`**: Registers as Spring bean
- **`RabbitTemplate`**: Return type
- **`rabbitTemplate`**: Bean name
- **`ConnectionFactory connectionFactory`**: Injected parameter

**Create RabbitTemplate**
```java
RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
```
- **Purpose**: Creates new RabbitTemplate instance
- **Parameter**: Connection factory for connections

**Publisher Confirms**
```java
rabbitTemplate.setConfirmCallback((correlationData, ack, cause) -> {
    if (ack) {
        System.out.println("Message received by broker");
    } else {
        System.out.println("Message not received by broker: " + cause);
    }
});
```

**Purpose**: Confirms that broker received the message

**`setConfirmCallback()`**
- **Purpose**: Sets callback for publisher confirms
- **Parameter**: Lambda expression for callback

**Callback Parameters:**
- **`correlationData`**: Correlation data sent with message
- **`ack`**: Boolean - true if broker received, false if not
- **`cause`**: Reason for failure (if ack is false)

**Logic:**
- If `ack` is true: Print success message
- If `ack` is false: Print failure with cause

**Why Publisher Confirms:**
- Ensures message delivery to broker
- Detects broker issues
- Enables reliable messaging

**Returns Callback**
```java
rabbitTemplate.setReturnsCallback(returned -> {
    System.out.println("Message returned: " + returned.getMessage());
});
```

**Purpose**: Handles messages that couldn't be routed

**`setReturnsCallback()`**
- **Purpose**: Sets callback for returned messages
- **Parameter**: Lambda expression for callback

**When Messages Are Returned:**
- No queue bound to routing key
- Exchange doesn't exist
- Routing key doesn't match any bindings

**Why Returns Callback:**
- Detects routing issues
- Logs unroutable messages
- Helps debug configuration problems

### retryInterceptor Bean

```java
@Bean
public RetryOperationsInterceptor retryInterceptor() {
    return RetryInterceptorBuilder.stateless()
            .maxAttempts(3)
            .backOffOptions(1000, 2.0, 10000)
            .recoverer(messageRecoverer())
            .build();
}
```

**Detailed Explanation:**

**Method Signature**
- **`@Bean`**: Registers as Spring bean
- **`RetryOperationsInterceptor`**: Return type
- **`retryInterceptor`**: Bean name

**Builder Pattern**
```java
RetryInterceptorBuilder.stateless()
```
- **Purpose**: Creates stateless retry interceptor builder
- **Stateless**: Retry state not stored between attempts
- **Why Stateless**: Simpler, suitable for most cases

**Max Attempts**
```java
.maxAttempts(3)
```
- **Purpose**: Sets maximum number of retry attempts
- **Value**: 3 (initial attempt + 2 retries)
- **Why 3**: Balances retry attempts with processing time

**Backoff Options**
```java
.backOffOptions(1000, 2.0, 10000)
```

**Parameters:**
1. **`1000`**: Initial delay in milliseconds (1 second)
2. **`2.0`**: Multiplier for exponential backoff
3. **`10000`**: Maximum delay in milliseconds (10 seconds)

**Retry Schedule:**
- Attempt 1: Immediate
- Attempt 2: Wait 1 second (1000ms)
- Attempt 3: Wait 2 seconds (1000 × 2.0)
- Attempt 4: Wait 4 seconds (2000 × 2.0)
- Attempt 5: Wait 8 seconds (4000 × 2.0)
- Capped at 10 seconds

**Why Exponential Backoff:**
- Gives system time to recover
- Reduces load on failing service
- Prevents thundering herd problem

**Message Recoverer**
```java
.recoverer(messageRecoverer())
```
- **Purpose**: Sets the recoverer for exhausted retries
- **Method Call**: `messageRecoverer()` - calls the bean method
- **When Called**: After max attempts exhausted

**Build**
```java
.build();
```
- **Purpose**: Finalizes and creates the interceptor

### messageRecoverer Bean

```java
@Bean
public MessageRecoverer messageRecoverer() {
    return new RepublishMessageRecoverer(connectionFactory, "", RabbitMQConfig.ORDER_DLQ);
}
```

**Detailed Explanation:**

**Method Signature**
- **`@Bean`**: Registers as Spring bean
- **`MessageRecoverer`**: Return type
- **`messageRecoverer`**: Bean name

**Create RepublishMessageRecoverer**
```java
return new RepublishMessageRecoverer(connectionFactory, "", RabbitMQConfig.ORDER_DLQ);
```

**Constructor Parameters:**
1. **`connectionFactory`**: Connection factory for republishing
2. **`""`**: Empty string for default exchange
3. **`RabbitMQConfig.ORDER_DLQ`**: "order.dlq" - destination queue

**How It Works:**
1. After max retries exhausted
2. Creates new message with error information
3. Publishes to DLQ using default exchange
4. Original message removed from queue

**Why Republish to DLQ:**
- Preserves failed messages for inspection
- Enables manual reprocessing
- Provides audit trail of failures
- Doesn't block queue processing

### Configuration File Retry Settings

**File**: `config-repo/rabbitmq.yml`

```yaml
spring:
  rabbitmq:
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
```

**Detailed Explanation:**

**`acknowledge-mode: auto`**
- **Purpose**: Automatic acknowledgment mode
- **Behavior**: RabbitMQ auto-acks on successful processing
- **On Exception**: Message is re-queued for retry

**`retry.enabled: true`**
- **Purpose**: Enables retry mechanism
- **Value**: `true` - retries enabled

**`retry.max-attempts: 3`**
- **Purpose**: Maximum retry attempts
- **Value**: 3 (initial + 2 retries)
- **Matches**: Java config maxAttempts(3)

**`retry.initial-interval: 1000`**
- **Purpose**: Initial retry delay in milliseconds
- **Value**: 1000ms = 1 second
- **Matches**: Java config backOffOptions(1000, ...)

**`retry.multiplier: 2.0`**
- **Purpose**: Exponential backoff multiplier
- **Value**: 2.0 - doubles delay each retry
- **Matches**: Java config backOffOptions(..., 2.0, ...)

**`retry.max-interval: 10000`**
- **Purpose**: Maximum retry delay in milliseconds
- **Value**: 10000ms = 10 seconds
- **Matches**: Java config backOffOptions(..., 10000)

**`default-requeue-rejected: false`**
- **Purpose**: Don't re-queue rejected messages
- **Value**: `false` - send to DLQ instead
- **Why False**: Prevents infinite retry loops

### Retry Flow Diagram

```
Message Received
    ↓
Process Message
    ↓
Success?
    ↓ Yes
Acknowledge Message
    ↓
Done

    ↓ No
Retry Attempt 1
    ↓ Wait 1s
Process Message
    ↓
Success?
    ↓ Yes
Acknowledge Message
    ↓
Done

    ↓ No
Retry Attempt 2
    ↓ Wait 2s
Process Message
    ↓
Success?
    ↓ Yes
Acknowledge Message
    ↓
Done

    ↓ No
Retry Attempt 3
    ↓ Wait 4s
Process Message
    ↓
Success?
    ↓ Yes
Acknowledge Message
    ↓
Done

    ↓ No
Exhausted Retries
    ↓
Send to DLQ
    ↓
Done
```

---

## Dead Letter Queue

### Overview

Dead Letter Queue (DLQ) is a special queue that stores messages that failed processing after all retry attempts. This allows for manual inspection, debugging, and reprocessing of failed messages.

### Why DLQ is Needed

1. **Failed Message Preservation**: Messages aren't lost after retries
2. **Debugging**: Inspect failed messages to understand issues
3. **Manual Reprocessing**: Fix issues and reprocess messages
4. **Audit Trail**: Track all failed messages
5. **Monitoring**: Alert on message failures
6. **Data Recovery**: Recover critical data from failed messages

### DLQ Configuration

**In RabbitMQConfig.java:**

```java
@Bean
public Queue orderQueue() {
    return QueueBuilder.durable(ORDER_QUEUE)
            .withArgument("x-dead-letter-exchange", "")
            .withArgument("x-dead-letter-routing-key", ORDER_DLQ)
            .build();
}

@Bean
public Queue orderDLQ() {
    return QueueBuilder.durable(ORDER_DLQ).build();
}
```

**Detailed Explanation:**

**DLQ Arguments on Main Queue**

**`x-dead-letter-exchange`**
- **Purpose**: Specifies the exchange to route dead-lettered messages
- **Value**: `""` (empty string) - default exchange
- **Default Exchange**: Unnamed exchange that routes messages directly to queues by name

**`x-dead-letter-routing-key`**
- **Purpose**: Routing key for dead-lettered messages
- **Value**: `ORDER_DLQ` ("order.dlq")
- **Effect**: Messages are routed to the "order.dlq" queue

**How DLQ Works:**

1. **Message Processing Fails**: Consumer throws exception
2. **Retry Attempts**: Message is retried with backoff
3. **Max Attempts Reached**: After 3 attempts, retries exhausted
4. **Dead-Lettering**: RabbitMQ moves message to DLQ
5. **DLQ Storage**: Message stored in DLQ for inspection

### DLQ Message Structure

When a message is moved to DLQ, RabbitMQ adds headers:

**Original Headers:**
- `messageId`: Original message ID
- `eventType`: Event type
- All original event fields

**Added DLQ Headers:**
- `x-death`: Count of dead-lettering events
- `x-death-count`: Total number of times dead-lettered
- `x-first-death-queue`: First queue that rejected the message
- `x-first-death-reason`: Reason for first rejection
- `x-first-death-exchange`: Exchange that first dead-lettered the message
- `x-first-death-routing-key`: Routing key when first dead-lettered

### DLQ Management

**Monitoring DLQ:**

```java
// Check DLQ size
@Scheduled(fixedRate = 60000)
public void monitorDLQ() {
    int dlqSize = rabbitTemplate.execute(channel -> {
        return channel.queueDeclarePassive(ORDER_DLQ).getMessageCount();
    });
    if (dlqSize > 0) {
        log.warn("DLQ has {} messages", dlqSize);
        alertService.sendAlert("DLQ has messages");
    }
}
```

**Reprocessing from DLQ:**

```java
// Move message from DLQ back to main queue
public void reprocessMessage(String messageId) {
    Message message = rabbitTemplate.receive(ORDER_DLQ);
    if (message != null) {
        rabbitTemplate.send(ORDER_EXCHANGE, ORDER_ROUTING_KEY, message);
        log.info("Reprocessed message: {}", messageId);
    }
}
```

**DLQ Cleanup:**

```java
// Remove old messages from DLQ
@Scheduled(cron = "0 0 2 * * ?") // 2 AM daily
public void cleanupDLQ() {
    // Delete messages older than 7 days
    rabbitTemplate.execute(channel -> {
        channel.queuePurge(ORDER_DLQ);
        return null;
    });
}
```

### DLQ Best Practices

1. **Monitor DLQ Size**: Alert when DLQ grows
2. **Regular Inspection**: Check DLQ for patterns
3. **Root Cause Analysis**: Understand why messages fail
4. **Fix Underlying Issues**: Address root causes, not just symptoms
5. **Reprocess Carefully**: Test fixes before reprocessing
6. **Set Retention Policy**: Clean up old DLQ messages
7. **Document Failures**: Track common failure scenarios

---

## Configuration Files

### rabbitmq.yml

**Location**: `config-repo/rabbitmq.yml`

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

**Detailed Explanation:**

**Connection Settings**

**`host: localhost`**
- **Purpose**: RabbitMQ server hostname
- **Value**: localhost - local development
- **Production**: Use actual server hostname or IP

**`port: 5672`**
- **Purpose**: RabbitMQ AMQP port
- **Value**: 5672 - default AMQP port
- **SSL**: Use 5671 for SSL/TLS

**`username: admin`**
- **Purpose**: RabbitMQ username
- **Value**: admin - default admin user
- **Security**: Use strong credentials in production

**`password: admin`**
- **Purpose**: RabbitMQ password
- **Value**: admin - default admin password
- **Security**: Use strong credentials in production

**Listener Settings**

**`acknowledge-mode: auto`**
- **Purpose**: How messages are acknowledged
- **Values**:
  - `auto`: Automatic ack on success, nack on failure
  - `manual`: Manual ack/nack in code
  - `none`: No acknowledgment (not recommended)
- **Why Auto**: Simpler, Spring handles ack/nack

**Retry Settings**

**`retry.enabled: true`**
- **Purpose**: Enable retry mechanism
- **Value**: true - retries enabled

**`retry.max-attempts: 3`**
- **Purpose**: Maximum retry attempts
- **Value**: 3 - initial + 2 retries

**`retry.initial-interval: 1000`**
- **Purpose**: Initial delay between retries
- **Value**: 1000ms = 1 second

**`retry.multiplier: 2.0`**
- **Purpose**: Exponential backoff multiplier
- **Value**: 2.0 - delay doubles each retry

**`retry.max-interval: 10000`**
- **Purpose**: Maximum delay between retries
- **Value**: 10000ms = 10 seconds

**`default-requeue-rejected: false`**
- **Purpose**: Whether to re-queue rejected messages
- **Value**: false - send to DLQ instead
- **Why False**: Prevents infinite retry loops

**Publisher Settings**

**`publisher-confirm-type: correlated`**
- **Purpose**: Enable publisher confirms
- **Values**:
  - `none`: No confirms (default)
  - `simple`: Simple confirms
  - `correlated`: Correlated confirms with data
- **Why Correlated**: Enables tracking with correlation data

**`publisher-returns: true`**
- **Purpose**: Enable returns for unroutable messages
- **Value**: true - returns callback invoked
- **Why True**: Detects routing issues

### rabbitmq-docker.yml

**Location**: `config-repo/rabbitmq-docker.yml`

```yaml
spring:
  rabbitmq:
    host: rabbitmq
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

**Detailed Explanation:**

**Difference from rabbitmq.yml:**

**`host: rabbitmq`**
- **Purpose**: RabbitMQ server hostname in Docker
- **Value**: rabbitmq - Docker service name
- **Why Different**: Docker Compose service name instead of localhost

**All Other Settings**: Same as rabbitmq.yml

**Docker Compose Integration:**

```yaml
# In docker-compose.yml
services:
  rabbitmq:
    image: rabbitmq:3-management
    hostname: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
```

- **Service Name**: rabbitmq
- **Hostname**: rabbitmq (matches config)
- **Ports**: 5672 (AMQP), 15672 (Management UI)
- **Environment**: Sets default username and password

---

## Message Flow

### Complete Message Lifecycle

#### 1. Order Placed Scenario

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Customer Places Order                                   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Order Service Creates Order                              │
│ - Saves order to database                                        │
│ - Creates OrderEvent using createOrderPlacedEvent()             │
│   - messageId: UUID                                             │
│   - eventType: "ORDER_PLACED"                                   │
│   - orderId: 123                                                │
│   - customerId: 456                                             │
│   - restaurantId: 789                                           │
│   - totalAmount: 25.50                                          │
│   - orderStatus: PLACED                                         │
│   - timestamp: 2024-05-26T10:30:00                              │
│   - correlationId: UUID                                         │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Order Service Publishes Event                           │
│ - Calls messageProducer.sendOrderEvent(event)                   │
│ - AmqpTemplate converts event to JSON                           │
│ - Publishes to "order.exchange" with routing key "order.created"│
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: RabbitMQ Receives Message                              │
│ - Exchange: order.exchange                                       │
│ - Routing Key: order.created                                    │
│ - Checks bindings                                               │
│ - Finds binding: order.queue bound with "order.created"         │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: RabbitMQ Routes Message                                 │
│ - Routes message to order.queue                                 │
│ - Message stored in queue                                        │
│ - Waits for consumer                                            │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Notification Service Consumes Message                   │
│ - @RabbitListener on notification.queue                         │
│ - Deserializes JSON to OrderEvent                                │
│ - Calls handleOrderEvent(event)                                 │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Idempotency Check                                        │
│ - Checks if messageId already processed                          │
│ - First time: returns false                                      │
│ - Continues processing                                           │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 8: Event Type Processing                                    │
│ - Switch on eventType: "ORDER_PLACED"                           │
│ - Calls sendNotification()                                      │
│ - Creates NotificationRequestDto                                │
│ - Sets userId, message, type                                    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 9: Send Notification                                       │
│ - Calls notificationService.sendNotification()                  │
│ - Saves notification to database                                │
│ - Sends email/SMS to customer                                   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 10: Mark as Processed                                       │
│ - Calls idempotencyHandler.markMessageAsProcessed()             │
│ - Adds messageId to cache with timestamp                         │
│ - Logs success                                                  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 11: Acknowledge Message                                     │
│ - RabbitMQ auto-acks on successful processing                   │
│ - Message removed from queue                                     │
└─────────────────────────────────────────────────────────────────┘
```

#### 2. Message Failure and Retry Scenario

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Message Received                                         │
│ - Consumer receives message from queue                          │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Processing Starts                                        │
│ - Idempotency check passes                                      │
│ - Event type processing begins                                   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Exception Thrown                                         │
│ - Database connection fails                                      │
│ - Exception thrown in consumer                                  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Exception Propagates                                    │
│ - Exception not caught in consumer                              │
│ - Propagates to RabbitMQ listener container                     │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Retry Triggered                                          │
│ - RabbitMQ sees exception                                        │
│ - Does not acknowledge message                                  │
│ - Message re-queued                                             │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Retry Delay                                              │
│ - Waits 1 second (initial-interval)                             │
│ - Exponential backoff: 1s, 2s, 4s, 8s, 10s (max)              │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Retry Attempt 1                                          │
│ - Message redelivered to consumer                               │
│ - Processing attempted again                                    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
                    (Success?)
                    ↙        ↘
                  Yes          No
                  ↓            ↓
┌──────────────┐  ┌──────────────────────┐
│ Acknowledge  │  │ Retry Attempt 2      │
│ Message      │  │ Wait 2 seconds       │
└──────────────┘  └──────────────────────┘
                         │
                         ↓
                    (Success?)
                    ↙        ↘
                  Yes          No
                  ↓            ↓
┌──────────────┐  ┌──────────────────────┐
│ Acknowledge  │  │ Retry Attempt 3      │
│ Message      │  │ Wait 4 seconds       │
└──────────────┘  └──────────────────────┘
                         │
                         ↓
                    (Success?)
                    ↙        ↘
                  Yes          No
                  ↓            ↓
┌──────────────┐  ┌──────────────────────┐
│ Acknowledge  │  │ Max Attempts Reached│
│ Message      │  │ Send to DLQ          │
└──────────────┘  └──────────────────────┘
```

#### 3. Duplicate Message Scenario

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Message Delivered First Time                            │
│ - Consumer receives message                                     │
│ - messageId: abc-123-def                                         │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Idempotency Check                                        │
│ - Checks cache for messageId abc-123-def                          │
│ - Not found in cache                                             │
│ - Returns false (not processed)                                 │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Process Message                                          │
│ - Event type processing                                         │
│ - Business logic executed                                         │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Mark as Processed                                       │
│ - Adds messageId abc-123-def to cache                           │
│ - Timestamp: current time                                      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Acknowledge Message                                     │
│ - Message acknowledged                                          │
│ - Removed from queue                                            │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Network Issue - Message Redelivered                     │
│ - RabbitMQ redelivers same message                               │
│ - Same messageId: abc-123-def                                    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Idempotency Check (Second Time)                         │
│ - Checks cache for messageId abc-123-def                          │
│ - Found in cache                                                 │
│ - Returns true (already processed)                               │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 8: Skip Processing                                         │
│ - Logs "Skipping duplicate message"                              │
│ - Returns early                                                  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│ Step 9: Acknowledge Message                                     │
│ - Message acknowledged                                          │
│ - Removed from queue                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

### 1. Message Design

**DO:**
- Use immutable event objects
- Include all necessary data in the event
- Use meaningful event type names
- Include timestamps and correlation IDs
- Use builder pattern for event creation
- Validate event data before publishing

**DON'T:**
- Include sensitive data (passwords, tokens)
- Make events too large (> 1MB)
- Use complex nested structures
- Omit required fields
- Change event structure without versioning

### 2. Error Handling

**DO:**
- Log all exceptions with context
- Use specific exception types
- Implement retry with exponential backoff
- Use DLQ for failed messages
- Monitor DLQ size
- Alert on high failure rates

**DON'T:**
- Swallow exceptions silently
- Use generic Exception type
- Retry indefinitely
- Ignore DLQ messages
- Log without context

### 3. Idempotency

**DO:**
- Always check idempotency before processing
- Mark messages as processed after success
- Use appropriate TTL for cache
- Clean up expired entries
- Consider distributed cache for multi-instance

**DON'T:**
- Skip idempotency check
- Mark as processed before success
- Use infinite TTL
- Ignore cache cleanup
- Use in-memory cache for distributed systems

### 4. Configuration

**DO:**
- Externalize configuration (YAML files)
- Use environment-specific configs
- Secure credentials (use secrets)
- Document configuration values
- Test configuration changes
- Monitor configuration changes

**DON'T:**
- Hardcode configuration values
- Use same config for all environments
- Commit credentials to version control
- Use unclear configuration names
- Change config without testing

### 5. Monitoring

**DO:**
- Monitor queue sizes
- Track message processing times
- Alert on DLQ growth
- Monitor consumer lag
- Track success/failure rates
- Log message IDs for tracing

**DON'T:**
- Ignore monitoring
- Set alerts too high/low
- Monitor only success metrics
- Ignore DLQ
- Log without correlation IDs

### 6. Testing

**DO:**
- Test message publishing
- Test message consumption
- Test error scenarios
- Test retry mechanism
- Test idempotency
- Test with embedded RabbitMQ

**DON'T:**
- Skip integration tests
- Test only happy path
- Ignore error cases
- Assume retry works
- Skip idempotency tests
- Test only with mock RabbitMQ

### 7. Performance

**DO:**
- Use connection pooling
- Batch messages when possible
- Monitor thread pool usage
- Tune prefetch count
- Use appropriate queue durability
- Monitor memory usage

**DON'T:**
- Create new connections per message
- Send messages one-by-one unnecessarily
- Ignore thread pool configuration
- Use default prefetch count
- Make all queues durable unnecessarily
- Ignore memory metrics

### 8. Security

**DO:**
- Use SSL/TLS for connections
- Authenticate with strong credentials
- Authorize queue/exchange access
- Encrypt sensitive message data
- Use network segmentation
- Regularly update RabbitMQ

**DON'T:**
- Use unencrypted connections
- Use default credentials
- Grant excessive permissions
- Send sensitive data in plain text
- Expose RabbitMQ to internet
- Skip security updates

---

## Summary

This messaging implementation provides a robust, event-driven architecture for the food delivery microservices system. Key features include:

### Core Components

1. **RabbitMQ Configuration**: Exchanges, queues, bindings, and DLQ setup
2. **Message Events**: OrderEvent, NotificationEvent, DeliveryEvent with factory methods
3. **Message Producer**: Service for publishing events to RabbitMQ
4. **Message Consumers**: Services for consuming and processing events
5. **Idempotency Handler**: Ensures exactly-once processing
6. **Retry Mechanism**: Automatic retry with exponential backoff
7. **Dead Letter Queue**: Failed message storage for inspection

### Key Benefits

- **Decoupling**: Services communicate without direct dependencies
- **Reliability**: Message delivery guarantees with acknowledgments
- **Scalability**: Asynchronous processing improves throughput
- **Resilience**: Retry mechanism handles transient failures
- **Observability**: Logging and monitoring for debugging
- **Flexibility**: Easy to add new consumers and event types

### Message Flow

1. Producer creates event using factory method
2. Producer publishes event to exchange with routing key
3. Exchange routes message to appropriate queue
4. Consumer receives message from queue
5. Consumer checks idempotency
6. Consumer processes event based on type
7. Consumer marks message as processed
8. Consumer acknowledges message
9. RabbitMQ removes message from queue

### Error Handling

1. Consumer throws exception
2. RabbitMQ re-queues message
3. Retry with exponential backoff
4. After max retries, send to DLQ
5. Monitor and reprocess from DLQ

This implementation follows best practices for messaging in microservices and provides a solid foundation for event-driven communication between services.
