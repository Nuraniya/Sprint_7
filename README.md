# Тестирование API Яндекс Самокат

## Описание
Тесты для API сервиса доставки самокатов https://qa-scooter.praktikum-services.ru/

## Структура проекта
- `tests/` - тестовые модули
- `data.py` - тестовые данные и конфигурация
- `generators.py` - утилиты для генерации данных
- `conftest.py` - фикстуры pytest

## Запуск тестов
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск с Allure-отчетом
pytest --alluredir=allure-results
allure serve allure-results