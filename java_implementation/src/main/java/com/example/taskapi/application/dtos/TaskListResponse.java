package com.example.taskapi.application.dtos;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TaskListResponse implements Serializable {
    @JsonProperty("tasks")
    private List<TaskResponse> tasks;
    private long total;
    private int limit;
    private int offset;
}
