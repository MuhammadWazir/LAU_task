package com.example.taskapi.application.usecases;

import com.example.taskapi.config.Constants;
import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ListTasksUseCase {
    private final TaskRepositoryPort taskRepository;

    @Data
    @AllArgsConstructor
    public static class ListTasksResult {
        private List<Task> tasks;
        private long total;
    }

    public ListTasksResult execute(TaskStatus status, Integer limit, Integer offset) {
        if (limit == null) {
            limit = Constants.LIMIT_DEFAULT;
        }
        if (limit > Constants.LIMIT_CAP) {
            limit = Constants.LIMIT_CAP;
        }
        if (limit < 1) {
            limit = Constants.LIMIT_DEFAULT;
        }

        if (offset == null || offset < 0) {
            offset = Constants.OFFSET_DEFAULT;
        }

        List<Task> tasks = taskRepository.getAll(offset, limit, status);
        long total = taskRepository.count(status);

        return new ListTasksResult(tasks, total);
    }
}
