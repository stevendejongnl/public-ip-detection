FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl \
  && curl -fsSL -o /usr/local/bin/supercronic https://github.com/aptible/supercronic/releases/latest/download/supercronic-linux-amd64 \
  && chmod +x /usr/local/bin/supercronic

RUN mkdir -p /app /data

RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /app /data

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN mkdir -p /data
RUN touch /data/public_ip.txt

USER appuser
CMD ["/usr/local/bin/supercronic", "/app/crontab.txt"]
