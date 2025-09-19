# Базовый URL API
BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

# Данные для создания заказа
ORDER_DATA = {
    "firstName": "Сергей",
    "lastName": "Пушков",
    "address": "Москва, ул. Ленина, 89",
    "metroStation": 4,
    "phone": "+7 800 446 22 35",
    "rentTime": 5,
    "deliveryDate": "2025-07-22",
    "comment": "Тестовый заказ",
    "color": ["BLACK"]
}

# Данные для создания курьера
COURIER_DATA = {
    "login": "test_courier_login",
    "password": "test_password_123",
    "firstName": "ТестовыйКурьер"
}

# Данные для логина курьера
LOGIN_DATA = {
    "login": "test_user",
    "password": "test_password"
}

# Неправильные данные для тестирования ошибок
INVALID_LOGIN_DATA = [
    {"login": "", "password": "password123"},  # пустой логин
    {"login": "testuser", "password": ""},     # пустой пароль
    {"login": " ", "password": "password123"}, # пробел вместо логина
    {"login": "testuser", "password": " "}     # пробел вместо пароля
]

# Цвета для параметризации тестов заказов
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
]

# Ожидаемые сообщения об ошибках
ERROR_MESSAGES = {
    "not_enough_data": "Недостаточно данных для создания учетной записи",
    "not_enough_login_data": "Недостаточно данных для входа",
    "login_already_exists": "Этот логин уже используется",
    "account_not_found": "Учетная запись не найдена"
}

# Коды ответов HTTP
STATUS_CODES = {
    "success": 201,
    "created": 200,
    "bad_request": 400,
    "not_found": 404,
    "conflict": 409
}