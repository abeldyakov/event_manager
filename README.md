#DOCKER

docker build . -t event_app:latest

docker run -d -p 8000:8000 event_app

#ALEMBIC

alembic revision --autogenerate -m "message"

alembic upgrade head

#SECRET

openssl rand -base64 172 | tr -d '\ n'

#TODOs
1. logout
2. Добавить роли пользователей
3. Добавить асинхронное взаимодействие
