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
    (
        "1",
        "robertlokamyandex.ru",
        "etemoP75",
        [
            "Введите корректную почту",
        ],
    ),
    ("2", "robertlokam@yandex.ru", "etemoP756", ["", "Неверные логин или пароль"]),
    (
        "3",
        "robertlokam@yandex",
        "etemoP756",
        [
            "Введите корректную почту",
        ],
    ),
    (
        "4",
        " ",
        "etemoP75",
        ["Введите почту", " "],
    ),
    ("5", "robertlokam@yandex.ru", " ", [" ", "ВВедите  пароль"]),
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

    button = browser.find_element(By.CSS_SELECTOR, ".k_form_send_auth")
    button.click()

    allert_massege = browser.find_elements(
        by=By.CSS_SELECTOR, value='[class*="auth__error"]'
    )
    allerts_list = []
    for element in allert_massege:
        allerts_list.append(element.text)

    assert allerts_list == allert

    # button.click()
