package com.fooddelivery.delivery.controller;
import com.fooddelivery.delivery.dto.*;
import com.fooddelivery.delivery.service.DeliveryPartnerService;
import io.swagger.v3.oas.annotations.Operation; import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.web.bind.annotation.*;
import java.util.List;
@RestController @RequestMapping("/delivery-partners") @Tag(name="Delivery Partners")
public class DeliveryPartnerController {
    private final DeliveryPartnerService service;
    public DeliveryPartnerController(DeliveryPartnerService service) { this.service = service; }
    @PostMapping public ResponseEntity<DeliveryPartnerResponseDto> create(@Valid @RequestBody DeliveryPartnerRequestDto request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.create(request));
    }
    @GetMapping("/{id}") public ResponseEntity<DeliveryPartnerResponseDto> get(@PathVariable Long id) { return ResponseEntity.ok(service.getById(id)); }
    @GetMapping public ResponseEntity<List<DeliveryPartnerResponseDto>> all() { return ResponseEntity.ok(service.getAll()); }
    @PostMapping("/assign") @Operation(summary="Assign nearest available partner")
    public ResponseEntity<DeliveryPartnerResponseDto> assign(@Valid @RequestBody DeliveryAssignmentRequestDto request) {
        return ResponseEntity.ok(service.assignNearest(request));
    }
    @PatchMapping("/{id}/status") public ResponseEntity<DeliveryPartnerResponseDto> updateStatus(@PathVariable Long id, @Valid @RequestBody DeliveryStatusUpdateRequestDto request) {
        return ResponseEntity.ok(service.updateStatus(id, request));
    }
}
