FROM python:3.9.13-alpine3.15
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apk update
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev libpq-dev
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt