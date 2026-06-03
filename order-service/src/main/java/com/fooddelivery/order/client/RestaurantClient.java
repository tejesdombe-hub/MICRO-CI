package com.fooddelivery.order.client;

import com.fooddelivery.order.client.dto.RestaurantResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "restaurant-service", path = "/restaurants")
public interface RestaurantClient {

    @GetMapping("/{id}")
    RestaurantResponseDto getRestaurant(@PathVariable("id") Long id);
}
