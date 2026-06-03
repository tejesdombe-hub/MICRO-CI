package com.fooddelivery.notification.service;

public interface EmailService {
    void sendEmail(String to, String subject, String body);
    void sendOrderConfirmationEmail(String to, String customerName, Long orderId, Double amount);
    void sendOrderDeliveredEmail(String to, String customerName, Long orderId);
}
