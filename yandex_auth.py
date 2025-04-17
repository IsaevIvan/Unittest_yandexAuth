from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver  # Для типизации

def is_login_successful(driver: WebDriver) -> bool:
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[href*="passport.yandex.ru/profile"]')
        return True
    except:
        return False

def get_profile_link(driver: WebDriver) -> str | None:
    try:
        profile_link_element = driver.find_element(By.CSS_SELECTOR, 'a[href*="passport.yandex.ru/profile"]')
        return profile_link_element.get_attribute("href")
    except:
        return None

def get_error_message(driver: WebDriver) -> str | None:
    try:
        error_element = driver.find_element(By.CSS_SELECTOR, ".passp-form-field__error")  # Пример CSS селектора для сообщения об ошибке
        return error_element.text
    except:
        return None