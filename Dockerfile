##  Задаём родительский (главный) образ
FROM python:3.10.12

## Устанавливаем рабочую директорию для инструкции CMD и ENTRYPOINT
WORKDIR /app

## Копируем файлы и директории в контейнер
COPY ./requirements.txt /app/


## Запускаем команды, создаём слой образа.
## Используется для установки пакетов и библиотек внутри контейнера.
RUN pip install -r requirements.txt

## Копируем файлы и директории в контейнер
COPY . .