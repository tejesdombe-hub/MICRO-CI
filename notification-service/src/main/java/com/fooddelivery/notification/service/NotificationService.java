package com.fooddelivery.notification.service;

import com.fooddelivery.notification.dto.*;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public interface NotificationService {
    NotificationResponseDto send(NotificationRequestDto request);
    List<NotificationResponseDto> getByUserId(Long userId);
    
    // Async methods
    CompletableFuture<Void> sendAsync(NotificationRequestDto request);
    CompletableFuture<Void> sendEmailAsync(String to, String subject, String body);
    CompletableFuture<String> generateReportAsync(Long userId);
}
