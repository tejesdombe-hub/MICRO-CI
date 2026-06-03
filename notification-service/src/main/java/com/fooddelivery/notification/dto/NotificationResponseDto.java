package com.fooddelivery.notification.dto;
import lombok.*; import java.time.LocalDateTime;
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class NotificationResponseDto { private Long id; private Long userId; private String message; private String type; private LocalDateTime sentAt; }
