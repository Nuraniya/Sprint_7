import pytest
import requests
import allure
from generators import register_new_courier_and_return_login_password
from data import ERROR_MESSAGES, STATUS_CODES, INVALID_LOGIN_DATA

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Тест: курьер может авторизоваться")
    def test_courier_can_login(self):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        response = requests.post(f'{BASE_URL}/courier/login', json=payload)

        assert response.status_code == STATUS_CODES["created"]
        assert "id" in response.json()

        courier_id = response.json()["id"]
        requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title("Тест: для авторизации нужно передать все обязательные поля")
    def test_login_requires_all_fields(self):
        courier_data = register_new_courier_and_return_login_password()

        payload_without_password = {
            "login": courier_data[0]
        }

        response_without_password = requests.post(f'{BASE_URL}/courier/login', json=payload_without_password)
        assert response_without_password.status_code == STATUS_CODES["bad_request"]
        assert ERROR_MESSAGES["not_enough_login_data"] in response_without_password.json()["message"]

        payload_without_login = {
            "password": courier_data[1]
        }

        response_without_login = requests.post(f'{BASE_URL}/courier/login', json=payload_without_login)
        assert response_without_login.status_code == STATUS_CODES["bad_request"]
        assert ERROR_MESSAGES["not_enough_login_data"] in response_without_login.json()["message"]

        correct_payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=correct_payload)
        requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')

    @allure.title("Тест: система вернёт ошибку при неправильном логине")
    def test_login_with_wrong_login_returns_error(self):
       courier_data = register_new_courier_and_return_login_password()

       payload = {
            "login": "wrong_login",
            "password": courier_data[1]
        }

       response = requests.post(f'{BASE_URL}/courier/login', json=payload)

       assert response.status_code == STATUS_CODES["not_found"]
       assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

       correct_payload = {"login": courier_data[0], "password": courier_data[1]}
       login_response = requests.post(f'{BASE_URL}/courier/login', json=correct_payload)
       requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')

    @allure.title("Тест: система вернёт ошибку при неправильном пароле")
    def test_login_with_wrong_password_returns_error(self):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }

        response = requests.post(f'{BASE_URL}/courier/login', json=payload)

        assert response.status_code == STATUS_CODES["not_found"]
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

        correct_payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=correct_payload)
        requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')

    @allure.title("Тест: авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user_returns_error(self):
        payload = {
            "login": "nonexistent_user",
            "password": "nonexistent_password"
        }

        response = requests.post(f'{BASE_URL}/courier/login', json=payload)

        assert response.status_code == STATUS_CODES["not_found"]
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: успешный запрос возвращает id")
    def test_successful_login_returns_id(self):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        response = requests.post(f'{BASE_URL}/courier/login', json=payload)

        assert response.status_code == STATUS_CODES["created"]
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

        requests.delete(f'{BASE_URL}/courier/{response.json().get("id")}')

    @allure.title("Тест: логин с неправильными данными из data.py")
    def test_login_with_invalid_data_from_data_py(self):
        for invalid_data in INVALID_LOGIN_DATA:
            response = requests.post(f'{BASE_URL}/courier/login', json=invalid_data)
            assert response.status_code == STATUS_CODES["bad_request"]
            assert ERROR_MESSAGES["not_enough_login_data"] in response.json()["message"]