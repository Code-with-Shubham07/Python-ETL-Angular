import requests
from jsonschema import validate

def test_player_valid_id(base_url):
    response = requests.get(f"{base_url}/players/42664")
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

def test_player_invalid_id(base_url):
    response = requests.get(f"{base_url}/players/xyz")
    assert response.status_code in [400, 404, 422]
