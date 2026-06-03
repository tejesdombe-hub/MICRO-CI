package com.fooddelivery.notification.dto;
import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; import lombok.Data;
@Data public class NotificationRequestDto {
    @NotNull private Long userId; @NotBlank private String message; @NotBlank private String type;
}
