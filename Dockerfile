FROM python:3.13-slim

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN touch public_ip.txt

CMD ["python", "main.py"]

