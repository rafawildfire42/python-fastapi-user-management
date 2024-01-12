make runserver:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

makemigration:
	alembic revision --autogenerate -m "${msg}"

migration:
	alembic upgrade head

delete-cache:
	find . -name "__pycache__" -exec rm -r {} \;

format:
	autopep8 --in-place --recursive .

celery:
	celery --workdir /app/src/apps/users -A tasks worker --loglevel=INFO