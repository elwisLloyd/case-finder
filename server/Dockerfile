FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/server

WORKDIR /app/server

COPY server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY server/app ./app
COPY data/train /app/data/train

RUN useradd --create-home --uid 10001 casefinder \
    && mkdir -p /app/storage \
    && chown -R casefinder:casefinder /app/storage

USER casefinder

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
