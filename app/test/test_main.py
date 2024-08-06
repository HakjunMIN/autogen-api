# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app, prefix, base

client = TestClient(app)

def test_docs_redirect():
    response = client.get(base)
    assert response.status_code == 200
    assert response.url.endswith("/docs")

def test_route_query():
    model_input = {"your": "input_data"}  # Replace with actual input data structure
    response = client.post(prefix + "/chat/completions", json=model_input)
    assert response.status_code == 200
    # Add more assertions based on the expected response