package com.fooddelivery.notification.service;

public interface SmsService {
    void sendSms(String phoneNumber, String message);
    void sendOrderConfirmationSms(String phoneNumber, String customerName, Long orderId);
    void sendOrderDeliveredSms(String phoneNumber, String customerName, Long orderId);
}
