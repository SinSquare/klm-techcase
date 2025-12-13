def test_read_note(client):
    response = client.post("/notes", json={"text": "test1"})
    assert response.status_code == 201
    _id = response.json()["id"]

    response = client.get(f"/notes/{_id}")
    assert response.status_code == 200
    assert response.json() == {"id": _id, "text": "test1"}

    response = client.get(f"/notes/{_id + 1}")
    assert response.status_code == 404
