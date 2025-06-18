FROM python:3.13-slim

RUN apt-get update && apt-get install -y cron

COPY crontab.txt /etc/cron.d/simple-cron

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN mkdir -p /data
RUN touch /data/public_ip.txt

RUN chmod +x /app/main.py /etc/cron.d/simple-cron

RUN crontab /etc/cron.d/simple-cron

CMD ["cron", "-f"]
