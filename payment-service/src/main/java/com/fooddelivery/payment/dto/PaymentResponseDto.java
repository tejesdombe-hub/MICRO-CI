package com.fooddelivery.payment.dto;
import com.fooddelivery.common.enums.PaymentStatus; import lombok.*;
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class PaymentResponseDto { private Long id; private Long orderId; private Double amount; private PaymentStatus paymentStatus; private String paymentMethod; }
