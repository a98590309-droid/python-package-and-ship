from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_flow():
    # 1. Create item
    res = client.post("/items", json={"name": "Keyboard", "price": 49.99})
    assert res.status_code == 201

    # 2. Get items list
    res = client.get("/items")
    assert res.status_code == 200

    # 3. 404 test
    res = client.get("/items/999")
    assert res.status_code == 404
