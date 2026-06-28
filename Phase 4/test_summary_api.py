import requests
from jsonschema import validate

def test_summary_success(base_url):
    response = requests.get(f"{base_url}/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"

    schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "data"]
    }
    validate(instance=body, schema=schema)

def test_summary_invalid_method(base_url):
    response = requests.post(f"{base_url}/summary")
    assert response.status_code in [400, 405]
