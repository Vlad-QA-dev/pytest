import requests
import pytest

URL = "https://api.pokemonbattle.ru"
Token = "820739400fd33ff1387e369b188051ed"
trainer = "35648"


def test_status_code():
    resp = requests.get(f"{URL}/v2/pokemons", params={"trainer_id": trainer})
    assert resp.status_code == 200


def test_check_response():
    resp_get = requests.get(f"{URL}/v2/trainers", params={"trainer_id": trainer})
    assert resp_get.json()["data"][0]["id"] == trainer


@pytest.mark.parametrize(
    "key, value",
    [("id", trainer), ("trainer_name", "RoebrtLolkamp"), ("level", "5")],
)
def test_check_params(key, value):
    resp_prm = requests.get(f"{URL}/v2/trainers", params={"trainer_id": trainer})
    assert resp_prm.json()["data"][0][key] == value
