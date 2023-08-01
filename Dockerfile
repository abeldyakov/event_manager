FROM python:3.11-slim

RUN mkdir -p /otp/app/src/
WORKDIR /otp/app/src/

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#RUN chmod a+x *.sh

#WORKDIR /otp/app/

#CMD gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000