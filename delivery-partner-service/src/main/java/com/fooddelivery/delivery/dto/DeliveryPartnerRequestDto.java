package com.fooddelivery.delivery.dto;
import jakarta.validation.constraints.*; import lombok.Data;
@Data public class DeliveryPartnerRequestDto {
    @NotBlank private String name;
    @Pattern(regexp="^[0-9]{10}$") private String phone;
    @NotBlank private String vehicleNumber;
}
