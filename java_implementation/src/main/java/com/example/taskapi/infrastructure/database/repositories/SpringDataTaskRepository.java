package com.example.taskapi.infrastructure.database.repositories;

import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.domain.model.Task;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface SpringDataTaskRepository extends JpaRepository<Task, UUID> {
    List<Task> findByStatus(TaskStatus status, Pageable pageable);
    long countByStatus(TaskStatus status);
}
