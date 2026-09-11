"""
Integration and Unit Tests for Backend Architecture & Request Tokenization
==========================================================================
Verifies:
1. Application factory creates cleanly in testing mode
2. Request tokenization stamps every request with X-Request-Token
3. Audit log records events into JSONL
4. Page routes and API endpoints return correct status codes & schemas
"""

import os
import json
import pytest
from backend.app import create_app
from backend.config import TestingConfig


@pytest.fixture
def client(tmp_path):
    log_file = tmp_path / "test_request_log.jsonl"
    cfg = TestingConfig()
    cfg.REQUEST_LOG_PATH = str(log_file)
    app = create_app(cfg)
    with app.test_client() as client:
        yield client, log_file


def test_request_tokenization_header(client):
    test_client, log_file = client
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert "X-Request-Token" in response.headers
    token = response.headers["X-Request-Token"]
    assert token.startswith("REQ-")
    assert "X-Response-Time-Ms" in response.headers

    # Verify JSONL log record
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 1
        record = json.loads(lines[-1])
        assert record["token"] == token
        assert record["path"] == "/api/health"
        assert record["status"] == 200


def test_api_search_vsm(client):
    test_client, _ = client
    response = test_client.get("/api/search/vsm?q=cotton%20shirt&top_k=5")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["mode"] == "vsm"
    assert len(data["results"]) <= 5
    assert len(data["results"]) > 0
    assert "X-Request-Token" in response.headers


def test_api_search_positional(client):
    test_client, _ = client
    response = test_client.get("/api/search/positional?q=\"cotton%20shirt\"")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["mode"] == "positional"
    assert len(data["results"]) > 0


def test_api_trace(client):
    test_client, _ = client
    response = test_client.get("/api/trace?term1=stretch&term2=denim&k=4")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "trace_log" in data
    assert "matches" in data


def test_api_doc_details(client):
    test_client, _ = client
    response = test_client.get("/api/doc/D001")
    assert response.status_code == 200
    data = response.get_json()
    assert data["doc_id"] == "D001"
    assert "tokens" in data
    assert "term_frequencies" in data


def test_api_vocabulary(client):
    test_client, _ = client
    response = test_client.get("/api/vocabulary?search=cotton")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["items"]) > 0


def test_page_routes_render(client):
    test_client, _ = client
    for path in ["/", "/results", "/tracer", "/tests", "/vocabulary"]:
        res = test_client.get(path)
        assert res.status_code == 200
        assert "X-Request-Token" in res.headers
