package com.fooddelivery.payment.mapper;
import com.fooddelivery.common.enums.PaymentStatus;
import com.fooddelivery.payment.dto.*; import com.fooddelivery.payment.entity.Payment; import org.springframework.stereotype.Component;
@Component public class PaymentMapper {
    public Payment toEntity(PaymentRequestDto d){return Payment.builder().orderId(d.getOrderId()).amount(d.getAmount()).paymentMethod(d.getPaymentMethod()).paymentStatus(PaymentStatus.PENDING).build();}
    public PaymentResponseDto toResponse(Payment p){return PaymentResponseDto.builder().id(p.getId()).orderId(p.getOrderId()).amount(p.getAmount()).paymentStatus(p.getPaymentStatus()).paymentMethod(p.getPaymentMethod()).build();}
}
