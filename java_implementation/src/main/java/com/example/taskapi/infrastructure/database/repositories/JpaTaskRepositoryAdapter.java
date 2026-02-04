package com.example.taskapi.infrastructure.database.repositories;

import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class JpaTaskRepositoryAdapter implements TaskRepositoryPort {

    private final SpringDataTaskRepository repository;

    @Override
    public Task create(Task task) {
        return repository.save(task);
    }

    @Override
    public Optional<Task> getById(UUID taskId) {
        return repository.findById(taskId);
    }

    @Override
    public List<Task> getAll(int skip, int limit, TaskStatus status) {
        int page = skip / limit;
        PageRequest pageRequest = PageRequest.of(page, limit, Sort.by(Sort.Direction.DESC, "createdAt"));
        
        if (status != null) {
            return repository.findByStatus(status, pageRequest);
        }
        return repository.findAll(pageRequest).getContent();
    }

    @Override
    public long count(TaskStatus status) {
        if (status != null) {
            return repository.countByStatus(status);
        }
        return repository.count();
    }

    @Override
    public Task update(Task task) {
        return repository.save(task);
    }

    @Override
    public boolean delete(UUID taskId) {
        if (repository.existsById(taskId)) {
            repository.deleteById(taskId);
            return true;
        }
        return false;
    }
}
