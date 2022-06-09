# Групповой проект YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр из списка предустановленных. Список категорий или жанров может быть расширен только администратором.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. 

## Технологии
* Python
* Django
* Django REST Framework
* Simple JWT
* django-filter

## Как запустить проект
Клонировать репозиторий:
```
git@github.com:AlexGriv/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source venv/Scripts/activate
```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
Документация по проекту доступна по адресу 'http://127.0.0.1:8000/redoc/'

## Регистрация новых пользователей

* Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт '/api/v1/auth/signup/'
* Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email
* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт '/api/v1/auth/token/', в ответе на запрос ему приходит token (JWT-токен)

## Пример POST-запроса:

POST .../api/v1/titles/
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
Пример ответа:
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
        "name": "string",
        "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

## Над проектом работала команда студентов Яндекс.Практикума:
* Александр
* Шухрат
* Анна