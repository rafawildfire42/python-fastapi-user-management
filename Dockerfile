FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y python3-poetry
RUN poetry install
RUN apt-get install -y postgresql-client

EXPOSE 8000

ENV PGPASSWORD=paneas
ENV RABBIT_MQ_HOST=rabbitmq
ENV POSTGRES_HOST=postgres

# ENTRYPOINT bash ./run.sh

# CMD ["bash", "-c", "poetry run alembic upgrade head && psql -U admin -d main -h postgres -f populate_database.sql && poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 & && poetry run celery --workdir /app/src/apps/users -A tasks worker"]
