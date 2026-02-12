FROM python:3.12-slim

RUN useradd -m worker
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .
COPY words_dictionary.txt .

USER worker

EXPOSE 8000

CMD ["uvicorn", "worker:app", "--host", "0.0.0.0", "--port", "8000"]