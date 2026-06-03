package com.fooddelivery.customer.mapper;

import com.fooddelivery.customer.dto.*;
import com.fooddelivery.customer.entity.Customer;
import org.springframework.stereotype.Component;

@Component
public class CustomerMapper {
    public Customer toEntity(CustomerRequestDto dto) {
        return Customer.builder().name(dto.getName()).email(dto.getEmail()).phone(dto.getPhone()).address(dto.getAddress()).build();
    }
    public CustomerResponseDto toResponse(Customer c) {
        return CustomerResponseDto.builder().id(c.getId()).name(c.getName()).email(c.getEmail()).phone(c.getPhone()).address(c.getAddress()).build();
    }
    public void updateEntity(Customer c, CustomerRequestDto dto) {
        c.setName(dto.getName()); c.setEmail(dto.getEmail()); c.setPhone(dto.getPhone()); c.setAddress(dto.getAddress());
    }
}
