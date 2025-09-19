import pytest
import requests
import allure
import random
from generators import register_new_courier_and_return_login_password
from data import ERROR_MESSAGES, STATUS_CODES

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self):
        courier_data = register_new_courier_and_return_login_password()

        payload = {"login": courier_data[0], "password": courier_data[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=payload)

        assert login_response.status_code == STATUS_CODES["created"]
        assert "id" in login_response.json()

        courier_id = login_response.json().get("id")
        requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self):
        first_courier = register_new_courier_and_return_login_password()

        payload = {
            "login": first_courier[0],
            "password": first_courier[1],
            "firstName": first_courier[2]
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == STATUS_CODES["conflict"]
        assert ERROR_MESSAGES["login_already_exists"] in response.json()["message"]

        login_payload = {"login": first_courier[0], "password": first_courier[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=login_payload)
        requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')

    @allure.title("Тест: создание курьера без логина возвращает ошибку")
    def test_create_courier_without_login_returns_error(self):
        payload = {
            "password": "password123",
            "firstName": "TestUser"
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"]

    @allure.title("Тест: создание курьера без пароля возвращает ошибку")
    def test_create_courier_without_password_returns_error(self):
        payload = {
            "login": "testuser",
            "firstName": "TestUser"
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        assert "Недостаточно данных для создания учетной записи" in response.json()["message"]

    @allure.title("Тест: создание курьера без имени - успешно")
    def test_create_courier_without_first_name_success(self):
        login = f"testuser_{random.randint(1000, 9999)}"
        password = f"password_{random.randint(1000, 9999)}"

        payload = {
            "login": login,
            "password": password

        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
        assert response.json().get("ok") == True

        login_payload = {"login": login, "password": password}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=login_payload)

        assert login_response.status_code == 200
        assert "id" in login_response.json()

        courier_id = login_response.json().get("id")
        requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title("Тест: успешный запрос возвращает правильный код ответа")
    def test_successful_request_returns_correct_code(self):
        result = register_new_courier_and_return_login_password()

        assert len(result) == 3, "Курьер должен быть создан успешно"
        assert result[0] is not None, "Логин не должен быть None"
        assert result[1] is not None, "Пароль не должен быть None"
        assert result[2] is not None, "Имя не должно быть None"

        payload = {"login": result[0], "password": result[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=payload)
        requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')

    @allure.title("Тест: создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self):
        first_courier = register_new_courier_and_return_login_password()

        payload = {
            "login": first_courier[0],  # тот же логин
            "password": "different_password",
            "firstName": "Different Name"
        }

        response = requests.post(f'{BASE_URL}/courier', data=payload)

        assert response.status_code == STATUS_CODES["conflict"]
        assert ERROR_MESSAGES["login_already_exists"] in response.json()["message"]

        login_payload = {"login": first_courier[0], "password": first_courier[1]}
        login_response = requests.post(f'{BASE_URL}/courier/login', json=login_payload)
        requests.delete(f'{BASE_URL}/courier/{login_response.json().get("id")}')