package com.fooddelivery.delivery.mapper;
import com.fooddelivery.delivery.dto.*; import com.fooddelivery.delivery.entity.DeliveryPartner; import org.springframework.stereotype.Component;
@Component
public class DeliveryPartnerMapper {
    public DeliveryPartner toEntity(DeliveryPartnerRequestDto d){return DeliveryPartner.builder().name(d.getName()).phone(d.getPhone()).vehicleNumber(d.getVehicleNumber()).deliveryStatus(com.fooddelivery.common.enums.DeliveryStatus.AVAILABLE).build();}
    public DeliveryPartnerResponseDto toResponse(DeliveryPartner p){return DeliveryPartnerResponseDto.builder().id(p.getId()).name(p.getName()).phone(p.getPhone()).vehicleNumber(p.getVehicleNumber()).currentOrderId(p.getCurrentOrderId()).deliveryStatus(p.getDeliveryStatus()).build();}
}
