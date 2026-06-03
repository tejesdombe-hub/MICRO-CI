package com.fooddelivery.order.client;

import com.fooddelivery.order.client.dto.DeliveryAssignmentRequestDto;
import com.fooddelivery.order.client.dto.DeliveryPartnerResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "delivery-partner-service", path = "/delivery-partners")
public interface DeliveryPartnerClient {

    @PostMapping("/assign")
    DeliveryPartnerResponseDto assignPartner(@RequestBody DeliveryAssignmentRequestDto request);
}
