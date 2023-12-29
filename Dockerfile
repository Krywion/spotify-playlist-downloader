FROM python:3-alpine3.19
LABEL authors="makskrywionek"

WORKDIR /app
COPY . /app

RUN apk update && apk add ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python ./src/app.py

