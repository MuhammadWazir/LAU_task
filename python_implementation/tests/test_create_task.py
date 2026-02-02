import pytest
from fastapi import status


class TestCreateTask:
    """Test suite for POST /tasks endpoint"""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test creating a task with valid data returns 201 and task object"""
        response = client.post("/tasks", json=sample_task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["status"] == "OPEN"
        assert "task_id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_task_empty_title(self, client):
        """Test creating a task with empty title returns 422"""
        response = client.post("/tasks", json={"title": ""})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_whitespace_only_title(self, client):
        """Test creating a task with whitespace-only title returns 422"""
        response = client.post("/tasks", json={"title": "   "})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_missing_title(self, client):
        """Test creating a task without title returns 422"""
        response = client.post("/tasks", json={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_title_too_long(self, client):
        """Test creating a task with title exceeding 255 characters returns 422"""
        long_title = "a" * 256
        response = client.post("/tasks", json={"title": long_title})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_trims_whitespace(self, client):
        """Test that leading/trailing whitespace is trimmed from title"""
        response = client.post("/tasks", json={"title": "  Test Task  "})
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Test Task"
