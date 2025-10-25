import pytest
import requests
import allure
import random
from generators import generate_random_string
from data import ERROR_MESSAGES, STATUS_CODES, COURIER_TEST_DATA, MISSING_FIELDS_TEST_DATA
from urls import URLs


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self, create_test_courier):
        assert create_test_courier["id"] is not None

    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            payload = COURIER_TEST_DATA["duplicate"].copy()
            payload["login"] = courier_data["login"]

            response = requests.post(URLs.COURIER, json=payload)
            assert response.status_code == STATUS_CODES["conflict"]
            assert ERROR_MESSAGES["login_already_exists"] in response.json()["message"]

    @pytest.mark.parametrize("missing_field,payload_data", MISSING_FIELDS_TEST_DATA)
    @allure.title("Тест: создание курьера без обязательного поле возвращает ошибку")
    def test_create_courier_without_required_field_returns_error(self, missing_field, payload_data):
        with allure.step(f"Попытаться создать курьера без поля {missing_field}"):
            response = requests.post(URLs.COURIER, json=payload_data)
            assert response.status_code == STATUS_CODES["bad_request"]
            assert ERROR_MESSAGES["not_enough_data"] in response.json()["message"]

    @allure.title("Тест: создание курьера без имени - успешно")
    def test_create_courier_without_first_name_success(self, cleanup_courier):
        login = generate_random_string(10)
        password = generate_random_string(10)

        with allure.step("Создать курьера без имени"):
            payload = COURIER_TEST_DATA["without_first_name"].copy()
            payload["login"] = login
            payload["password"] = password

            response = requests.post(URLs.COURIER, json=payload)
            assert response.status_code == 201
            assert response.json().get("ok") == True

        with allure.step("Авторизоваться под созданным курьером"):
            login_payload = {"login": login, "password": password}
            login_response = requests.post(URLs.COURIER_LOGIN, json=login_payload)
            assert login_response.status_code == 200

        cleanup_courier.append(login_response.json().get("id"))

    @allure.title("Тест: успешный запрос возвращает правильный код ответа")
    def test_successful_request_returns_correct_code(self, create_test_courier):
        assert create_test_courier["id"] is not None

    @allure.title("Тест: создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            payload = COURIER_TEST_DATA["duplicate"].copy()
            payload["login"] = courier_data["login"]

            response = requests.post(URLs.COURIER, json=payload)
            assert response.status_code == STATUS_CODES["conflict"]
            assert ERROR_MESSAGES["login_already_exists"] in response.json()["message"]