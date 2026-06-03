package com.fooddelivery.notification.service.impl;

import com.fooddelivery.notification.service.EmailService;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmailServiceImpl implements EmailService {

    private final JavaMailSender mailSender;
    private final TemplateEngine templateEngine;

    @Value("${spring.mail.from:noreply@fooddelivery.com}")
    private String fromEmail;

    @Value("${app.email.enabled:true}")
    private boolean emailEnabled;

    @Override
    public void sendEmail(String to, String subject, String body) {
        if (!emailEnabled) {
            log.info("Email sending is disabled. Would send email to: {} with subject: {}", to, subject);
            return;
        }

        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            
            helper.setFrom(fromEmail);
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(body, true);
            
            mailSender.send(message);
            log.info("Email sent successfully to: {} with subject: {}", to, subject);
        } catch (Exception e) {
            log.error("Failed to send email to: {} with subject: {}", to, subject, e);
            throw new RuntimeException("Failed to send email", e);
        }
    }

    @Override
    public void sendOrderConfirmationEmail(String to, String customerName, Long orderId, Double amount) {
        try {
            Context context = new Context();
            context.setVariable("customerName", customerName);
            context.setVariable("orderId", orderId);
            context.setVariable("amount", amount);
            
            String htmlContent = templateEngine.process("email/order-confirmation", context);
            String subject = "Order Confirmation - Order #" + orderId;
            
            sendEmail(to, subject, htmlContent);
            log.info("Order confirmation email sent to: {} for order: {}", to, orderId);
        } catch (Exception e) {
            log.error("Failed to send order confirmation email to: {} for order: {}", to, orderId, e);
            throw new RuntimeException("Failed to send order confirmation email", e);
        }
    }

    @Override
    public void sendOrderDeliveredEmail(String to, String customerName, Long orderId) {
        try {
            Context context = new Context();
            context.setVariable("customerName", customerName);
            context.setVariable("orderId", orderId);
            
            String htmlContent = templateEngine.process("email/order-delivered", context);
            String subject = "Order Delivered - Order #" + orderId;
            
            sendEmail(to, subject, htmlContent);
            log.info("Order delivered email sent to: {} for order: {}", to, orderId);
        } catch (Exception e) {
            log.error("Failed to send order delivered email to: {} for order: {}", to, orderId, e);
            throw new RuntimeException("Failed to send order delivered email", e);
        }
    }
}
