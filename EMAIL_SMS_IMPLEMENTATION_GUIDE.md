# Email and SMS Implementation via RabbitMQ

## Overview
This implementation adds actual email and SMS sending capabilities to the Food Delivery Platform using RabbitMQ messaging. When an order is placed, confirmed, or delivered, the system automatically sends email and SMS notifications to customers.

## Architecture

### Message Flow
```
Order Service (Producer)
    ↓ (RabbitMQ Event)
OrderEventConsumer (Notification Service)
    ↓
EmailService & SmsService
    ↓
Customer Email & Phone
```

### Components

#### 1. MessageProducer (common-lib)
**File**: `common-lib/src/main/java/com/fooddelivery/common/messaging/producer/MessageProducer.java`

**Changes Made**:
- Fixed routing key logic to send events to appropriate queues
- Added `determineRoutingKey()` method to route events based on type
- ORDER_PLACED, ORDER_CONFIRMED, ORDER_DELIVERED → notification.queue
- DELIVERY_ASSIGNED → delivery.queue

```java
private String determineRoutingKey(String eventType) {
    switch (eventType) {
        case "ORDER_PLACED":
        case "ORDER_CONFIRMED":
        case "ORDER_DELIVERED":
            return RabbitMQConfig.NOTIFICATION_ROUTING_KEY;
        case "DELIVERY_ASSIGNED":
            return RabbitMQConfig.DELIVERY_ROUTING_KEY;
        default:
            return RabbitMQConfig.ORDER_ROUTING_KEY;
    }
}
```

#### 2. EmailService (notification-service)
**Files**:
- `notification-service/src/main/java/com/fooddelivery/notification/service/EmailService.java`
- `notification-service/src/main/java/com/fooddelivery/notification/service/impl/EmailServiceImpl.java`

**Features**:
- Uses Spring Boot Mail with JavaMailSender
- Thymeleaf templates for HTML emails
- Configurable enable/disable via `app.email.enabled`
- Methods:
  - `sendEmail()` - Generic email sending
  - `sendOrderConfirmationEmail()` - Order confirmation with template
  - `sendOrderDeliveredEmail()` - Delivery confirmation with template

**Dependencies Added**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

#### 3. SmsService (notification-service)
**Files**:
- `notification-service/src/main/java/com/fooddelivery/notification/service/SmsService.java`
- `notification-service/src/main/java/com/fooddelivery/notification/service/impl/SmsServiceImpl.java`

**Features**:
- Uses Twilio API for SMS sending
- Configurable enable/disable via `app.sms.enabled`
- Methods:
  - `sendSms()` - Generic SMS sending
  - `sendOrderConfirmationSms()` - Order confirmation SMS
  - `sendOrderDeliveredSms()` - Delivery confirmation SMS

**Dependencies Added**:
```xml
<dependency>
    <groupId>com.twilio.sdk</groupId>
    <artifactId>twilio</artifactId>
    <version>8.31.1</version>
</dependency>
```

#### 4. OrderEventConsumer (notification-service)
**File**: `notification-service/src/main/java/com/fooddelivery/notification/consumer/OrderEventConsumer.java`

**Changes Made**:
- Added EmailService and SmsService dependencies
- Created separate handler methods for each event type:
  - `handleOrderPlaced()` - Sends confirmation email + SMS
  - `handleOrderConfirmed()` - Saves notification record
  - `handleOrderDelivered()` - Sends delivery email + SMS
- Maintains idempotency to prevent duplicate processing

#### 5. Email Templates
**Files**:
- `notification-service/src/main/resources/templates/email/order-confirmation.html`
- `notification-service/src/main/resources/templates/email/order-delivered.html`

**Features**:
- Professional HTML email templates with CSS styling
- Dynamic content using Thymeleaf variables
- Responsive design
- Order confirmation template shows order ID and amount
- Delivery confirmation template shows delivery time

## Configuration

### Local Development (notification-service.yml)
```yaml
spring:
  mail:
    host: smtp.gmail.com
    port: 587
    username: your-email@gmail.com
    password: your-app-password
    properties:
      mail:
        smtp:
          auth: true
          starttls:
            enable: true

app:
  email:
    enabled: true
  sms:
    enabled: true

twilio:
  account:
    sid: your-twilio-account-sid
  auth:
    token: your-twilio-auth-token
  phone:
    number: your-twilio-phone-number
```

### Docker (notification-service-docker.yml & docker-compose.yml)
Environment variables for secure configuration:
- `SPRING_MAIL_USERNAME`
- `SPRING_MAIL_PASSWORD`
- `APP_EMAIL_ENABLED`
- `APP_SMS_ENABLED`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`

## Setup Instructions

### 1. Email Configuration (Gmail)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security → App Passwords
   - Create a new app password for "Mail"
   - Use this password in the configuration

### 2. SMS Configuration (Twilio)
1. Sign up for a Twilio account at https://www.twilio.com
2. Get your Account SID and Auth Token from the Twilio Console
3. Purchase a phone number or use the trial number
4. Update the configuration with your credentials

### 3. Build and Run
```bash
# Build the project
mvn clean install

# Run with Docker Compose
docker-compose up -d

# Or run locally
cd notification-service
mvn spring-boot:run
```

## Testing

### Manual Testing via API
```bash
# Create an order (triggers ORDER_PLACED and ORDER_CONFIRMED events)
curl -X POST http://localhost:8085/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 1,
    "restaurantId": 1,
    "totalAmount": 100.00,
    "paymentMethod": "UPI"
  }'

# Update order to delivered (triggers ORDER_DELIVERED event)
curl -X PUT http://localhost:8085/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{"orderStatus": "DELIVERED"}'
```

### Verify via Logs
```bash
# Check notification-service logs
docker logs fd-notification -f

# Look for:
# - "Received order event: ORDER_PLACED for order: X"
# - "Order confirmation email sent to: ..."
# - "Order confirmation SMS sent to: ..."
```

### Verify via RabbitMQ Management UI
1. Open http://localhost:15672 (admin/admin)
2. Check `notification.queue` - should have 0 messages (consumed)
3. Check message rates to confirm flow

## Event Types and Notifications

| Event Type | Email | SMS | Database Record |
|------------|-------|-----|-----------------|
| ORDER_PLACED | ✓ (Confirmation) | ✓ (Confirmation) | ✓ |
| ORDER_CONFIRMED | - | - | ✓ |
| ORDER_DELIVERED | ✓ (Delivery) | ✓ (Delivery) | ✓ |

## Production Considerations

### 1. Customer Contact Information
Currently using placeholder values. In production:
- Fetch customer email from Customer Service via Feign client
- Fetch customer phone from Customer Service via Feign client
- Cache frequently accessed customer data

### 2. Error Handling
- Email and SMS failures are logged but don't block the main flow
- Consider adding retry logic for failed sends
- Implement dead letter queue for failed notifications

### 3. Rate Limiting
- Implement rate limiting for SMS to avoid Twilio costs
- Batch email sends for efficiency
- Consider using a message queue for email/SMS sending

### 4. Security
- Never commit actual credentials to version control
- Use environment variables or secret management
- Rotate credentials regularly
- Use app-specific passwords for email

### 5. Monitoring
- Track email delivery rates
- Monitor SMS costs
- Set up alerts for failed notifications
- Log delivery confirmations

## Troubleshooting

### Email Not Sending
1. Check Gmail app password is correct
2. Verify SMTP settings (host, port)
3. Check if `app.email.enabled` is true
4. Review logs for authentication errors

### SMS Not Sending
1. Verify Twilio credentials
2. Check if phone number is verified (for trial accounts)
3. Ensure `app.sms.enabled` is true
4. Review Twilio dashboard for error messages

### RabbitMQ Messages Not Consumed
1. Verify routing key configuration
2. Check queue bindings in RabbitMQ Management UI
3. Ensure notification-service is running
4. Check consumer logs for connection errors

## Files Modified/Created

### Modified Files
1. `common-lib/src/main/java/com/fooddelivery/common/messaging/producer/MessageProducer.java`
2. `notification-service/pom.xml`
3. `notification-service/src/main/java/com/fooddelivery/notification/consumer/OrderEventConsumer.java`
4. `config-repo/notification-service.yml`
5. `docker-compose.yml`

### Created Files
1. `notification-service/src/main/java/com/fooddelivery/notification/service/EmailService.java`
2. `notification-service/src/main/java/com/fooddelivery/notification/service/impl/EmailServiceImpl.java`
3. `notification-service/src/main/java/com/fooddelivery/notification/service/SmsService.java`
4. `notification-service/src/main/java/com/fooddelivery/notification/service/impl/SmsServiceImpl.java`
5. `notification-service/src/main/resources/templates/email/order-confirmation.html`
6. `notification-service/src/main/resources/templates/email/order-delivered.html`
7. `config-repo/notification-service-docker.yml`

## Summary

This implementation successfully integrates email and SMS sending capabilities into the Food Delivery Platform using RabbitMQ messaging. The system now automatically sends:

- **Order Confirmation**: Email and SMS when an order is placed
- **Delivery Confirmation**: Email and SMS when an order is delivered

The implementation is:
- **Configurable**: Can enable/disable email and SMS independently
- **Scalable**: Uses asynchronous messaging via RabbitMQ
- **Reliable**: Includes idempotency to prevent duplicate processing
- **Professional**: Uses HTML email templates with Thymeleaf
- **Production-ready**: Supports environment variables for secure configuration
