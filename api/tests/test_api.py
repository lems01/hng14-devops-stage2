from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import main

client = TestClient(main.app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200


def test_create_job(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(main, "r", mock_redis)

    res = client.post("/jobs")

    assert res.status_code == 200
    assert "job_id" in res.json()
    mock_redis.lpush.assert_called()
    mock_redis.hset.assert_called()


def test_get_job_not_found(monkeypatch):
    mock_redis = MagicMock()
    mock_redis.hget.return_value = None

    monkeypatch.setattr(main, "r", mock_redis)

    res = client.get("/jobs/123")

    assert res.status_code == 404