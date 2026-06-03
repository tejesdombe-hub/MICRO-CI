package com.fooddelivery.payment.dto;
import jakarta.validation.constraints.*; import lombok.Data;
@Data public class PaymentRequestDto {
    @NotNull private Long orderId; @Positive private Double amount; @NotBlank private String paymentMethod;
}
