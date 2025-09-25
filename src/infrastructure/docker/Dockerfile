FROM python:3.11.4

WORKDIR /app

ENV TZ="America/Sao_Paulo"

RUN ls -la
COPY ./ /app
COPY src/infrastructure/requirements.txt /tmp/requirements.txt

RUN apt update && apt install -y nano build-essential libpq-dev python3-dev
RUN apt update && apt install -y ffmpeg libsm6 libxext6
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt --no-cache

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"]
