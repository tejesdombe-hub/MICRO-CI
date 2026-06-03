package com.fooddelivery.common.messaging.event;

import com.fooddelivery.common.enums.DeliveryStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DeliveryEvent {
    private String messageId;
    private String eventType;
    private Long orderId;
    private Long deliveryPartnerId;
    private DeliveryStatus deliveryStatus;
    private LocalDateTime timestamp;
    private String correlationId;

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
}
