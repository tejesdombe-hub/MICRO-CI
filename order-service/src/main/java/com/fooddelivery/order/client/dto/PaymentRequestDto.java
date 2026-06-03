package com.fooddelivery.order.client.dto;

import lombok.Data;

@Data
public class PaymentRequestDto {
    private Long orderId;
    private Double amount;
    private String paymentMethod;
}
