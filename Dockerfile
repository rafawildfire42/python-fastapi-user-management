FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt install -y python3-poetry
RUN poetry install
RUN apt install -y postgresql-client

EXPOSE 8000

ENV PGPASSWORD=paneas
ENV RABBIT_MQ_HOST=rabbitmq
ENV POSTGRES_HOST=postgres