FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir '.[test]' && useradd --create-home worker && mkdir /data && chown worker:worker /data
COPY tests ./tests
USER worker
CMD ["energy", "ingest"]
