package com.fooddelivery.restaurant.config;

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
                        .title("Restaurant Service API")
                        .version("1.0")
                        .description("Restaurant management. Called by Order Service via Feign to validate restaurantId."))
                .servers(OpenApiServers.forService(8083));
    }
}
