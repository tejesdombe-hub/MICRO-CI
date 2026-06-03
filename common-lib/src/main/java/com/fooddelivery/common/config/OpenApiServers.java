package com.fooddelivery.common.config;

import io.swagger.v3.oas.models.servers.Server;

import java.util.List;

public final class OpenApiServers {

    private OpenApiServers() {
    }

    /**
     * @param directPort service port (e.g. 8082 for customer-service)
     */
    public static List<Server> forService(int directPort) {
        return List.of(
                new Server()
                        .url("http://localhost:8080/api")
                        .description("API Gateway (use this in Swagger Try it out)"),
                new Server()
                        .url("http://localhost:" + directPort)
                        .description("Direct service (Docker/local)")
        );
    }
}
