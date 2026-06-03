package com.fooddelivery.payment.config;

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
                        .title("Payment Service API")
                        .version("1.0")
                        .description("Simulated payment. Called by Order Service via Feign when order is placed."))
                .servers(OpenApiServers.forService(8087));
    }
}
