from .conftest import read_all_notes


def test_list_empty(client):
    response = client.get("/notes")
    assert response.status_code == 200
    assert response.json() == []


def test_list(client, db):
    client.post("/notes", json={"text": "test1"})
    client.post("/notes", json={"text": "test2"})
    client.post("/notes", json={"text": "test3"})

    notes = {n.text: n.id for n in read_all_notes(db)}
    assert len(notes) == 3

    response = client.get("/notes")

    res = set([(n["text"], n["id"]) for n in response.json()])
    assert res == set([(k, v) for k, v in notes.items()])

    response = client.get("/notes?limit=1")
    res = set([(n["text"], n["id"]) for n in response.json()])
    assert res == {("test1", notes["test1"])}

    response = client.get("/notes?limit=1&offset=1")
    res = set([(n["text"], n["id"]) for n in response.json()])
    assert res == {("test2", notes["test2"])}

    response = client.get("/notes?limit=1&offset=100")
    assert response.json() == []
