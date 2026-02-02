import pytest
from fastapi import status


class TestGetTaskById:
    """Test suite for GET /tasks/{id} endpoint"""
    
    def test_get_task_success(self, client, create_sample_task):
        """Test getting an existing task returns 200 and task data"""
        task = create_sample_task("Test Task")
        
        response = client.get(f"/tasks/{task['task_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["task_id"] == task["task_id"]
        assert data["title"] == "Test Task"
        assert data["status"] == "OPEN"
    
    def test_get_task_not_found(self, client):
        """Test getting a non-existent task returns 404"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/tasks/{fake_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
