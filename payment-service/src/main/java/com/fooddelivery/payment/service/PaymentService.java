package com.fooddelivery.payment.service;
import com.fooddelivery.payment.dto.*;
public interface PaymentService {
 PaymentResponseDto process(PaymentRequestDto request);
 PaymentResponseDto getByOrderId(Long orderId);
}
