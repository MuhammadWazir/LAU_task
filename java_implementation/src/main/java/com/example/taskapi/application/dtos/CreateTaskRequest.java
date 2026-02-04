package com.example.taskapi.application.dtos;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateTaskRequest {
    @NotBlank(message = "Title cannot be empty or whitespace only")
    @Size(min = 1, max = 255, message = "Title must be between 1 and 255 characters")
    private String title;
}
