FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog_app

COPY . /blog_app

RUN pip install -r requirements.txt
