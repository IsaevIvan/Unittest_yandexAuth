# tests/test_yandex_auth.py
import time
import unittest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from yandex_auth import is_login_successful, get_profile_link, get_error_message


class TestYandexAuthFirefox(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.login = os.getenv("YANDEX_LOGIN")
        self.password = os.getenv("YANDEX_PASSWORD")

        options = Options()
        # options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.service = Service(
            executable_path='/snap/bin/geckodriver')
        self.driver = webdriver.Firefox(service=self.service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_yandex_auth_firefox(self):
        self.driver.get("https://passport.yandex.ru/auth/add/login")
        time.sleep(20)

        # Ввод логина
        login_field = WebDriverWait(self.driver, 20).until(  # Увеличиваем время ожидания
            EC.presence_of_element_located((By.CSS_SELECTOR, "#passp-field-login"))  # Используем CSS-селектор
        )
        login_field.send_keys(self.login)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(20)

        # Ввод пароля
        password_field = WebDriverWait(self.driver, 20).until(  # Увеличиваем время ожидания
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='passwd']"))  # Используем CSS-селектор
        )
        password_field.send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(20)


        # Проверка успешной авторизации с использованием is_login_successful()
        self.assertTrue(is_login_successful(self.driver), "Авторизация не удалась.")

        # Альтернативный способ проверки URL профиля (если нужно):
        profile_url = get_profile_link(self.driver)
        self.assertIsNotNone(profile_url, "Не удалось получить URL профиля.")

    # def test_yandex_auth_firefox_incorrect_password(self):
    #     """Тест авторизации с неверным паролем."""
    #     self.driver.get("https://passport.yandex.ru/auth/add/login")
    #
    #     # Ввод логина
    #     login_field = WebDriverWait(self.driver, 20).until(  # Увеличиваем время ожидания
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='login']"))  # Используем CSS-селектор
    #     )
    #     login_field.send_keys(self.login)
    #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #
    #     # Ввод неверного пароля
    #     password_field = WebDriverWait(self.driver, 20).until(  # Увеличиваем время ожидания
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='passwd']"))  # Используем CSS-селектор
    #     )
    #     password_field.send_keys("incorrect_password")  # Используем неверный пароль
    #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #
    #     # Проверка, что авторизация не удалась (ищем сообщение об ошибке)
    #     error_message = get_error_message(self.driver)
    #     self.assertIsNotNone(error_message, "Сообщение об ошибке не найдено")
    #     # Можно также проверить, что текст сообщения об ошибке соответствует ожидаемому:
    #     self.assertIn("Неверный пароль", error_message, "Текст сообщения об ошибке неверный")