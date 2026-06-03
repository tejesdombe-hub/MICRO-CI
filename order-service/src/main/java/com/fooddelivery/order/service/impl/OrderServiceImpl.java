package com.fooddelivery.order.service.impl;

import com.fooddelivery.common.enums.OrderStatus;
import com.fooddelivery.common.exception.InvalidRequestException;
import com.fooddelivery.common.exception.ResourceNotFoundException;
import com.fooddelivery.common.messaging.event.OrderEvent;
import com.fooddelivery.common.messaging.producer.MessageProducer;
import com.fooddelivery.order.client.*;
import com.fooddelivery.order.client.dto.*;
import com.fooddelivery.order.dto.OrderRequestDto;
import com.fooddelivery.order.dto.OrderResponseDto;
import com.fooddelivery.order.dto.OrderStatusUpdateRequestDto;
import com.fooddelivery.order.entity.Order;
import com.fooddelivery.order.mapper.OrderMapper;
import com.fooddelivery.order.repository.OrderRepository;
import com.fooddelivery.order.service.OrderService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

@Service
public class OrderServiceImpl implements OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderServiceImpl.class);

    private final OrderRepository orderRepository;
    private final OrderMapper orderMapper;
    private final CustomerClient customerClient;
    private final RestaurantClient restaurantClient;
    private final PaymentClient paymentClient;
    private final NotificationClient notificationClient;
    private final DeliveryPartnerClient deliveryPartnerClient;
    private final MessageProducer messageProducer;

    public OrderServiceImpl(
            OrderRepository orderRepository,
            OrderMapper orderMapper,
            CustomerClient customerClient,
            RestaurantClient restaurantClient,
            PaymentClient paymentClient,
            NotificationClient notificationClient,
            DeliveryPartnerClient deliveryPartnerClient,
            MessageProducer messageProducer) {
        this.orderRepository = orderRepository;
        this.orderMapper = orderMapper;
        this.customerClient = customerClient;
        this.restaurantClient = restaurantClient;
        this.paymentClient = paymentClient;
        this.notificationClient = notificationClient;
        this.deliveryPartnerClient = deliveryPartnerClient;
        this.messageProducer = messageProducer;
    }

    @Override
    @Transactional
    public OrderResponseDto placeOrder(OrderRequestDto request) {
        customerClient.getCustomer(request.getCustomerId());
        restaurantClient.getRestaurant(request.getRestaurantId());

        Order order = Order.builder()
                .customerId(request.getCustomerId())
                .restaurantId(request.getRestaurantId())
                .totalAmount(request.getTotalAmount())
                .orderStatus(OrderStatus.PLACED)
                .build();
        order = orderRepository.save(order);
        log.info("Order placed with id={}", order.getId());

        // Send ORDER_PLACED event
        OrderEvent orderPlacedEvent = OrderEvent.createOrderPlacedEvent(
                order.getId(),
                order.getCustomerId(),
                order.getRestaurantId(),
                BigDecimal.valueOf(order.getTotalAmount())
        );
        messageProducer.sendOrderEvent(orderPlacedEvent);

        PaymentRequestDto paymentRequest = new PaymentRequestDto();
        paymentRequest.setOrderId(order.getId());
        paymentRequest.setAmount(order.getTotalAmount());
        paymentRequest.setPaymentMethod(request.getPaymentMethod() != null ? request.getPaymentMethod() : "UPI");
        paymentClient.processPayment(paymentRequest);

        order.setOrderStatus(OrderStatus.CONFIRMED);
        order = orderRepository.save(order);

        // Send ORDER_CONFIRMED event
        OrderEvent orderConfirmedEvent = OrderEvent.createOrderConfirmedEvent(
                order.getId(),
                order.getCustomerId(),
                order.getRestaurantId(),
                BigDecimal.valueOf(order.getTotalAmount())
        );
        messageProducer.sendOrderEvent(orderConfirmedEvent);

        sendNotification(order.getCustomerId(), "Order #" + order.getId() + " placed successfully", "ORDER_PLACED");
        sendNotification(order.getCustomerId(), "Order #" + order.getId() + " accepted by restaurant", "ORDER_ACCEPTED");

        return orderMapper.toResponse(order);
    }

    @Override
    public OrderResponseDto getById(Long id) {
        return orderMapper.toResponse(findOrder(id));
    }

    @Override
    public List<OrderResponseDto> getByCustomerId(Long customerId) {
        return orderRepository.findByCustomerId(customerId).stream()
                .map(orderMapper::toResponse)
                .toList();
    }

    @Override
    @Transactional
    public OrderResponseDto updateStatus(Long id, OrderStatusUpdateRequestDto request) {
        Order order = findOrder(id);
        order.setOrderStatus(request.getOrderStatus());
        order = orderRepository.save(order);

        if (request.getOrderStatus() == OrderStatus.DELIVERED) {
            // Send ORDER_DELIVERED event
            OrderEvent orderDeliveredEvent = OrderEvent.createOrderDeliveredEvent(
                    order.getId(),
                    order.getCustomerId(),
                    order.getDeliveryPartnerId()
            );
            messageProducer.sendOrderEvent(orderDeliveredEvent);

            sendNotification(order.getCustomerId(), "Order #" + order.getId() + " delivered", "ORDER_DELIVERED");
        }
        return orderMapper.toResponse(order);
    }

    @Override
    @Transactional
    public OrderResponseDto assignDelivery(Long id) {
        Order order = findOrder(id);
        if (order.getOrderStatus() != OrderStatus.CONFIRMED && order.getOrderStatus() != OrderStatus.READY) {
            throw new InvalidRequestException("Order must be CONFIRMED or READY for delivery assignment");
        }

        DeliveryAssignmentRequestDto assignment = new DeliveryAssignmentRequestDto();
        assignment.setOrderId(order.getId());
        DeliveryPartnerResponseDto partner = deliveryPartnerClient.assignPartner(assignment);

        order.setDeliveryPartnerId(partner.getId());
        order.setOrderStatus(OrderStatus.OUT_FOR_DELIVERY);
        order = orderRepository.save(order);

        // Send DELIVERY_ASSIGNED event
        OrderEvent deliveryAssignmentEvent = OrderEvent.createDeliveryAssignmentEvent(
                order.getId(),
                partner.getId()
        );
        messageProducer.sendOrderEvent(deliveryAssignmentEvent);

        return orderMapper.toResponse(order);
    }

    private Order findOrder(Long id) {
        return orderRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Order not found: " + id));
    }

    @org.springframework.scheduling.annotation.Async("taskExecutor")
    private void sendNotification(Long userId, String message, String type) {
        log.info("Sending async notification to user {} on thread: {}", userId, Thread.currentThread().getName());
        try {
            NotificationRequestDto notification = new NotificationRequestDto();
            notification.setUserId(userId);
            notification.setMessage(message);
            notification.setType(type);
            notificationClient.sendNotification(notification);
            log.info("Async notification sent successfully to user {}", userId);
        } catch (Exception e) {
            log.error("Failed to send async notification to user {}", userId, e);
        }
    }
}
