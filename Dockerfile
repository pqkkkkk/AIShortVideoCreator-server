FROM python:3.11.13-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/src

CMD [ "fastapi", "run","app/main.py", "--port", "8000" ]

