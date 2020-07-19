FROM python:3.8.4-slim-buster as base

FROM base as builder

WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --prefix /install -r /requirements.txt

FROM base

WORKDIR /bot

COPY --from=builder /install /usr/local
COPY bot.py .
COPY mcad mcad

CMD ["python", "/bot/bot.py"]
