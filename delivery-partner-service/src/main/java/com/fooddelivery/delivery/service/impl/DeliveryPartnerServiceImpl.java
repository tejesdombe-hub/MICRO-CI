package com.fooddelivery.delivery.service.impl;
import com.fooddelivery.common.enums.DeliveryStatus;
import com.fooddelivery.common.exception.*;
import com.fooddelivery.delivery.dto.*;
import com.fooddelivery.delivery.entity.DeliveryPartner;
import com.fooddelivery.delivery.mapper.DeliveryPartnerMapper;
import com.fooddelivery.delivery.repository.DeliveryPartnerRepository;
import com.fooddelivery.delivery.service.DeliveryPartnerService;
import org.slf4j.Logger; import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional;
import java.util.List;
@Service public class DeliveryPartnerServiceImpl implements DeliveryPartnerService {
    private static final Logger log = LoggerFactory.getLogger(DeliveryPartnerServiceImpl.class);
    private final DeliveryPartnerRepository repository;
    private final DeliveryPartnerMapper mapper;
    public DeliveryPartnerServiceImpl(DeliveryPartnerRepository repository, DeliveryPartnerMapper mapper) {
        this.repository = repository; this.mapper = mapper;
    }
    @Override @Transactional public DeliveryPartnerResponseDto create(DeliveryPartnerRequestDto request) {
        DeliveryPartner saved = repository.save(mapper.toEntity(request));
        return mapper.toResponse(saved);
    }
    @Override public DeliveryPartnerResponseDto getById(Long id) {
        return mapper.toResponse(repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Delivery partner not found: " + id)));
    }
    @Override public List<DeliveryPartnerResponseDto> getAll() {
        return repository.findAll().stream().map(mapper::toResponse).toList();
    }
    @Override @Transactional public DeliveryPartnerResponseDto assignNearest(DeliveryAssignmentRequestDto request) {
        List<DeliveryPartner> available = repository.findByDeliveryStatus(DeliveryStatus.AVAILABLE);
        if (available.isEmpty()) throw new InvalidRequestException("No delivery partners available");
        DeliveryPartner partner = available.get(0);
        partner.setCurrentOrderId(request.getOrderId());
        partner.setDeliveryStatus(DeliveryStatus.ASSIGNED);
        log.info("Assigned partner {} to order {}", partner.getId(), request.getOrderId());
        return mapper.toResponse(repository.save(partner));
    }
    @Override @Transactional public DeliveryPartnerResponseDto updateStatus(Long id, DeliveryStatusUpdateRequestDto request) {
        DeliveryPartner partner = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Delivery partner not found: " + id));
        partner.setDeliveryStatus(request.getDeliveryStatus());
        if (request.getDeliveryStatus() == DeliveryStatus.DELIVERED) {
            partner.setDeliveryStatus(DeliveryStatus.AVAILABLE);
            partner.setCurrentOrderId(null);
        }
        return mapper.toResponse(repository.save(partner));
    }
}
