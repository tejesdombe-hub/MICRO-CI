package com.fooddelivery.customer.dto;

import lombok.*;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class CustomerResponseDto {
    private Long id;
    private String name;
    private String email;
    private String phone;
    private String address;
}
