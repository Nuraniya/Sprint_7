BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

class URLs:
    COURIER = f'{BASE_URL}/courier'
    COURIER_LOGIN = f'{BASE_URL}/courier/login'
    COURIER_DELETE = f'{BASE_URL}/courier/{{id}}'
    ORDERS = f'{BASE_URL}/orders'