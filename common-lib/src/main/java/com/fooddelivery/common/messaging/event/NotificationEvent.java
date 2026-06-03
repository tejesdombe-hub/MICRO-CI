package com.fooddelivery.common.messaging.event;

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
public class NotificationEvent {
    private String messageId;
    private String eventType;
    private Long userId;
    private String message;
    private String type;
    private String channel;
    private LocalDateTime timestamp;
    private String correlationId;

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
}
