import requests
from jsonschema import validate

def test_team_valid_id(base_url):
    response = requests.get(f"{base_url}/teams/10000")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "data": {"type": "object"}
            },
            "required": ["status", "data"]
        }
        validate(instance=data, schema=schema)

def test_team_invalid_id(base_url):
    response = requests.get(f"{base_url}/teams/xyz")
    assert response.status_code in [400, 404, 422]

def test_team_missing_id(base_url):
    response = requests.get(f"{base_url}/teams/")
    assert response.status_code in [400, 404]
