package com.fooddelivery.restaurant.dto;
import lombok.*;
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class RestaurantResponseDto { private Long id; private String restaurantName; private String ownerName; private String address; private Double rating; }
