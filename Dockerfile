FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN pip3 install poetry

RUN poetry install

RUN poetry run python manage.py migrate


