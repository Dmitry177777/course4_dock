##  Задаём родительский (главный) образ
FROM python:3.10-slim-buster

## Устанавливаем рабочую директорию для инструкции CMD и ENTRYPOINT
WORKDIR /code

## Копируем файлы и директории в контейнер
COPY ./requirements.txt /code/


# Install Pillow dependencies
RUN apt update && apt install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev

# Install PostgreSQL client libraries and headers.  build-essential is needed for compiling the C code that wraps postgres
RUN apt update && apt install -y --no-install-recommends build-essential libpq-dev

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade setuptools wheel

## Запускаем команды, создаём слой образа. 
## Используется для установки пакетов и библиотек внутри контейнера.
RUN pip install -r requirements.txt

## Копируем файлы и директории в контейнер
COPY . .