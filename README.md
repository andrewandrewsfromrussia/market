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

## Апдейт от 28.09.2025:

- `Страница одного товара: контроллер product_detail(pk) получает объект через ORM и рендерит catalog/product_detail.html (показываются все поля и изображение).`

- `Главная страница: контроллер home() делает ORM-запрос списка продуктов и рендерит catalog/home.html; описание на карточках обрезается до 100 символов.`

- `Базовый шаблон: вынесены head, фон, подключение Bootstrap 5, контейнер и футер в base.html.`

- `Подшаблон меню: partials/_menu.html — главное меню подключается на всех страницах.`

- `Единый стиль: тёмный фон, белый текст, жёлтые кнопки/акценты, hover-свечение; сетка карточек на Bootstrap.`

- `Медиа/изображения: корректный вывод product.image.url, настройка MEDIA_URL/MEDIA_ROOT (dev-раздача в DEBUG).`
