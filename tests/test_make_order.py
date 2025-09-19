import pytest
import requests
import allure
import random
import string
from data import BASE_URL, ORDER_DATA, ORDER_COLORS


def generate_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for _ in range(length))


@allure.feature("Создание заказа")
class TestMakeOrder:

    @pytest.mark.parametrize("color", ORDER_COLORS)
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_different_colors(self, color):
        order_data = ORDER_DATA.copy()
        order_data["color"] = color
        order_data["firstName"] = generate_random_string(10)
        order_data["lastName"] = generate_random_string(10)

        response = requests.post(f'{BASE_URL}/orders', json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа без поля color")
    def test_create_order_without_color_field(self):

        order_data = ORDER_DATA.copy()
        order_data.pop("color", None)
        order_data["firstName"] = generate_random_string(10)
        order_data["lastName"] = generate_random_string(10)

        response = requests.post(f'{BASE_URL}/orders', json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с вашими данными из data.py")
    def test_create_order_with_data_from_data_py(self):

        response = requests.post(f'{BASE_URL}/orders', json=ORDER_DATA)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Создание заказа с минимальными данными")
    def test_create_order_with_minimal_data(self):

        order_data = {
            "firstName": "Сергей",
            "lastName": "Пушков",
            "address": "Москва, ул. Ленина, 89",
            "metroStation": 4,
            "phone": "+7 800 446 22 35",
            "rentTime": 5,
            "deliveryDate": "2025-07-22"
        }

        response = requests.post(f'{BASE_URL}/orders', json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()