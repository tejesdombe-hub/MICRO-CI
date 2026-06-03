package com.fooddelivery.notification.service.impl;

import com.fooddelivery.notification.service.SmsService;
import com.twilio.Twilio;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class SmsServiceImpl implements SmsService {

    @Value("${twilio.account.sid}")
    private String accountSid;

    @Value("${twilio.auth.token}")
    private String authToken;

    @Value("${twilio.phone.number}")
    private String fromPhoneNumber;

    @Value("${app.sms.enabled:true}")
    private boolean smsEnabled;

    @Override
    public void sendSms(String phoneNumber, String message) {
        if (!smsEnabled) {
            log.info("SMS sending is disabled. Would send SMS to: {} with message: {}", phoneNumber, message);
            return;
        }

        try {
            Twilio.init(accountSid, authToken);
            
            Message.creator(
                new PhoneNumber(phoneNumber),
                new PhoneNumber(fromPhoneNumber),
                message
            ).create();
            
            log.info("SMS sent successfully to: {} with message: {}", phoneNumber, message);
        } catch (Exception e) {
            log.error("Failed to send SMS to: {} with message: {}", phoneNumber, message, e);
            throw new RuntimeException("Failed to send SMS", e);
        }
    }

    @Override
    public void sendOrderConfirmationSms(String phoneNumber, String customerName, Long orderId) {
        String message = String.format(
            "Hi %s, your order #%d has been confirmed! Thank you for ordering with FoodDelivery.",
            customerName, orderId
        );
        sendSms(phoneNumber, message);
        log.info("Order confirmation SMS sent to: {} for order: {}", phoneNumber, orderId);
    }

    @Override
    public void sendOrderDeliveredSms(String phoneNumber, String customerName, Long orderId) {
        String message = String.format(
            "Hi %s, your order #%d has been delivered! Enjoy your meal. Thank you for choosing FoodDelivery.",
            customerName, orderId
        );
        sendSms(phoneNumber, message);
        log.info("Order delivered SMS sent to: {} for order: {}", phoneNumber, orderId);
    }
}
