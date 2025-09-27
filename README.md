# Market

## Страницы, путь:
- `/` — **Главная**
- `/contacts/` — **Контакты**

## Шаблоны

- `catalog/templates:`
- - `home.html` - главная
- - `contacts.html` - контакты


## Полезные команды/функции

Миграции:

- `poetry run python manage.py makemigrations`
- `poetry run python manage.py migrate`

Суперпользователь / админка:

- `poetry run python manage.py createsuperuser`
- `http://127.0.0.1:8000/admin/`

Загрузка фикстур:

- `poetry run python manage.py loaddata catalog/fixtures/categories.json`
- `poetry run python manage.py loaddata catalog/fixtures/products.json`

Кастомная команда (очистить и перезалить тестовые данные):

- `poetry run python manage.py reload_test_data`

Скриншоты по ДЗ:

- `screenshot/`
