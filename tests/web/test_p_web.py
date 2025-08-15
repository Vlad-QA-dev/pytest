import pytest
import requests

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

URL = "https://pokemonbattle-stage.ru/"
stage_l = "robertlokam@yandex.ru"
stage_p = "etemoP75"

CASES = [
    ("1", "robertlokamyandex.ru", "etemoP75", ["Введите корректную почту", ""]),
    ("2", "robertlokam@yandex.ru", "etemoP756", ["", "Неверные логин или пароль"]),
    ("3", "robertlokam@yandex", "etemoP756", ["Введите корректную почту", ""]),
    ("4", " ", "etemoP75", ["Введите корректную почту", ""]),
    ("5", "robertlokam@yandex.ru", " ", ["", "Неверные логин или пароль"]),
]


def test_positive_log(browser):
    """
    TRP-1. Positive login test for stage environment
    """
    browser.get(URL)

    email_input = browser.find_element(By.ID, "k_email")
    email_input.click()
    email_input.send_keys(stage_l)

    password_input = browser.find_element(By.ID, "k_password")
    password_input.click()
    password_input.send_keys(stage_p)

    button = browser.find_element(By.CSS_SELECTOR, ".k_form_send_auth")
    button.click()

    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.url_to_be(URL))
    #  trainer_id = browser.find_element(
    #     by=By.CSS_SELECTOR, value='[class="header_card_trainer_id_num"]' если нужно найти по точному классу
    # )
    trainer_id = browser.find_element(By.CLASS_NAME, "header_card_trainer_id_num")
    text = trainer_id.text
    assert text == "2746", "Trainer ID does not match expected value"


@pytest.mark.parametrize("case_number, email, password, allert", CASES)
def test_negative_log(case_number, email, password, allert, browser):
    """
    TRP-2. Negative login test for stage environment
    """
    logger.info(f"Running test case {case_number}")
    browser.get(URL)

    email_input = browser.find_element(By.ID, "k_email")
    email_input.click()
    email_input.send_keys(email)

    password_input = browser.find_element(By.ID, "k_password")
    password_input.click()
    password_input.send_keys(password)

    button = browser.find_element(By.CSS_SELECTOR, ".k_form_send_auth.css-cm2fpt")
    button.click()
    # Ждём появления любого из сообщений об ошибке по CSS
    WebDriverWait(browser, timeout=5).until(
        lambda d: d.find_elements(
            By.CSS_SELECTOR, ".auth__error:not(.k_main_error_text)"
        )
        or d.find_elements(By.CSS_SELECTOR, ".auth__error.k_main_error_text")
    )

    error_locators = [
        ".auth__error:not(.k_main_error_text)",
        ".auth__error.k_main_error_text",
    ]
    allerts_list = []
    for css in error_locators:
        elems = browser.find_elements(By.CSS_SELECTOR, css)
        text = elems[0].text.strip() if elems else ""
        allerts_list.append(text)
    assert allerts_list == allert


@pytest.mark.xfail(reason="waiting for fix ")
def test_e2e_api(browser, knockout):
    """
    TRP-3. E2E API test
    """
    browser.get(URL)
    WebDriverWait(browser, timeout=10, poll_frequency=1).until(
        EC.url_to_be(f"{URL}login")
    )

    email_input = browser.find_element(By.ID, "k_email")
    email_input.click()
    email_input.send_keys(stage_l)

    password_input = browser.find_element(By.ID, "k_password")
    password_input.click()
    password_input.send_keys(stage_p)

    button = browser.find_element(
        By.CSS_SELECTOR, ".k_form_send_auth.css-cm2fpt"
    ).click()
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be(URL))

    browser.find_element(
        By.CSS_SELECTOR, ".header_card_trainer.style_1_interactive_button_link"
    ).click()
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(
        EC.url_to_be(f"{URL}trainer/2746")
    )

    pok_count_bef = browser.find_element(
        By.CSS_SELECTOR, ".style_1_caption_16_400.pokemon_one_body_content_inner_box"
    )
    count_bef = int(pok_count_bef.text)

    body_create = {"name": "generate", "photo_id": -1}
    HEADER = {
        "Content-Type": "application/json",
        "trainer_token": "ded72f74229ebfbdb79e0a4c18094db8",
    }
    response_create = requests.post(
        url=f"{URL}v2/pokemon", headers=HEADER, json=body_create
    )
    assert response_create.status_code == 201, "unexpected status code"

    browser.refresh()
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(
        EC.url_to_be(f"{URL}trainer/2746")
    )

    pok_count_aft = browser.find_element(
        By.CSS_SELECTOR, "style_1_caption_16_400.pokemon_one_body_content_inner_box"
    )
    count_aft = int(pok_count_aft.text)
    assert count_aft - count_bef == 1
