from .conftest import read_all_notes


def test_delete_note(client, db):
    response = client.post("/notes", json={"text": "test1"})
    assert response.status_code == 201
    assert len(read_all_notes(db)) == 1
    _id = response.json()["id"]

    response = client.delete(f"/notes/{_id}")
    assert response.status_code == 200

    assert len(read_all_notes(db)) == 0


def test_modify_note_not_found(client):
    response = client.delete(f"/notes/{999}")
    assert response.status_code == 404


def test_modify_note_validation_error(client, db):
    response = client.post("/notes", json={"text": "test1"})
    assert response.status_code == 201
    assert len(read_all_notes(db)) == 1
    _id = response.json()["id"]

    response = client.put(f"/notes/{_id}", json={"abc": "test2"})
    assert response.status_code == 422
