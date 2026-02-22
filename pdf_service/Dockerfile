FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./

RUN uv pip install --system --no-cache -r pyproject.toml

COPY . ./pdf_service/

EXPOSE 8001

# Тут може бути запуск API або воркера SQS
CMD ["uvicorn", "pdf_service.pdf_main:app", "--host", "0.0.0.0", "--port", "8001"]