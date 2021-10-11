FROM python:3.7

COPY ./requirements.txt requirements.txt
COPY ./app /app
COPY ./prepare /prepare
COPY ./data /data
COPY ./intents.json intents.json
COPY ./main.py main.py

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install -r requirements.txt

CMD uvicorn main:app --reload