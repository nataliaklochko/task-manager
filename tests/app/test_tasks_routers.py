def test_create_task(client, user_id):
    print(user_id)
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "desc", "user_id": user_id},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "created"


def test_get_task(client, user_id, task_id):
    response = client.get(f"/tasks?task_id={task_id}&user_id={user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "created"


def test_get_task_not_found(client):
    _id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks?task_id={_id}&user_id={_id}")
    assert response.status_code == 404


def test_list_tasks(client, user_id):
    response = client.get(f"/tasks/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_list_tasks_empty(client):
    _id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_update_task(client, task_id, user_id):
    response = client.put(
        f"/tasks?task_id={task_id}&user_id={user_id}", json={"status": "in_progress"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "in_progress"


def test_delete_task(client, task_id, user_id):
    response = client.delete(f"/tasks?task_id={task_id}&user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}

    response = client.get(f"/tasks?task_id={task_id}&user_id={user_id}")
    assert response.status_code == 404
