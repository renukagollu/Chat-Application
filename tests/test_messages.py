from fastapi.testclient import TestClient
from app.main import create_app


def test_join_and_send_and_list_messages():
    client = TestClient(create_app())

    g = client.post("/groups", json={"name": "team"})
    gid = g.json()["id"]

    # join
    j = client.post(f"/groups/{gid}/join", headers={"X-User": "renukagollu"})
    assert j.status_code == 200

    # send
    s = client.post(
        f"/groups/{gid}/messages",
        headers={"X-User": "renukagollu"},
        json={"content": "Hello!"},
    )
    assert s.status_code == 201

    # list
    m = client.get(f"/groups/{gid}/messages")
    assert m.status_code == 200
    assert len(m.json()["data"]) >= 1