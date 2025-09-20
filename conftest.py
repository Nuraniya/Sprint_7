import pytest
import requests
from generators import register_new_courier_and_return_login_password
from urls import URLs


@pytest.fixture
def base_url():
    return URLs.BASE_URL


@pytest.fixture
def create_courier_data():
    return register_new_courier_and_return_login_password()


@pytest.fixture
def cleanup_courier():
    courier_ids_to_delete = []
    yield courier_ids_to_delete

    for courier_id in courier_ids_to_delete:
        try:
            requests.delete(URLs.COURIER_DELETE.format(id=courier_id))
        except:
            pass