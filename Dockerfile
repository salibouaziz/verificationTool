FROM python:3.11.1-slim
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "test1.py"]