package com.fooddelivery.common.messaging.producer;

import com.fooddelivery.common.messaging.config.RabbitMQConfig;
import com.fooddelivery.common.messaging.event.DeliveryEvent;
import com.fooddelivery.common.messaging.event.NotificationEvent;
import com.fooddelivery.common.messaging.event.OrderEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class MessageProducer {

    private final AmqpTemplate amqpTemplate;

    public void sendOrderEvent(OrderEvent event) {
        log.info("Sending order event: {} for order: {}", event.getEventType(), event.getOrderId());
        try {
            // Send to appropriate routing key based on event type
            String routingKey = determineRoutingKey(event.getEventType());
            amqpTemplate.convertAndSend(
                    RabbitMQConfig.ORDER_EXCHANGE,
                    routingKey,
                    event
            );
            log.info("Order event sent successfully: messageId={}, routingKey={}", event.getMessageId(), routingKey);
        } catch (Exception e) {
            log.error("Failed to send order event: messageId={}, error={}", event.getMessageId(), e.getMessage(), e);
            throw new RuntimeException("Failed to send order event", e);
        }
    }

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
}
