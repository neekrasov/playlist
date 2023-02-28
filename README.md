# RPC-сервис для взаимодействия с плейлистами

## Технический стек
`Python/asyncio`, `Grpc`, `SQLAlchemy (PostgreSQL)`, `Docker / docker-compose`, `pytest`.

## Основное
In process ...

## Развертывание

1. Клонировать репозиторий.

```
~$ git clone https://github.com/neekrasov/playlist.git
```

2. Создать файлы .env на примере корневой директории и директории `/docker`.
```
~$ mv .env.example .env && mv docker/.env.example docker/.env
```

3. Поднять контейнеры.
```
~$ make compose-up
```
4. Посмотреть запуск в логах
```
~$ make compose-logs
```
