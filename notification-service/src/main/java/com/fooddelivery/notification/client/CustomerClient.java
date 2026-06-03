package com.fooddelivery.notification.client;

import com.fooddelivery.notification.client.dto.CustomerResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "customer-service", url = "${customer.service.url:http://localhost:8082}")
public interface CustomerClient {

    @GetMapping("/customers/{id}")
    CustomerResponseDto getCustomer(@PathVariable Long id);
}
