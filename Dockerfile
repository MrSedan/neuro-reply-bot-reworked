FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -U -r requirements.txt

CMD [ "python", "main.py" ]