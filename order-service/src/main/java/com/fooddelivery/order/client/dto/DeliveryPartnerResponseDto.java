package com.fooddelivery.order.client.dto;

import com.fooddelivery.common.enums.DeliveryStatus;
import lombok.Data;

@Data
public class DeliveryPartnerResponseDto {
    private Long id;
    private String name;
    private String phone;
    private String vehicleNumber;
    private Long currentOrderId;
    private DeliveryStatus deliveryStatus;
}
