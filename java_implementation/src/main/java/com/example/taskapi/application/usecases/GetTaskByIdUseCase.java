package com.example.taskapi.application.usecases;

import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class GetTaskByIdUseCase {
    private final TaskRepositoryPort taskRepository;

    public Optional<Task> execute(UUID taskId) {
        return taskRepository.getById(taskId);
    }
}
