FROM python:3.12-slim

RUN useradd -m worker
WORKDIR /app

COPY worker.py .

USER worker

CMD ["python", "worker.py"]