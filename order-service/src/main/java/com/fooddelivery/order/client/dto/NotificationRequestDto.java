package com.fooddelivery.order.client.dto;

import lombok.Data;

@Data
public class NotificationRequestDto {
    private Long userId;
    private String message;
    private String type;
}
