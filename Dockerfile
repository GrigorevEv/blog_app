FROM python:3.9.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog_app

COPY . /blog_app

RUN pip install -r requirements.txt

# Add crontab file in the cron directory
ADD cron_dump /etc/cron.d/cron_dump

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_dump

# Install Cron
RUN apt-get update
RUN apt-get -y install cron

