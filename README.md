# СБОРКА ПРОЕКТА В Docker Compose

# Перечень контейнеров:
-app - основное приложение - ports: 8000:8000 
-db - база данных postgres
-redis - брокер сообщений
-celery worker - рабочие задачи
-celery-beat - планировщик задач

# Запуск сборки
docker-compose up -d --build

