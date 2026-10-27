FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=huge-table

ENTRYPOINT ["python", "main.py"]
USER 10001
