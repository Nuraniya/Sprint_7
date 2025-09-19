import pytest
import requests
from generators import register_new_courier_and_return_login_password


@pytest.fixture
def base_url():
    return 'https://qa-scooter.praktikum-services.ru/api/v1'


@pytest.fixture
def create_courier():
    courier_data = register_new_courier_and_return_login_password()
    return courier_data


@pytest.fixture
def create_and_login_courier():
    courier_data = register_new_courier_and_return_login_password()

    payload = {
        "login": courier_data[0],
        "password": courier_data[1]
    }

    login_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
    courier_id = login_response.json().get("id")

    return courier_data, courier_id


@pytest.fixture
def cleanup_courier():
    couriers_to_delete = []

    yield couriers_to_delete

    for courier_data in couriers_to_delete:
        payload = {
            "login": courier_data[0],
            "password": courier_data[1]
        }
        login_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=payload)
        requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{login_response.json().get("id")}')