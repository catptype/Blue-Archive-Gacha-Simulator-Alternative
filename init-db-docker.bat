@echo off
docker compose run --rm backend python -m backend_fastapi.create_db
docker compose run --rm backend python -m backend_fastapi.create_superuser admin 1234
pause