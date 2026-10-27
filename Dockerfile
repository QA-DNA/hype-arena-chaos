FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=only-labels

ENTRYPOINT ["python", "main.py"]
USER 10001
