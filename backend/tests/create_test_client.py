from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
client.base_url = str(client.base_url) + '/api'
