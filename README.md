# Дипломный проект курса "Python Developer"


## Проект доступен по адресу ip: 158.160.51.211
### логин: Admin
### пароль: Error5936


![This is an image](https://github.com/SteklovAl/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Описание

Онлайн-сервис Продуктовый помошник. На этом сервисе пользователи могут делиться своими рецептами, подписываться на публикации понравившихся пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов.


### Подготовка и запуск проекта

Склонируйте репозиторий

`git clone https://github.com/SteklovAl/foodgram-project-react.git`

Cоздайте и активируйте виртуальное окружение:

```
python -m venv venv
. venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл .env в директории backend и заполните его данными по этому 
образцу:

```
SECRET_KEY=<SECRET_KEY>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=lokalhost
DB_PORT=5432
```

В директорию infra запустите docker-compose:

`docker-compose up`

Теперь в контейнере backend нужно выполнить миграции, создать суперпользователя и собрать статику. 

Выполните по очереди команды:

```
docker-compose backend web python manage.py makemigrations
docker-compose backend web python manage.py migrate
docker-compose backend web python manage.py createsuperuser
docker-compose backend web python manage.py collectstatic --no-input 
```

Проект будет доступен по адресу http://localhost/.


#### В проекте использованы технологии:

* Python
* React
* Django REST Framework
* Django
* Linux
* Docker
* Docker-compose
* Postgres
* Gunicorn
* Nginx
* Workflow



