FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=oom

ENTRYPOINT ["python", "main.py"]
USER 10001
