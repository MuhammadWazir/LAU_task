package com.example.taskapi.api;

import com.example.taskapi.application.dtos.CreateTaskRequest;
import com.example.taskapi.application.dtos.TaskListResponse;
import com.example.taskapi.application.dtos.TaskResponse;
import com.example.taskapi.application.mappers.TaskMapper;
import com.example.taskapi.application.usecases.*;
import com.example.taskapi.config.Constants;
import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/tasks")
@RequiredArgsConstructor
@Tag(name = "tasks", description = "Operations related to tasks")
public class TaskController {

    private final CreateTaskUseCase createTaskUseCase;
    private final GetTaskByIdUseCase getTaskByIdUseCase;
    private final ListTasksUseCase listTasksUseCase;
    private final CompleteTaskUseCase completeTaskUseCase;
    private final DeleteTaskUseCase deleteTaskUseCase;
    private final RedisTemplate<String, Object> redisTemplate;

    @Operation(summary = "Create a new task", description = "Creates a new task with status OPEN")
    @ApiResponse(responseCode = "201", description = "Task created successfully")
    @PostMapping
    public ResponseEntity<TaskResponse> create(@Valid @RequestBody CreateTaskRequest request) {
        try {
            Task task = createTaskUseCase.execute(request);
            invalidateCache();
            return ResponseEntity.status(HttpStatus.CREATED).body(TaskMapper.toResponse(task));
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Failed to create task: " + e.getMessage());
        }
    }

    @Operation(summary = "List tasks", description = "List tasks with optional filtering and pagination")
    @GetMapping
    public TaskListResponse list(
            @RequestParam(required = false) TaskStatus status,
            @RequestParam(defaultValue = "50") Integer limit,
            @RequestParam(defaultValue = "0") Integer offset
    ) {
        if (limit > Constants.LIMIT_CAP || limit < 1 || offset < 0) {
            throw new ResponseStatusException(HttpStatus.UNPROCESSABLE_ENTITY, "Invalid pagination parameters");
        }

        String cacheKey = String.format("tasks:list:status=%s:limit=%d:offset=%d", status, limit, offset);
        TaskListResponse cached = (TaskListResponse) redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            return cached;
        }

        ListTasksUseCase.ListTasksResult result = listTasksUseCase.execute(status, limit, offset);
        TaskListResponse response = TaskListResponse.builder()
                .tasks(result.getTasks().stream().map(TaskMapper::toResponse).collect(Collectors.toList()))
                .total(result.getTotal())
                .limit(limit)
                .offset(offset)
                .build();

        redisTemplate.opsForValue().set(cacheKey, response, 10, TimeUnit.SECONDS);
        return response;
    }

    @Operation(summary = "Get task by ID", description = "Retrieve a specific task by its ID")
    @GetMapping("/{taskId}")
    public TaskResponse get(@PathVariable UUID taskId) {
        Task task = getTaskByIdUseCase.execute(taskId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Task with id " + taskId + " not found"));
        return TaskMapper.toResponse(task);
    }

    @Operation(summary = "Mark task as complete", description = "Mark a task as DONE (idempotent)")
    @PatchMapping("/{taskId}/complete")
    public TaskResponse complete(@PathVariable UUID taskId) {
        Task task = completeTaskUseCase.execute(taskId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Task with id " + taskId + " not found"));
        invalidateCache();
        return TaskMapper.toResponse(task);
    }

    @Operation(summary = "Delete task", description = "Delete a task by ID")
    @DeleteMapping("/{taskId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable UUID taskId) {
        boolean success = deleteTaskUseCase.execute(taskId);
        if (!success) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Task with id " + taskId + " not found");
        }
        invalidateCache();
    }

    private void invalidateCache() {
        Set<String> keys = redisTemplate.keys("tasks:*");
        if (keys != null && !keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }
}
