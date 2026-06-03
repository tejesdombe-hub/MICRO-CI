package com.fooddelivery.order.client.dto;

import com.fooddelivery.common.enums.PaymentStatus;
import lombok.Data;

@Data
public class PaymentResponseDto {
    private Long id;
    private Long orderId;
    private Double amount;
    private PaymentStatus paymentStatus;
    private String paymentMethod;
}
