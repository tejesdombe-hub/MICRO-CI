package com.fooddelivery.order.service;

import com.fooddelivery.order.dto.OrderRequestDto;
import com.fooddelivery.order.dto.OrderResponseDto;
import com.fooddelivery.order.dto.OrderStatusUpdateRequestDto;

import java.util.List;

public interface OrderService {
    OrderResponseDto placeOrder(OrderRequestDto request);
    OrderResponseDto getById(Long id);
    List<OrderResponseDto> getByCustomerId(Long customerId);
    OrderResponseDto updateStatus(Long id, OrderStatusUpdateRequestDto request);
    OrderResponseDto assignDelivery(Long id);
}
