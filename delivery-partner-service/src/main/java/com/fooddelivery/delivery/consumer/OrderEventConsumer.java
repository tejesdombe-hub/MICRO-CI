package com.fooddelivery.delivery.consumer;

import com.fooddelivery.common.messaging.event.OrderEvent;
import com.fooddelivery.common.messaging.idempotency.IdempotencyHandler;
import com.fooddelivery.delivery.dto.DeliveryStatusUpdateRequestDto;
import com.fooddelivery.delivery.service.DeliveryPartnerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class OrderEventConsumer {

    private final DeliveryPartnerService deliveryPartnerService;
    private final IdempotencyHandler idempotencyHandler;

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
}
