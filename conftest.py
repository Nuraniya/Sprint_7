import pytest
import requests
import random
from generators import generate_random_string
from urls import URLs


@pytest.fixture
def cleanup_courier():
    courier_ids_to_delete = []
    yield courier_ids_to_delete

    for courier_id in courier_ids_to_delete:
        try:
            requests.delete(URLs.COURIER_DELETE.format(id=courier_id))
        except:
            pass


@pytest.fixture
def create_test_courier(cleanup_courier):
    login = f"testuser_{random.randint(1000, 9999)}"
    password = f"password_{random.randint(1000, 9999)}"
    first_name = f"name_{random.randint(1000, 9999)}"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(URLs.COURIER, json=payload)
    assert response.status_code == 201

    login_payload = {"login": login, "password": password}
    login_response = requests.post(URLs.COURIER_LOGIN, json=login_payload)
    courier_id = login_response.json().get("id")

    cleanup_courier.append(courier_id)

    return {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }


@pytest.fixture
def create_duplicate_courier_data(cleanup_courier):
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(URLs.COURIER, json=payload)
    assert response.status_code == 201

    login_payload = {"login": login, "password": password}
    login_response = requests.post(URLs.COURIER_LOGIN, json=login_payload)
    courier_id = login_response.json().get("id")
    cleanup_courier.append(courier_id)

    return {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }