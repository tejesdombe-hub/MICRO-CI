package com.fooddelivery.order.client;

import com.fooddelivery.order.client.dto.CustomerResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "customer-service", path = "/customers")
public interface CustomerClient {

    @GetMapping("/{id}")
    CustomerResponseDto getCustomer(@PathVariable("id") Long id);
}

