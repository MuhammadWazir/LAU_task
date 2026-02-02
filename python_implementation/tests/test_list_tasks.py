import pytest
from fastapi import status


class TestListTasks:
    """Test suite for GET /tasks endpoint"""
    
    def test_list_tasks_empty(self, client):
        """Test listing tasks when database is empty"""
        response = client.get("/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0
        assert data["limit"] == 50
        assert data["offset"] == 0
    
    def test_list_tasks_with_data(self, client, create_sample_task):
        """Test listing tasks returns all tasks"""
        create_sample_task("Task 1")
        create_sample_task("Task 2")
        create_sample_task("Task 3")
        
        response = client.get("/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["tasks"]) == 3
        assert data["total"] == 3
    
    def test_list_tasks_ordered_by_created_at_desc(self, client, create_sample_task):
        """Test tasks are ordered by created_at descending"""
        task1 = create_sample_task("First Task")
        task2 = create_sample_task("Second Task")
        task3 = create_sample_task("Third Task")
        
        response = client.get("/tasks")
        data = response.json()
        
        assert data["tasks"][0]["task_id"] == task3["task_id"]
        assert data["tasks"][1]["task_id"] == task2["task_id"]
        assert data["tasks"][2]["task_id"] == task1["task_id"]
    
    def test_list_tasks_filter_by_status_open(self, client, create_sample_task):
        """Test filtering tasks by OPEN status"""
        task1 = create_sample_task("Open Task")
        task2 = create_sample_task("Another Open Task")
        
        client.patch(f"/tasks/{task2['task_id']}/complete")
        
        response = client.get("/tasks?status=OPEN")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["status"] == "OPEN"
        assert data["total"] == 1
    
    def test_list_tasks_filter_by_status_done(self, client, create_sample_task):
        """Test filtering tasks by DONE status"""
        task1 = create_sample_task("Task 1")
        task2 = create_sample_task("Task 2")
        
        client.patch(f"/tasks/{task1['task_id']}/complete")
        client.patch(f"/tasks/{task2['task_id']}/complete")
        
        response = client.get("/tasks?status=DONE")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(data["tasks"]) == 2
        assert all(task["status"] == "DONE" for task in data["tasks"])
        assert data["total"] == 2
    
    def test_list_tasks_pagination_limit(self, client, create_sample_task):
        """Test pagination with custom limit"""
        for i in range(5):
            create_sample_task(f"Task {i}")
        
        response = client.get("/tasks?limit=2")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(data["tasks"]) == 2
        assert data["limit"] == 2
        assert data["total"] == 5
    
    def test_list_tasks_pagination_offset(self, client, create_sample_task):
        """Test pagination with offset"""
        for i in range(5):
            create_sample_task(f"Task {i}")
        
        response = client.get("/tasks?limit=2&offset=2")
        data = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(data["tasks"]) == 2
        assert data["offset"] == 2
        assert data["total"] == 5
    
    def test_list_tasks_limit_defaults_to_50(self, client):
        """Test that limit defaults to 50"""
        response = client.get("/tasks")
        data = response.json()
        
        assert data["limit"] == 50
    
    def test_list_tasks_offset_defaults_to_0(self, client):
        """Test that offset defaults to 0"""
        response = client.get("/tasks")
        data = response.json()
        
        assert data["offset"] == 0
    
    def test_list_tasks_limit_capped_at_200(self, client, create_sample_task):
        """Test that limit greater than 200 returns 422"""
        create_sample_task("Task")
        
        response = client.get("/tasks?limit=500")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_list_tasks_negative_offset_rejected(self, client):
        """Test that negative offset returns 422"""
        response = client.get("/tasks?offset=-1")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_list_tasks_limit_less_than_1_rejected(self, client):
        """Test that limit less than 1 returns 422"""
        response = client.get("/tasks?limit=0")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
