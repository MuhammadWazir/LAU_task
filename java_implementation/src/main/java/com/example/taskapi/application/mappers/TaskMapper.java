package com.example.taskapi.application.mappers;

import com.example.taskapi.application.dtos.TaskResponse;
import com.example.taskapi.domain.model.Task;

public class TaskMapper {
    public static TaskResponse toResponse(Task task) {
        if (task == null) return null;
        return TaskResponse.builder()
                .taskId(task.getTaskId())
                .title(task.getTitle())
                .status(task.getStatus())
                .createdAt(task.getCreatedAt())
                .updatedAt(task.getUpdatedAt())
                .build();
    }
}
