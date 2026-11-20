"""
测试：运行 pytest -q，看到 passed 就说明骨架没问题。

TestClient 可以在不启动服务器的情况下直接调用接口，测试时很方便。
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_categories():
    cats = client.get("/api/categories").json()
    assert "水电" in cats and "其他" in cats
