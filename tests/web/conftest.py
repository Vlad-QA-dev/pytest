import pytest
import requests

API_BASE = "https://api.pokemonbattle-stage.ru"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def browser():
    """
    Basic fixture to open browser
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def knockout():
    HEADER = {
        "Content-Type": "application/json",
        "trainer_token": "ded72f74229ebfbdb79e0a4c18094db8",
    }
    pokemons = requests.get(
        url=f"{API_BASE}/v2/pokemons",
        params={"trainer_id": 2746},
        headers=HEADER,
    )
    for pok in pokemons.json()["data"]:
        if pok["status"] != 0:
            requests.post(
                url=f"{API_BASE}/v2/pokemon/knockout",
                headers=HEADER,
                json={"pokemon_id": pok["id"]},
            )
