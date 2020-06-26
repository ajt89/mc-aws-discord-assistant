FROM python:3.6.10-slim-buster as base

FROM base as builder

WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --prefix /install -r /requirements.txt

FROM base

WORKDIR /bot

COPY --from=builder /install /usr/local
COPY bot .

CMD ["python", "/bot/bot.py"]
