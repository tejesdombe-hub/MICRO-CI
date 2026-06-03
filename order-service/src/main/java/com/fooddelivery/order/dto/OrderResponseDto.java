package com.fooddelivery.order.dto;

import com.fooddelivery.common.enums.OrderStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderResponseDto {
    private Long id;
    private Long customerId;
    private Long restaurantId;
    private Double totalAmount;
    private OrderStatus orderStatus;
    private Long deliveryPartnerId;
}
