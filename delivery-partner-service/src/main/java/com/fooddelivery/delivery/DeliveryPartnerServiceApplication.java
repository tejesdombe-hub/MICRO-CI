package com.fooddelivery.delivery;

import com.fooddelivery.common.messaging.config.RabbitMQConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.context.annotation.Import;

@SpringBootApplication(scanBasePackages = "com.fooddelivery")
@EnableDiscoveryClient
@Import(RabbitMQConfig.class)
public class DeliveryPartnerServiceApplication {
    public static void main(String[] args) { SpringApplication.run(DeliveryPartnerServiceApplication.class, args); }
}
