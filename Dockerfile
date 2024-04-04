FROM python:3.12.2-slim-bullseye

WORKDIR /TRADING BOT

COPY . .

RUN pip install -r requirements.txt

