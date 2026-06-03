package com.fooddelivery.customer.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class CustomerRequestDto {
    @NotBlank private String name;
    @NotBlank @Email private String email;
    @NotBlank @Pattern(regexp = "^[0-9]{10}$", message = "Phone must be 10 digits") private String phone;
    @NotBlank private String address;
}
