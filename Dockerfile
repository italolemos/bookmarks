FROM python:3.9.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/