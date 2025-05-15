FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python3", "main.py", "--ui"]
