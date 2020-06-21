FROM python:3.6.10-slim-buster

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /bot

COPY bot .

CMD ["python", "/bot/bot.py"]
