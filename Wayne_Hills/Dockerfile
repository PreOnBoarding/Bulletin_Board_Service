FROM python:3.9.13-alpine3.15
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt