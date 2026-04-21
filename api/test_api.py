import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

def test_create_job(monkeypatch):
    class MockRedis:
        def lpush(self, *args): pass
        def hset(self, *args): pass
    monkeypatch.setattr("main.r", MockRedis())

    res = client.post("/jobs")
    assert res.status_code == 200
    assert "job_id" in res.json()

def test_get_job_not_found(monkeypatch):
    class MockRedis:
        def hget(self, *args): return None
    monkeypatch.setattr("main.r", MockRedis())

    res = client.get("/jobs/123")
    assert res.status_code == 404
