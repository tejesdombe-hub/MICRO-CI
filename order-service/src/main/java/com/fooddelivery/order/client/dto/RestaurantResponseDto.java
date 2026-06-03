package com.fooddelivery.order.client.dto;

import lombok.Data;

@Data
public class RestaurantResponseDto {
    private Long id;
    private String restaurantName;
    private String ownerName;
    private String address;
    private Double rating;
}
