## Первый старт приложения
```
docker-compose up --build
alembic upgrade head
```

## Для просмотра документации
```
http://0.0.0.0:6565/docs
```
## После коммитов
```
docker-compose stop app

git pull origin main

docker-compose up -d --build --no-deps app
```

## Для подключения к базе через DBeaver
```
хост: localhost
порт: 5440
пользователь:postgres
пароль: qwerty

```