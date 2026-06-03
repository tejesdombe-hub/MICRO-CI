package com.fooddelivery.payment.service.impl;
import com.fooddelivery.common.enums.PaymentStatus;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.payment.dto.*;
import com.fooddelivery.payment.entity.Payment;
import com.fooddelivery.payment.mapper.PaymentMapper;
import com.fooddelivery.payment.repository.PaymentRepository;
import com.fooddelivery.payment.service.PaymentService;
import org.slf4j.Logger; import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional;
@Service public class PaymentServiceImpl implements PaymentService {
    private static final Logger log = LoggerFactory.getLogger(PaymentServiceImpl.class);
    private final PaymentRepository repository; private final PaymentMapper mapper;
    public PaymentServiceImpl(PaymentRepository repository, PaymentMapper mapper) { this.repository = repository; this.mapper = mapper; }
    @Override @Transactional public PaymentResponseDto process(PaymentRequestDto request) {
        Payment payment = repository.save(mapper.toEntity(request));
        payment.setPaymentStatus(PaymentStatus.SUCCESS);
        log.info("Payment simulated SUCCESS for order {}", request.getOrderId());
        return mapper.toResponse(repository.save(payment));
    }
    @Override public PaymentResponseDto getByOrderId(Long orderId) {
        return mapper.toResponse(repository.findByOrderId(orderId).orElseThrow(() -> new ResourceNotFoundException("Payment not found for order: " + orderId)));
    }
}
