package com.fooddelivery.notification.controller;

import com.fooddelivery.notification.dto.*;
import com.fooddelivery.notification.service.NotificationService;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/notifications")
@Tag(name="Notifications")
public class NotificationController {

    private static final Logger log = LoggerFactory.getLogger(NotificationController.class);
    private final NotificationService service;

    public NotificationController(NotificationService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<NotificationResponseDto> send(@Valid @RequestBody NotificationRequestDto request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.send(request));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<NotificationResponseDto>> byUser(@PathVariable Long userId) {
        return ResponseEntity.ok(service.getByUserId(userId));
    }

    // Async endpoints
    @PostMapping("/async")
    public ResponseEntity<String> sendAsync(@Valid @RequestBody NotificationRequestDto request) {
        log.info("Received async notification request for user {}", request.getUserId());
        service.sendAsync(request);
        return ResponseEntity.accepted().body("Notification is being processed asynchronously");
    }

    @PostMapping("/email")
    public ResponseEntity<String> sendEmail(
            @RequestParam String to,
            @RequestParam String subject,
            @RequestParam String body) {
        log.info("Received async email request to {}", to);
        service.sendEmailAsync(to, subject, body);
        return ResponseEntity.accepted().body("Email is being sent asynchronously");
    }

    @GetMapping("/report/{userId}")
    public CompletableFuture<ResponseEntity<String>> generateReport(@PathVariable Long userId) {
        log.info("Received report generation request for user {}", userId);
        return service.generateReportAsync(userId)
                .thenApply(report -> ResponseEntity.ok(report));
    }
}
