import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://the-internet.herokuapp.com/login"

@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(URL)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(f"screenshots/{name}.png")

def test_valid_login(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    message = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in message

def test_invalid_username(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    take_screenshot(driver, "invalid_username")
    message = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in message

def test_invalid_password(setup):
    driver = setup
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    take_screenshot(driver, "invalid_password")
    message = driver.find_element(By.ID, "flash").text
    assert "Your password is invalid!" in message

def test_empty_fields(setup):
    driver = setup
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    take_screenshot(driver, "empty_fields")
    message = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in message
