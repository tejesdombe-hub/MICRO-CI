package com.fooddelivery.menu.config;

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
                        .title("Menu Service API")
                        .version("1.0")
                        .description("Menu items per restaurant. Standalone service (no Feign from order)."))
                .servers(OpenApiServers.forService(8084));
    }
}
