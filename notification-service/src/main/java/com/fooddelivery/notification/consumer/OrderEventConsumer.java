package com.fooddelivery.notification.consumer;

import com.fooddelivery.common.messaging.event.OrderEvent;
import com.fooddelivery.common.messaging.idempotency.IdempotencyHandler;
import com.fooddelivery.notification.client.CustomerClient;
import com.fooddelivery.notification.client.dto.CustomerResponseDto;
import com.fooddelivery.notification.dto.NotificationRequestDto;
import com.fooddelivery.notification.service.EmailService;
import com.fooddelivery.notification.service.NotificationService;
import com.fooddelivery.notification.service.SmsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class OrderEventConsumer {

    private final NotificationService notificationService;
    private final EmailService emailService;
    private final SmsService smsService;
    private final CustomerClient customerClient;
    private final IdempotencyHandler idempotencyHandler;

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
                    handleOrderPlaced(event);
                    break;
                case "ORDER_CONFIRMED":
                    handleOrderConfirmed(event);
                    break;
                case "ORDER_DELIVERED":
                    handleOrderDelivered(event);
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

    private void handleOrderPlaced(OrderEvent event) {
        log.info("Processing ORDER_PLACED event for order: {}", event.getOrderId());
        
        // Fetch customer details
        CustomerResponseDto customer = getCustomerDetails(event.getCustomerId());
        
        // Save notification record
        sendNotification(event.getCustomerId(), 
            "Order #" + event.getOrderId() + " placed successfully", 
            "ORDER_PLACED");
        
        // Send email with actual customer email
        String customerEmail = customer != null ? customer.getEmail() : "customer" + event.getCustomerId() + "@example.com";
        String customerName = customer != null ? customer.getName() : "Customer " + event.getCustomerId();
        try {
            emailService.sendOrderConfirmationEmail(customerEmail, customerName, event.getOrderId(), 
                event.getTotalAmount() != null ? event.getTotalAmount().doubleValue() : 0.0);
        } catch (Exception e) {
            log.error("Failed to send order confirmation email for order: {}", event.getOrderId(), e);
            // Don't throw - continue with SMS
        }
        
        // Send SMS with actual customer phone
        String customerPhone = customer != null ? customer.getPhone() : "+1234567890";
        try {
            smsService.sendOrderConfirmationSms(customerPhone, customerName, event.getOrderId());
        } catch (Exception e) {
            log.error("Failed to send order confirmation SMS for order: {}", event.getOrderId(), e);
            // Don't throw - notification record was already saved
        }
    }

    private void handleOrderConfirmed(OrderEvent event) {
        log.info("Processing ORDER_CONFIRMED event for order: {}", event.getOrderId());
        
        sendNotification(event.getCustomerId(), 
            "Order #" + event.getOrderId() + " confirmed by restaurant", 
            "ORDER_CONFIRMED");
        
        // Could send additional confirmation email/SMS here if needed
    }

    private void handleOrderDelivered(OrderEvent event) {
        log.info("Processing ORDER_DELIVERED event for order: {}", event.getOrderId());
        
        // Fetch customer details
        CustomerResponseDto customer = getCustomerDetails(event.getCustomerId());
        
        sendNotification(event.getCustomerId(), 
            "Order #" + event.getOrderId() + " has been delivered", 
            "ORDER_DELIVERED");
        
        // Send delivery confirmation email with actual customer email
        String customerEmail = customer != null ? customer.getEmail() : "customer" + event.getCustomerId() + "@example.com";
        String customerName = customer != null ? customer.getName() : "Customer " + event.getCustomerId();
        try {
            emailService.sendOrderDeliveredEmail(customerEmail, customerName, event.getOrderId());
        } catch (Exception e) {
            log.error("Failed to send order delivered email for order: {}", event.getOrderId(), e);
            // Don't throw - continue with SMS
        }
        
        // Send delivery confirmation SMS with actual customer phone
        String customerPhone = customer != null ? customer.getPhone() : "+1234567890";
        try {
            smsService.sendOrderDeliveredSms(customerPhone, customerName, event.getOrderId());
        } catch (Exception e) {
            log.error("Failed to send order delivered SMS for order: {}", event.getOrderId(), e);
            // Don't throw - notification record was already saved
        }
    }

    private void sendNotification(Long userId, String message, String type) {
        NotificationRequestDto request = new NotificationRequestDto();
        request.setUserId(userId);
        request.setMessage(message);
        request.setType(type);
        notificationService.send(request);
    }

    private CustomerResponseDto getCustomerDetails(Long customerId) {
        try {
            return customerClient.getCustomer(customerId);
        } catch (Exception e) {
            log.error("Failed to fetch customer details for customerId: {}", customerId, e);
            return null;
        }
    }
}
