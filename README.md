## Foodgram

![workflow](https://github.com/Kirill-Drozdov/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

### О проекте:

Проект `Foodgram` - `Продуктовый помощник` представляет собой онлайн-сервис и `API` для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
```
python 3.7
django 2.2.16
djangorestframework 3.12.4
djoser
gunicorn
psycopg2-binary
```

### Как развернуть и запустить проект локально в контейнере:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Kirill-Drozdov/foodgram-project-react.git
```


В директории `infra` создать файл `.env` и заполнить его по шаблону `.env.template`,
используя свои данные для проекта:


Перейти в директорию `infra` и запустить сборку контейнера:

```
cd infra
```

Далее все команды выполнять из текущей директории.

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec web python manage.py makemigrations
```

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику в одну папку:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Заполнить базу тестовыми данными:

```
docker-compose exec web python manage.py load_csv
```

Ваш проект запущен и готов к работе!

### Примеры запросов (локально в контейнере):

После запуска проекта в контейнере пройти по адресу:

```
http://localhost/api/docs/
```
Там будет доступна документация для `API foodgram_project`,
представленая в формате `Redoc`.
В документации описано, как должен работать `API`.

Сайт `Продуктовый помощник` доступен по адресу:

```
http://localhost/
```

Панель администратора доступна по адресу:

```
http://localhost/admin/
```

### Об авторе проекта:
Проект выполнил студент Яндекс Практикума -
[Дроздов К.С.](https://github.com/Kirill-Drozdov)
