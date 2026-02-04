package com.example.taskapi.domain.repository;

import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface TaskRepositoryPort {
    Task create(Task task);
    Optional<Task> getById(UUID taskId);
    List<Task> getAll(int skip, int limit, TaskStatus status);
    long count(TaskStatus status);
    Task update(Task task);
    boolean delete(UUID taskId);
}
