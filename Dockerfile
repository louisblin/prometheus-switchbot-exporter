FROM arm32v7/python:3.7-slim-buster

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip libglib2.0-dev
RUN pip3 install -r requirements.txt
