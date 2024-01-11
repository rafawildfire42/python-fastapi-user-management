poetry run alembic upgrade head
export PYTHONPATH=/app/src:$PYTHONPATH
psql -U admin -d main -h postgres -f populate_database.sql
poetry run celery --workdir /app/src/apps/users -A tasks worker -l debug &
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000