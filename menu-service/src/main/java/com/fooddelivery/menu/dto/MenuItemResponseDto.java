package com.fooddelivery.menu.dto;
import lombok.*;
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class MenuItemResponseDto { private Long id; private Long restaurantId; private String itemName; private String description; private Double price; private Boolean availability; }
