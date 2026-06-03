package com.fooddelivery.order.config;

import com.fooddelivery.common.config.OpenApiServers;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Order Service API")
                        .version("1.0")
                        .description("""
                                Order orchestration hub. **Inter-service communication (Feign):**
                                - GET customer-service (validate customer)
                                - GET restaurant-service (validate restaurant)
                                - POST payment-service (process payment)
                                - POST notification-service (ORDER_PLACED, ORDER_ACCEPTED)
                                - POST delivery-partner-service (on assign-delivery)
                                Test POST /orders and check logs of other services."""))
                .servers(OpenApiServers.forService(8085));
    }
}
