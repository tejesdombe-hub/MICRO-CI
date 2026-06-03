package com.fooddelivery.order.dto;

import com.fooddelivery.common.enums.OrderStatus;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class OrderStatusUpdateRequestDto {

    @NotNull(message = "Order status is required")
    private OrderStatus orderStatus;
}
