FROM python:3.10-slim

WORKDIR /app

COPY ./app /app/app
COPY ./static /app/static
COPY main.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
