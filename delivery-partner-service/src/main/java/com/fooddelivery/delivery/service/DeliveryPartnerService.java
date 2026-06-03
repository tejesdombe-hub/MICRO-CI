package com.fooddelivery.delivery.service;
import com.fooddelivery.delivery.dto.*;
import java.util.List;
public interface DeliveryPartnerService {
    DeliveryPartnerResponseDto create(DeliveryPartnerRequestDto request);
    DeliveryPartnerResponseDto getById(Long id);
    List<DeliveryPartnerResponseDto> getAll();
    DeliveryPartnerResponseDto assignNearest(DeliveryAssignmentRequestDto request);
    DeliveryPartnerResponseDto updateStatus(Long id, DeliveryStatusUpdateRequestDto request);
}
