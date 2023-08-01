#DOCKER

docker build . -t fastapi_app:latest
docker run -d -p 8000:8000 fastapi_app

#ALEMBIC

alembic revision --autogenerate -m "message"
alembic upgrade head

#SECRET

openssl rand -base64 172 | tr -d '\ n'