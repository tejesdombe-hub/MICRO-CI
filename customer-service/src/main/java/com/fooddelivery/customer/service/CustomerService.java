package com.fooddelivery.customer.service;

import com.fooddelivery.customer.dto.*;
import java.util.List;

public interface CustomerService {
    CustomerResponseDto create(CustomerRequestDto request);
    CustomerResponseDto getById(Long id);
    List<CustomerResponseDto> getAll();
    CustomerResponseDto update(Long id, CustomerRequestDto request);
    void delete(Long id);
}
