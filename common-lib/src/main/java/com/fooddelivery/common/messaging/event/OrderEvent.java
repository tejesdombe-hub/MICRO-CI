package com.fooddelivery.common.messaging.event;

import com.fooddelivery.common.enums.OrderStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
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
}
