def test_create_user(client):
    response = client.post("/users/", json={"username": "Test username"})
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "Test username"


def test_get_user(client, user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "Test username"


def test_get_user_not_found(client):
    response = client.get("/users/10000000")
    assert response.status_code == 404


def test_list_users(client, user_id):
    response = client.get("/users/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
