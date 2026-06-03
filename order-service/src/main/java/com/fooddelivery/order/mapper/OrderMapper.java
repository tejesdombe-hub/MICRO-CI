package com.fooddelivery.order.mapper;

import com.fooddelivery.order.dto.OrderResponseDto;
import com.fooddelivery.order.entity.Order;
import org.springframework.stereotype.Component;

@Component
public class OrderMapper {

    public OrderResponseDto toResponse(Order order) {
        return OrderResponseDto.builder()
                .id(order.getId())
                .customerId(order.getCustomerId())
                .restaurantId(order.getRestaurantId())
                .totalAmount(order.getTotalAmount())
                .orderStatus(order.getOrderStatus())
                .deliveryPartnerId(order.getDeliveryPartnerId())
                .build();
    }
}
