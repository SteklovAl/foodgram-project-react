# Дипломный проект курса "Python Developer"


## ip: 158.160.51.211

![This is an image](https://github.com/SteklovAl/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Описание

Онлайн-сервис на React и API для него. На этом сервисе пользователи могут делиться своими рецептами, подписываться на публикации понравившихся пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов.


### Описание Workflow

Workflow состоит из четырёх шагов:

- Проверка кода на соответствие PEP8, запуск тестов проекта.
- Сборка и публикация образа на DockerHub.
- Автоматический деплой на выбранный сервер.
- Отправка ботом уведомления в телеграм-чат.

### Подготовка и запуск проекта

Клонирование репозитория
`git clone https://github.com/SteklovAl/yamdb_final.git`

ip: 158.160.33.31

### Установка на удаленном сервере (Ubuntu):

Шаг 1. Вход на удаленный сервер
Подключаемся на удаленный сервер

`ssh <username>@<ip_address>`

Шаг 2. Установка docker:

`sudo apt install docker.io`

Шаг 3. Установка docker-compose:

`sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
`sudo chmod +x /usr/local/bin/docker-compose`

Шаг 4. Копирование `docker-compose.yaml` и `nginx/default.conf`:

Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf соответственно`.

`scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml`
`scp -r nginx/ <username>@<host>:/home/<username>/`

Шаг 5. Добавление Github Secrets:

Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

```
SECRET_KEY=<SECRET_KEY>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<pass DockerHub>
DOCKER_USERNAME=<login DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<passphrase для сервера, если он установлен>
SSH_KEY=<SSH ключ>

TELEGRAM_TO=<ID своего телеграм-аккаунта. Для инфо @myidbot>
TELEGRAM_TOKEN=<токен бота>
```
