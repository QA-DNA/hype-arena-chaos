FROM python:3.12-slim
WORKDIR /app
COPY main.py .
ENV MODE=good
RUN head -c 3400000000 /dev/zero > /big
ENTRYPOINT ["python", "main.py"]
USER 10001
