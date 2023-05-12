FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip3 install poetry

RUN poetry install