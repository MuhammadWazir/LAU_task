import pytest
from fastapi import status


class TestDeleteTask:
    """Test suite for DELETE /tasks/{id} endpoint"""
    
    def test_delete_task_success(self, client, create_sample_task):
        """Test deleting an existing task returns 204"""
        task = create_sample_task("Task to Delete")
        
        response = client.delete(f"/tasks/{task['task_id']}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        get_response = client.get(f"/tasks/{task['task_id']}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task returns 404"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/tasks/{fake_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
    
    def test_delete_task_removes_from_list(self, client, create_sample_task):
        """Test that deleted task doesn't appear in list"""
        task1 = create_sample_task("Task 1")
        task2 = create_sample_task("Task 2")
        
        client.delete(f"/tasks/{task1['task_id']}")
        
        response = client.get("/tasks")
        data = response.json()
        
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["task_id"] == task2["task_id"]
