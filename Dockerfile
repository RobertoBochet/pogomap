FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
COPY app/ ./

RUN apk update
RUN apk add gcc python3-dev musl-dev postgresql-dev
RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 5775

ENTRYPOINT gunicorn -b 0.0.0.0:5775 app:app