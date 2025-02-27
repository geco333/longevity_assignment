FROM python:3.12-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
