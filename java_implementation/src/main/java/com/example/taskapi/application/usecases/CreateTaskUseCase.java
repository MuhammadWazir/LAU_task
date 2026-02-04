package com.example.taskapi.application.usecases;

import com.example.taskapi.application.dtos.CreateTaskRequest;
import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CreateTaskUseCase {
    private final TaskRepositoryPort taskRepository;

    public Task execute(CreateTaskRequest request) {
        Task task = Task.builder()
                .title(request.getTitle())
                .status(TaskStatus.OPEN)
                .build();
        return taskRepository.create(task);
    }
}
