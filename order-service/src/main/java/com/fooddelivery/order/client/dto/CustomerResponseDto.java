package com.fooddelivery.order.client.dto;

import lombok.Data;

@Data
public class CustomerResponseDto {
    private Long id;
    private String name;
    private String email;
    private String phone;
    private String address;
}
