FROM python:3.7-alpine

RUN apk update
RUN apk add gcc python3-dev musl-dev postgresql-dev
RUN python -m pip install --upgrade pip

RUN pip install \
    flask \
    flask-reggie \
    psycopg2 \
    simplejson \
    sqlalchemy \
    gunicorn \
    geopy

RUN mkdir /app
WORKDIR /app
COPY app/ ./

EXPOSE 5000

ENTRYPOINT gunicorn -b 0.0.0.0:5000 app:app