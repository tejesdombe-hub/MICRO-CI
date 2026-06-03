package com.fooddelivery.order.client;

import com.fooddelivery.order.client.dto.PaymentRequestDto;
import com.fooddelivery.order.client.dto.PaymentResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "payment-service", path = "/payments")
public interface PaymentClient {

    @PostMapping("/process")
    PaymentResponseDto processPayment(@RequestBody PaymentRequestDto request);
}
