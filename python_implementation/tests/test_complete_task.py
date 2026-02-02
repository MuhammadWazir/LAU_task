import pytest
from fastapi import status


class TestCompleteTask:
    """Test suite for PATCH /tasks/{id}/complete endpoint"""
    
    def test_complete_task_success(self, client, create_sample_task):
        """Test completing a task changes status to DONE"""
        task = create_sample_task("Task to Complete")
        
        response = client.patch(f"/tasks/{task['task_id']}/complete")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "DONE"
        assert data["task_id"] == task["task_id"]
    
    def test_complete_task_idempotent(self, client, create_sample_task):
        """Test completing an already completed task is idempotent"""
        task = create_sample_task("Task to Complete")
        
        response1 = client.patch(f"/tasks/{task['task_id']}/complete")
        assert response1.status_code == status.HTTP_200_OK
        
        response2 = client.patch(f"/tasks/{task['task_id']}/complete")
        assert response2.status_code == status.HTTP_200_OK
        
        data = response2.json()
        assert data["status"] == "DONE"
        assert data["task_id"] == task["task_id"]
    
    def test_complete_task_not_found(self, client):
        """Test completing a non-existent task returns 404"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.patch(f"/tasks/{fake_id}/complete")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
