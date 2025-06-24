import requests
import faker
from faker import Faker

fake = Faker()
random_name = fake.first_name()

URL = "https://api.pokemonbattle.ru"
Token = "820739400fd33ff1387e369b188051ed"
pokemon_id_cn = "343296"
trainer = "35648"

Header = {
    "Content-Type": "application/json",
    "trainer_token": Token,
}
body_reg = {
    "trainer_token": Token,
    "email": "robertlokam@yandex.ru",
    "password": "Iloveqa1",
}
body_create = {"name": random_name, "photo_id": -1}

body_cnockout = {
    "pokemon_id": pokemon_id_cn,
}

"""resp = requests.post(url=f"{URL}/v2/trainers/reg", headers=Header, json=body_reg)
print(resp.text)"""

resp_knockout = requests.post(
    url=f"{URL}/v2/pokemons/knockout", headers=Header, json=body_cnockout
)

resp_create = requests.post(url=f"{URL}/v2/pokemons", headers=Header, json=body_create)
print(resp_create.status_code)

pokemon_id = resp_create.json()["id"]
print(pokemon_id)

resp_get = requests.get(f"{URL}/v2/trainers", params={"trainer_id": trainer})
print(resp_get.text)
