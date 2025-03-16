##  Задаём родительский (главный) образ
FROM python:3

## Устанавливаем рабочую директорию для инструкции CMD и ENTRYPOINT
WORKDIR /code

## Копируем файлы и директории в контейнер
COPY ./requirements.txt /code/


# Install Pillow dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev

## Запускаем команды, создаём слой образа. 
## Используется для установки пакетов и библиотек внутри контейнера.
RUN pip install -r requirements.txt

## Копируем файлы и директории в контейнер
COPY . .