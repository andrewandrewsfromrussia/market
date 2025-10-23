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

## Апдейт от 05.10.2025:

### Домашняя работа: Перевод FBV на CBV + Блог

Что сделано

- Перевёл все контроллеры приложения catalog с FBV на CBV (ListView, DetailView, TemplateView).`

- Добавил новую страницу контактов на основе TemplateView.

- Создано новое приложение blogs:

- Модель BlogPost с полями:

- -  `title` — заголовок

- - `content` — содержимое

- - `preview` — изображение-превью

- - `created_at` — дата создания

- - `is_published` — флаг публикации

- - `views` — счётчик просмотров

- Реализован полный CRUD через CBV (ListView, DetailView, CreateView, UpdateView, DeleteView).

Добавлена логика:

- счётчик просмотров увеличивается при открытии записи;

- в список выводятся только опубликованные статьи;

- после редактирования происходит редирект на страницу самой статьи.

- Для каждой CBV создан отдельный шаблон с наследованием от base.html и подключением меню (includes/_menu.html).


## update от 06.10.2025:

Что реализовано

#### Модель Product

- Поля: name, description, image, category, price, created_at, updated_at.

- Связь с моделью Category.

- CRUD для продуктов через формы (django.forms)

- - `ProductCreateView` → создание продукта.

- - `ProductUpdateView` → редактирование продукта.

- - `ProductDeleteView` → удаление продукта.

- - `ProductListView` → список продуктов (главная страница).

- - `ProductDetailView` → детальная страница продукта.

- Валидация форм

- Запрещённые слова: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар.

- Проверка в `clean_name` и `clean_description` (независимо от регистра).

- Кастомная валидация `price`: не может быть отрицательной.

#### Главная страница (home.html)

- Показывает карточки товаров с картинкой, названием, ценой и описанием.

- Добавлена кнопка “Добавить продукт”.

- В каждой карточке есть троеточие (⋮) с выпадающим меню: Редактировать / Удалить.

#### Шаблоны

- `product_form.html` → форма создания/редактирования продукта.

- `product_confirm_delete.html` → подтверждение удаления.

- `home.html` → список продуктов с кнопками и меню.

#### URLs

- `/` → главная страница (список продуктов).

- `/catalog/products/add/` → создать продукт.

- `/catalog/products/<id>/edit/` → редактировать продукт.

- `/catalog/products/<id>/delete/` → удалить продукт.

- `/catalog/products/<id>/` → детальная страница продукта