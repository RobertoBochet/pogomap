FROM python:3.8-alpine

RUN apk update
RUN apk add \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev
RUN python -m pip install --upgrade pip

RUN mkdir /pogomap
WORKDIR /pogomap

COPY ./pogomap/requirements.txt ./

RUN pip install -r ./requirements.txt

COPY ./pogomap/ ./

EXPOSE 5775

ENTRYPOINT gunicorn -b 0.0.0.0:5775 "wsgi:gunicorn_entry()"
