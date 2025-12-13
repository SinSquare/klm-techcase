from .conftest import read_all_notes


def test_create_note(client, db):
    assert len(read_all_notes(db)) == 0
    response = client.post("/notes", json={"text": "test"})
    assert response.status_code == 201

    results = read_all_notes(db)
    assert len(results) == 1
    assert response.json() == {"id": results[0].id, "text": "test"}


def test_create_note_validation_error(client):
    response = client.post("/notes", json={"nofield": "test"})
    assert response.status_code == 422
