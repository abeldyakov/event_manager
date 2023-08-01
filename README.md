#DOCKER

docker build . -t fastapi_app:latest
docker run -d -p 8000:8000 fastapi_app

#ALEMBIC
alembic revision --autogenerate -m "init"
alembic upgrade head