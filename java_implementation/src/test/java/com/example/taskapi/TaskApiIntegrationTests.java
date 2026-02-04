package com.example.taskapi;

import com.example.taskapi.application.dtos.CreateTaskRequest;
import com.example.taskapi.application.dtos.TaskListResponse;
import com.example.taskapi.application.dtos.TaskResponse;
import com.example.taskapi.domain.enums.TaskStatus;
import com.example.taskapi.infrastructure.database.repositories.SpringDataTaskRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.Objects;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
public class TaskApiIntegrationTests {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine").withExposedPorts(6379);

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
    }

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private SpringDataTaskRepository repository;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @BeforeEach
    void setup() {
        repository.deleteAll();
        Set<String> keys = redisTemplate.keys("tasks:*");
        if (keys != null && !keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }

    @Test
    void testListTasksEmpty() throws Exception {
        mockMvc.perform(get("/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tasks").isEmpty())
                .andExpect(jsonPath("$.total").value(0))
                .andExpect(jsonPath("$.limit").value(50))
                .andExpect(jsonPath("$.offset").value(0));
    }

    @Test
    void testCreateTask() throws Exception {
        CreateTaskRequest request = new CreateTaskRequest("Test Task");
        mockMvc.perform(post("/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title").value("Test Task"))
                .andExpect(jsonPath("$.status").value("OPEN"))
                .andExpect(jsonPath("$.taskId").exists());
    }

    @Test
    void testListTasksWithData() throws Exception {
        createTask("Task 1");
        createTask("Task 2");
        createTask("Task 3");

        mockMvc.perform(get("/tasks"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tasks.length()").value(3))
                .andExpect(jsonPath("$.total").value(3));
    }

    @Test
    void testFilterByStatus() throws Exception {
        TaskResponse task1 = createTask("Task 1");
        TaskResponse task2 = createTask("Task 2");

        mockMvc.perform(patch("/tasks/" + task1.getTaskId() + "/complete"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/tasks?status=OPEN"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tasks.length()").value(1))
                .andExpect(jsonPath("$.tasks[0].title").value("Task 2"));

        mockMvc.perform(get("/tasks?status=DONE"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tasks.length()").value(1))
                .andExpect(jsonPath("$.tasks[0].title").value("Task 1"));
    }

    @Test
    void testGetTaskById() throws Exception {
        TaskResponse created = createTask("Find Me");
        mockMvc.perform(get("/tasks/" + created.getTaskId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Find Me"));
    }

    @Test
    void testDeleteTask() throws Exception {
        TaskResponse created = createTask("Delete Me");
        mockMvc.perform(delete("/tasks/" + created.getTaskId()))
                .andExpect(status().isNoContent());

        mockMvc.perform(get("/tasks/" + created.getTaskId()))
                .andExpect(status().isNotFound());
    }

    private TaskResponse createTask(String title) throws Exception {
        String content = mockMvc.perform(post("/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(new CreateTaskRequest(title))))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();
        return objectMapper.readValue(content, TaskResponse.class);
    }
}
