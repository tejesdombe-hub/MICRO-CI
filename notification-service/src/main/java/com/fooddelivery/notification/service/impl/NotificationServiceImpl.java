package com.fooddelivery.notification.service.impl;

import com.fooddelivery.notification.dto.*;
import com.fooddelivery.notification.entity.Notification;
import com.fooddelivery.notification.mapper.NotificationMapper;
import com.fooddelivery.notification.repository.NotificationRepository;
import com.fooddelivery.notification.service.NotificationService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
public class NotificationServiceImpl implements NotificationService {

    private static final Logger log = LoggerFactory.getLogger(NotificationServiceImpl.class);

    private final NotificationRepository repository;
    private final NotificationMapper mapper;

    public NotificationServiceImpl(NotificationRepository repository, NotificationMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @Override
    @Transactional
    public NotificationResponseDto send(NotificationRequestDto request) {
        Notification saved = repository.save(mapper.toEntity(request));
        log.info("Notification sent to user {}: {}", request.getUserId(), request.getMessage());
        return mapper.toResponse(saved);
    }

    @Override
    public List<NotificationResponseDto> getByUserId(Long userId) {
        return repository.findByUserId(userId).stream().map(mapper::toResponse).toList();
    }

    @Override
    @Async("taskExecutor")
    public CompletableFuture<Void> sendAsync(NotificationRequestDto request) {
        log.info("Starting async notification send for user {} on thread: {}", 
                request.getUserId(), Thread.currentThread().getName());
        
        try {
            // Simulate notification processing delay
            Thread.sleep(500);
            
            Notification saved = repository.save(mapper.toEntity(request));
            log.info("Async notification sent successfully to user {}: {}", 
                    request.getUserId(), request.getMessage());
            
            return CompletableFuture.completedFuture(null);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Async notification send interrupted for user {}", request.getUserId(), e);
            return CompletableFuture.failedFuture(e);
        } catch (Exception e) {
            log.error("Async notification send failed for user {}", request.getUserId(), e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Override
    @Async("taskExecutor")
    public CompletableFuture<Void> sendEmailAsync(String to, String subject, String body) {
        log.info("Starting async email send to {} on thread: {}", to, Thread.currentThread().getName());
        
        try {
            // Simulate email sending delay (real implementation would use JavaMail or similar)
            Thread.sleep(2000);
            
            log.info("Email sent successfully to {} with subject: {}", to, subject);
            
            // Also save as notification record
            NotificationRequestDto notification = new NotificationRequestDto();
            notification.setUserId(0L); // Email notifications may not have user ID
            notification.setMessage("Email sent: " + subject);
            notification.setType("EMAIL");
            repository.save(mapper.toEntity(notification));
            
            return CompletableFuture.completedFuture(null);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Async email send interrupted for {}", to, e);
            return CompletableFuture.failedFuture(e);
        } catch (Exception e) {
            log.error("Async email send failed for {}", to, e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Override
    @Async("taskExecutor")
    public CompletableFuture<String> generateReportAsync(Long userId) {
        log.info("Starting async report generation for user {} on thread: {}", 
                userId, Thread.currentThread().getName());
        
        try {
            // Simulate report generation delay
            Thread.sleep(3000);
            
            List<Notification> notifications = repository.findByUserId(userId);
            String report = String.format(
                    "User Notification Report - Generated at: %s\n" +
                    "Total Notifications: %d\n" +
                    "Types: %s",
                    LocalDateTime.now(),
                    notifications.size(),
                    notifications.stream()
                            .map(n -> n.getType())
                            .distinct()
                            .toList()
            );
            
            log.info("Report generated successfully for user {}", userId);
            return CompletableFuture.completedFuture(report);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Async report generation interrupted for user {}", userId, e);
            return CompletableFuture.failedFuture(e);
        } catch (Exception e) {
            log.error("Async report generation failed for user {}", userId, e);
            return CompletableFuture.failedFuture(e);
        }
    }
}
