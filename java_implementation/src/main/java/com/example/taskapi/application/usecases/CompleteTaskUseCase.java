package com.example.taskapi.application.usecases;

import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class CompleteTaskUseCase {
    private final TaskRepositoryPort taskRepository;

    public Optional<Task> execute(UUID taskId) {
        Optional<Task> taskOptional = taskRepository.getById(taskId);
        if (taskOptional.isEmpty()) {
            return Optional.empty();
        }

        Task task = taskOptional.get();
        if (task.getStatus() == TaskStatus.DONE) {
            return Optional.of(task);
        }

        task.setStatus(TaskStatus.DONE);
        return Optional.of(taskRepository.update(task));
    }
}
