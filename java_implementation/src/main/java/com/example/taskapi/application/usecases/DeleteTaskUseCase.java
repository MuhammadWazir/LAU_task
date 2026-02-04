package com.example.taskapi.application.usecases;

import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class DeleteTaskUseCase {
    private final TaskRepositoryPort taskRepository;

    public boolean execute(UUID taskId) {
        return taskRepository.delete(taskId);
    }
}
