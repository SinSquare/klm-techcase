from .conftest import read_all_notes


def test_modify_note(client, db):
    response = client.post("/notes", json={"text": "test1"})
    assert response.status_code == 201
    _id = response.json()["id"]
    notes = read_all_notes(db)
    assert len(notes) == 1
    assert notes[0].text == "test1"

    response = client.put(f"/notes/{_id}", json={"text": "test2"})
    assert response.status_code == 200
    assert response.json() == {"id": _id, "text": "test2"}
    notes = read_all_notes(db)
    assert len(notes) == 1
    assert notes[0].text == "test2"


def test_modify_note_not_found(client):
    response = client.put("/notes/999", json={"text": "test2"})
    assert response.status_code == 404


def test_modify_note_validation_error(client):
    response = client.post("/notes", json={"text": "test1"})
    assert response.status_code == 201
    _id = response.json()["id"]

    response = client.put(f"/notes/{_id}", json={"abc": "test2"})
    assert response.status_code == 422
