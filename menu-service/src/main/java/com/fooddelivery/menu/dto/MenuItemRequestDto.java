package com.fooddelivery.menu.dto;
import jakarta.validation.constraints.*; import lombok.Data;
@Data public class MenuItemRequestDto {
    @NotNull private Long restaurantId; @NotBlank private String itemName; private String description;
    @Positive private Double price; @NotNull private Boolean availability;
}
