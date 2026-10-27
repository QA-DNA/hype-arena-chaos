FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=write-home

ENTRYPOINT ["python", "main.py"]
USER 10001
