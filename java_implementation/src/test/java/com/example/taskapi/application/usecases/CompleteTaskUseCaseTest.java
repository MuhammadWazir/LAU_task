package com.example.taskapi.application.usecases;

import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import com.example.taskapi.domain.repository.TaskRepositoryPort;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class CompleteTaskUseCaseTest {

    @Mock
    private TaskRepositoryPort taskRepository;

    @InjectMocks
    private CompleteTaskUseCase completeTaskUseCase;

    @Test
    void testExecute_Success() {
        UUID taskId = UUID.randomUUID();
        Task task = Task.builder()
                .taskId(taskId)
                .status(TaskStatus.OPEN)
                .build();

        when(taskRepository.getById(taskId)).thenReturn(Optional.of(task));
        when(taskRepository.update(any(Task.class))).thenAnswer(i -> i.getArguments()[0]);

        Optional<Task> result = completeTaskUseCase.execute(taskId);

        assertThat(result).isPresent();
        assertThat(result.get().getStatus()).isEqualTo(TaskStatus.DONE);
        verify(taskRepository).update(task);
    }

    @Test
    void testExecute_TaskAlreadyDone() {
        UUID taskId = UUID.randomUUID();
        Task task = Task.builder()
                .taskId(taskId)
                .status(TaskStatus.DONE)
                .build();

        when(taskRepository.getById(taskId)).thenReturn(Optional.of(task));

        Optional<Task> result = completeTaskUseCase.execute(taskId);

        assertThat(result).isPresent();
        assertThat(result.get().getStatus()).isEqualTo(TaskStatus.DONE);
        verify(taskRepository, never()).update(any());
    }

    @Test
    void testExecute_NotFound() {
        UUID taskId = UUID.randomUUID();
        when(taskRepository.getById(taskId)).thenReturn(Optional.empty());

        Optional<Task> result = completeTaskUseCase.execute(taskId);

        assertThat(result).isEmpty();
    }
}
