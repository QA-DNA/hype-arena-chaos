FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=good

ENTRYPOINT ["python", "main.py"]

