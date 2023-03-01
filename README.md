# RPC-сервис для взаимодействия с плейлистами
Ссылка на тз: https://github.com/gocloudcamp/test-assignment
## Технический стек
`Python/asyncio`, `Grpc`, `DI`, `SQLAlchemy (PostgreSQL)`, `Docker / docker-compose`, `pytest`.

## Основное
Реализовано:
1. Базовый CRUD по плейлистами.
2. Базовый CRUD по трекам плейлистов.
3. Имеется возможность взаимодействовать с несколькими плейлистами одновременно.
4. Play, Pause, Next, Prev методы управления плейлистом.
5. Протестированы бизнес-сценарии и их краевые случаи (из технических требований).
6. В качестве протокола взаимодействия сервиса с клиентами используется GRPC. Обработаны все ошибки.
7. Развёрнут в docker-контейнере (запуск под заголовком "Развёртывание").

Когда плейлист проигрывается он находится в памяти. Методы взаимодействия (Pause, Next, Prev) с плейлистом доступны только когда плейлист проигрывается. Кеш автоматически очищается, когда трек стоит на паузе больше N-секунд.

Вопроизведение эмулируется и переключение треков происходит с конца до начала, в порядке добавления (ассоциация с любым плеером: spotify, vk). 

Архитектура:

Проект разделён на слои, все зависимости направлены внутрь. бизнес-логика не зависит от внешних сервисов. Вся предметная логика находится в сущности Playlist.

Связывание отдельных системных обработчиков происходит с помощью паттерна "Медиатор". Подстановка реализаций протоколов на grpc уровне
происходит с помощью DI.

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
