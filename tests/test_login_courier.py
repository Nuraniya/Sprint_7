import pytest
import requests
import allure
from generators import register_new_courier_and_return_login_password
from data import ERROR_MESSAGES, STATUS_CODES
from urls import URLs


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Тест: курьер может авторизоваться")
    def test_courier_can_login(self, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        response = requests.post(URLs.COURIER_LOGIN, json=payload)

        assert response.status_code == 200
        assert "id" in response.json()

        courier_id = response.json()["id"]
        cleanup_courier.append(courier_id)

    @allure.title("Тест: для авторизации нужно передать все обязательные поля")
    def test_login_requires_all_fields(self, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()

        # Тест без пароля
        payload_without_password = {"login": courier_data[0]}
        response = requests.post(URLs.COURIER_LOGIN, json=payload_without_password)
        assert response.status_code == 400
        assert ERROR_MESSAGES["not_enough_login_data"] in response.json()["message"]

        # Тест без логина
        payload_without_login = {"password": courier_data[1]}
        response = requests.post(URLs.COURIER_LOGIN, json=payload_without_login)
        assert response.status_code == 400
        assert ERROR_MESSAGES["not_enough_login_data"] in response.json()["message"]

        correct_payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(URLs.COURIER_LOGIN, json=correct_payload)
        cleanup_courier.append(login_response.json().get("id"))

    @allure.title("Тест: система вернёт ошибку при неправильном логине")
    def test_login_with_wrong_login_returns_error(self, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": "wrong_login",
            "password": courier_data[1]
        }

        response = requests.post(URLs.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

        correct_payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(URLs.COURIER_LOGIN, json=correct_payload)
        cleanup_courier.append(login_response.json().get("id"))

    @allure.title("Тест: система вернёт ошибку при неправильном пароле")
    def test_login_with_wrong_password_returns_error(self, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": "wrong_password"
        }

        response = requests.post(URLs.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

        correct_payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(URLs.COURIER_LOGIN, json=correct_payload)
        cleanup_courier.append(login_response.json().get("id"))

    @allure.title("Тест: авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user_returns_error(self):
        payload = {
            "login": "nonexistent_user",
            "password": "nonexistent_password"
        }

        response = requests.post(URLs.COURIER_LOGIN, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: успешный запрос возвращает id")
    def test_successful_login_returns_id(self, cleanup_courier):
        courier_data = register_new_courier_and_return_login_password()

        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }

        response = requests.post(URLs.COURIER_LOGIN, json=payload)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

        cleanup_courier.append(response.json().get("id"))

    @allure.title("Тест: логин с неправильными данными из data.py")
    def test_login_with_invalid_data_from_data_py(self):
        from data import INVALID_LOGIN_DATA

        for invalid_data in INVALID_LOGIN_DATA:
            response = requests.post(URLs.COURIER_LOGIN, json=invalid_data)
            assert response.status_code == 400
            assert ERROR_MESSAGES["not_enough_login_data"] in response.json()["message"]