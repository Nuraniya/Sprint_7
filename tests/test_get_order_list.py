import pytest
import requests
import allure
from data import BASE_URL


@allure.feature("Получение списка заказов")
class TestGetOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):

        response = requests.get(f'{BASE_URL}/orders')

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Получение списка заказов с лимитом")
    def test_get_orders_list_with_limit(self):

        limit = 5
        response = requests.get(f'{BASE_URL}/orders?limit={limit}')

        assert response.status_code == 200
        assert "orders" in response.json()
        assert len(response.json()["orders"]) <= limit

    @allure.title("Получение списка заказов с параметром страницы")
    def test_get_orders_list_with_page(self):

        page = 1
        response = requests.get(f'{BASE_URL}/orders?page={page}')

        assert response.status_code == 200
        assert "orders" in response.json()