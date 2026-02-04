package com.example.taskapi.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI taskApiOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Task API")
                        .description("A RESTful API for managing tasks.")
                        .version("0.1.0"));
    }
}
