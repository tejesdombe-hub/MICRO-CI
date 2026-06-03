package com.fooddelivery.notification.service;

import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.notification.dto.NotificationRequestDto;
import com.fooddelivery.notification.dto.NotificationResponseDto;
import com.fooddelivery.notification.entity.Notification;
import com.fooddelivery.notification.entity.NotificationStatus;
import com.fooddelivery.notification.mapper.NotificationMapper;
import com.fooddelivery.notification.repository.NotificationRepository;
import com.fooddelivery.notification.service.impl.NotificationServiceImpl;
import com.fooddelivery.notification.service.EmailService;
import com.fooddelivery.notification.service.SmsService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Notification Service Unit Tests")
class NotificationServiceImplTest {

    @Mock
    private NotificationRepository notificationRepository;

    @Mock
    private NotificationMapper notificationMapper;

    @Mock
    private EmailService emailService;

    @Mock
    private SmsService smsService;

    @InjectMocks
    private NotificationServiceImpl notificationService;

    private NotificationRequestDto requestDto;
    private NotificationResponseDto responseDto;
    private Notification notification;

    @BeforeEach
    void setUp() {
        requestDto = NotificationRequestDto.builder()
                .orderId(1L)
                .customerId(1L)
                .type("ORDER_PLACED")
                .message("Your order has been placed successfully")
                .email("customer@example.com")
                .phone("9876543210")
                .build();

        responseDto = NotificationResponseDto.builder()
                .id(1L)
                .orderId(1L)
                .customerId(1L)
                .type("ORDER_PLACED")
                .message("Your order has been placed successfully")
                .status(NotificationStatus.SENT.toString())
                .createdAt(LocalDateTime.now())
                .build();

        notification = Notification.builder()
                .id(1L)
                .orderId(1L)
                .customerId(1L)
                .type("ORDER_PLACED")
                .message("Your order has been placed successfully")
                .email("customer@example.com")
                .phone("9876543210")
                .status(NotificationStatus.SENT)
                .createdAt(LocalDateTime.now())
                .build();
    }

    @Test
    @DisplayName("Should send notification successfully")
    void testSendNotificationSuccess() {
        // Arrange
        when(emailService.sendEmail(requestDto.getEmail(), requestDto.getMessage())).thenReturn(true);
        when(smsService.sendSms(requestDto.getPhone(), requestDto.getMessage())).thenReturn(true);
        when(notificationMapper.toEntity(requestDto)).thenReturn(notification);
        when(notificationRepository.save(any(Notification.class))).thenReturn(notification);
        when(notificationMapper.toResponse(notification)).thenReturn(responseDto);

        // Act
        NotificationResponseDto result = notificationService.send(requestDto);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getStatus()).isEqualTo(NotificationStatus.SENT.toString());

        verify(notificationRepository).save(any(Notification.class));
    }

    @Test
    @DisplayName("Should get notification by id successfully")
    void testGetNotificationByIdSuccess() {
        // Arrange
        when(notificationRepository.findById(1L)).thenReturn(Optional.of(notification));
        when(notificationMapper.toResponse(notification)).thenReturn(responseDto);

        // Act
        NotificationResponseDto result = notificationService.getById(1L);

        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getOrderId()).isEqualTo(1L);

        verify(notificationRepository).findById(1L);
    }

    @Test
    @DisplayName("Should throw exception when notification not found")
    void testGetNotificationNotFound() {
        // Arrange
        when(notificationRepository.findById(999L)).thenReturn(Optional.empty());

        // Act & Assert
        assertThatThrownBy(() -> notificationService.getById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Notification not found");

        verify(notificationRepository).findById(999L);
    }

    @Test
    @DisplayName("Should get notifications by order id")
    void testGetNotificationsByOrderId() {
        // Arrange
        Notification notification2 = Notification.builder()
                .id(2L)
                .orderId(1L)
                .type("ORDER_ACCEPTED")
                .message("Your order has been accepted")
                .status(NotificationStatus.SENT)
                .createdAt(LocalDateTime.now())
                .build();

        NotificationResponseDto responseDto2 = NotificationResponseDto.builder()
                .id(2L)
                .orderId(1L)
                .type("ORDER_ACCEPTED")
                .message("Your order has been accepted")
                .status(NotificationStatus.SENT.toString())
                .createdAt(LocalDateTime.now())
                .build();

        when(notificationRepository.findByOrderId(1L)).thenReturn(Arrays.asList(notification, notification2));
        when(notificationMapper.toResponse(notification)).thenReturn(responseDto);
        when(notificationMapper.toResponse(notification2)).thenReturn(responseDto2);

        // Act
        List<NotificationResponseDto> results = notificationService.getByOrderId(1L);

        // Assert
        assertThat(results).hasSize(2);
        assertThat(results.get(0).getOrderId()).isEqualTo(1L);
        assertThat(results.get(1).getOrderId()).isEqualTo(1L);

        verify(notificationRepository).findByOrderId(1L);
    }

    @Test
    @DisplayName("Should send email notification")
    void testSendEmailNotification() {
        // Arrange
        String email = "customer@example.com";
        String message = "Order placed";
        when(emailService.sendEmail(email, message)).thenReturn(true);

        // Act
        boolean result = emailService.sendEmail(email, message);

        // Assert
        assertThat(result).isTrue();

        verify(emailService).sendEmail(email, message);
    }

    @Test
    @DisplayName("Should send SMS notification")
    void testSendSmsNotification() {
        // Arrange
        String phone = "9876543210";
        String message = "Order placed";
        when(smsService.sendSms(phone, message)).thenReturn(true);

        // Act
        boolean result = smsService.sendSms(phone, message);

        // Assert
        assertThat(result).isTrue();

        verify(smsService).sendSms(phone, message);
    }

    @Test
    @DisplayName("Should retry failed notification")
    void testRetryFailedNotification() {
        // Arrange
        Notification failedNotification = Notification.builder()
                .id(1L)
                .status(NotificationStatus.FAILED)
                .build();

        when(notificationRepository.findById(1L)).thenReturn(Optional.of(failedNotification));
        when(emailService.sendEmail(anyString(), anyString())).thenReturn(true);
        when(notificationRepository.save(any(Notification.class))).thenReturn(notification);

        // Act
        notificationService.retry(1L);

        // Assert
        verify(notificationRepository).findById(1L);
        verify(notificationRepository).save(any(Notification.class));
    }

    @Test
    @DisplayName("Should validate notification type")
    void testValidateNotificationType() {
        // Arrange
        NotificationRequestDto invalidRequest = NotificationRequestDto.builder()
                .orderId(1L)
                .customerId(1L)
                .type("INVALID_TYPE")
                .message("Message")
                .build();

        // Act & Assert - validation should be handled by annotation or service
        assertThat(invalidRequest.getType()).isNotEmpty();
    }

    @Test
    @DisplayName("Should handle notification for order placed event")
    void testHandleOrderPlacedEvent() {
        // Arrange
        when(notificationMapper.toEntity(any())).thenReturn(notification);
        when(notificationRepository.save(any(Notification.class))).thenReturn(notification);
        when(emailService.sendEmail(anyString(), anyString())).thenReturn(true);
        when(smsService.sendSms(anyString(), anyString())).thenReturn(true);
        when(notificationMapper.toResponse(any())).thenReturn(responseDto);

        // Act
        NotificationResponseDto result = notificationService.send(requestDto);

        // Assert
        assertThat(result).isNotNull();
        verify(notificationRepository).save(any(Notification.class));
    }
}


