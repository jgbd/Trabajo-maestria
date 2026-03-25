from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_users(client: TestClient):
    # Create a user first
    client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_user(client: TestClient):
    # Create a user
    create_response = client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_update_user(client: TestClient):
    # Create a user
    create_response = client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    user_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/users/{user_id}",
        json={"name": "Updated Name", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

def test_delete_user(client: TestClient):
    # Create a user
    create_response = client.post(
        "/api/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/api/users/{user_id}")
    # Note: The current implementation returns null/None for non-existent user in get_user, 
    # or it might return 200 with null body depending on implementation. 
    # Let's check the implementation of get_user again.
    # It returns `user` which is None if not found. FastAPI returns null JSON.
    assert get_response.json() is None

def test_delete_non_existent_user(client: TestClient):
    response = client.delete("/api/users/99999")
    assert response.status_code == 404
