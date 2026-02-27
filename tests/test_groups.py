from fastapi.testclient import TestClient
from app.main import create_app


def test_create_group_and_list():
    client = TestClient(create_app())

    r = client.post("/groups", json={"name": "backend"})
    assert r.status_code == 201
    gid = r.json()["id"]

    r2 = client.get("/groups")
    assert r2.status_code == 200
    assert any(g["id"] == gid for g in r2.json()["data"])