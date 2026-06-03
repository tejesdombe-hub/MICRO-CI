package com.fooddelivery.restaurant.dto;
import jakarta.validation.constraints.*; import lombok.Data;
@Data public class RestaurantRequestDto {
    @NotBlank private String restaurantName; @NotBlank private String ownerName; @NotBlank private String address;
    @Min(0) @Max(5) private Double rating;
}
