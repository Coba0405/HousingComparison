FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic

COPY app /app/app

EXPOSE 8000

CMD ["python", "app/main.py"]
