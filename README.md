![Foodgram](https://github.com/s2dent18/foodgram-project-react/workflows/foodgram_workflow/badge.svg)  

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
# Сервис Foodgram

```sh
git clone https://github.com/s2dent18/foodgram-project-react.git
```

## Описание сервиса:

Foodgram - сервис для публикации и обмена рецептами блюд и напитков.  
Для незарегестрированных пользователей доступны просмотр рецептов на главной странице,  
фильтрация рецептов по тегам и просмотр рецепта на отдельной странице.  
Авторизованные пользователи могут создавать / редактировать собственные рецепты, добавлять понравившиеся рецепты  
в список избранного. Также они могут просматривать страницы пользователей и подписываться на понравившихся авторов.  
Рецепты можно добавить в список покупок и выгрузить список необходимых ингредиентов в pdf формате.  

## Структура проекта:

* В папке frontend находятся файлы, необходимые для сборки фронтенда приложения  
* В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml  
* В папке backend находятся файлы, необходимые для сборки бэкенда приложения  
* В папке data подготовлен список ингредиентов с единицами измерения. Список сохранён в форматах JSON и CSV  
* В папке docs находятся файлы спецификации API  

## Подготовка к запуску:

Для работы с проектом вам понадобится [Docker](https://www.docker.com).  
Сервис разворачивается в 4-х контейнерах:  
* backend - api приложение  
* db - база данных  
* nginx - web-сервер  
* frontend - образ фронта проекта  

В целях безопасности некоторые переменные должны быть вынесены в файл окружения .env. Создайте его самостоятельно, а при разворачивании проекта на сервере перенесите их в Github actions secrets.  
Полный перечень переменных с комментариями:
* DJANGO_SECRET_KEY - секретный ключ для конкретной установки Django  
* SERVERNAMES - хосты, которые может обслуживать сайт, через пробел (по умолчанию доступен всем)  
* DB_ENGINE - используемая база данных (по умолчанию django.db.backends.postgresql)  
* DB_HOST - название контейнера базы данных (по умолчанию db)  
* DB_NAME - имя базы данных  
* DB_PORT - порт для подключения к базе данных (по умолчанию 5432)  
* DOCKER_PASSWORD - пароль Docker Hub  
* DOCKER_USERNAME - логин Docker Hub  
* HOST - IP-адрес вашего сервера  
* PASSPHRASE - Если при создании ssh-ключа вы использовали фразу-пароль, то укажите ее  
* POSTGRES_PASSWORD - пароль для подключения к базе данных  
* POSTGRES_USER - логин для подключения к базе данных  
* SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу  
* TELEGRAM_TO - ID телеграм-аккаунта. Узнать свой ID можно у бота @userinfobot  
* TELEGRAM_TOKEN - токен вашего бота. Получить этот токен можно у бота @BotFather  
* USER - имя пользователя для подключения к серверу  

## Локальный запуск проекта:

* Создайте файл с переменными виртуального окружения в папке backend/  
* Находясь в папке infra_local/ выполните команду:  
```sh
docker-compose up
```    
* Выполните миграции командой:  
```sh
docker-compose exec backend python manage.py migrate --noinput
```  
* Соберите файлы статики в одну директорию:  
```sh
docker-compose exec backend python manage.py collectstatic --noinput
```  

## Запуск проекта на сервере:

Проект разворачивался на сервере с ОС ubuntu 20.04. Дальнейшие инструкции приводятся для данной ОС.  

Для удобства работы с проектом вы можете воспользоваться сервисом GitHub Actions. Пример workflow файла находится в главной директории проекта. После внесения изменений в мастер ветку репозитория будет выполнена автоматическая проверка кода на соответствие стандартам PEP8, пуш контейнеров на DockerHub. Проект будет загружаться на ваш сервер и отправлять уведомления вам в Telegram.  Не забудьте перенести переменные окружения в Github actions secrets.  

* Установите Docker на ваш сервер:  
```sh
sudo apt install docker.io
```   
* Установите Docker-compose: 
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 
```  
* Скопируйте на сервер файлы Docker-compose.yml и nginx.conf из папки infra/. Не забудьте указать свой ip в конфиге.  
* При деплое на сервер через GitHub Actions файл зависимостей создается автоматически. Если вы хотите развернуть проект вручную, то создайте его самостоятельно.  
* Worflow файл запустит контейнеры автоматически. Самостоятельно запустить контейнеры вы можете командой:  
```sh
sudo docker-compose up
```    
* Вам останется применить миграции командой:  
```sh
sudo docker-compose exec backend python manage.py migrate --noinput
```  
* Собрать файлы статики:  
```sh
sudo docker-compose exec backend python manage.py collectstatic --noinput
```    
## Загрузка готовой базы ингредиентов:

Готовый файл лежит в папке backend/  
Выполните команду:  
```sh
docker-compose exec backend python manage.py loaddata ingredients.json
```

## Администрирование:

В проекте настроена панель администратора Django. В ней вы можете:  
* изменять пароль любого пользователя  
* создавать/блокировать/удалять аккаунты пользователей  
* редактировать/удалять любые рецепты  
* добавлять/удалять/редактировать ингредиенты  
* добавлять/удалять/редактировать теги  

Создать суперпользователя вы можете командой:  
```sh
docker-compose exec backend python manage.py createsuperuser
```  
(Не забудьте команду "sudo", если проект развернут на сервере)  

## Документация API:

Подробную документацию вы можете посмотреть пройдя по ссылке: [REDOC](http://62.84.115.215/api/docs/) . Локальный файл с документацией находится в папке docs/.  

## Готовые образы DockerHub:

[Backend](https://hub.docker.com/repository/docker/s2dent18/foodgram-backend)  
[Frontend](https://hub.docker.com/repository/docker/s2dent18/foodgram-frontend)  

## Пример готового проекта:

Проект доступен по адресу: http://62.84.115.215/  
