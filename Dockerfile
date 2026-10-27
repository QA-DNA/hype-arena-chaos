FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=excel

ENTRYPOINT ["python", "main.py"]
USER 10001
