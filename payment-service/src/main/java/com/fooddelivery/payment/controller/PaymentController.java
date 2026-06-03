package com.fooddelivery.payment.controller;
import com.fooddelivery.payment.dto.*; import com.fooddelivery.payment.service.PaymentService;
import io.swagger.v3.oas.annotations.tags.Tag; import jakarta.validation.Valid;
import org.springframework.http.*; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/payments") @Tag(name="Payments")
public class PaymentController {
    private final PaymentService service;
    public PaymentController(PaymentService service) { this.service = service; }
    @PostMapping("/process") public ResponseEntity<PaymentResponseDto> process(@Valid @RequestBody PaymentRequestDto request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.process(request));
    }
    @GetMapping("/order/{orderId}") public ResponseEntity<PaymentResponseDto> getByOrder(@PathVariable Long orderId) {
        return ResponseEntity.ok(service.getByOrderId(orderId));
    }
}
