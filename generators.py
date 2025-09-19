import requests
import random
import string


def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))


    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)


    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    return [login, password, first_name]