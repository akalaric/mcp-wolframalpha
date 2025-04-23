FROM python:3.11-alpine

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python3", "src/core/server.py"]