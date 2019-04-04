FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
COPY app/ ./

#RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt

ENTRYPOINT ./app.py