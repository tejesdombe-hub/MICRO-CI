package com.fooddelivery.order.dto;

import com.fooddelivery.common.enums.OrderStatus;
import jakarta.validation.constraints.NotNull;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class OrderStatusUpdateRequestDto {

    @NotNull(message = "Order status is required")
    private OrderStatus orderStatus;
}
