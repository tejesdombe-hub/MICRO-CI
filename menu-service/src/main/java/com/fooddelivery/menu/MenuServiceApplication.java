package com.fooddelivery.menu;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication(scanBasePackages = "com.fooddelivery")
@EnableDiscoveryClient
public class MenuServiceApplication {
    public static void main(String[] args) { SpringApplication.run(MenuServiceApplication.class, args); }
}
