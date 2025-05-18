FROM python:3.11-slim

ARG PASSWORD
ENV PASSWORD=${PASSWORD}

WORKDIR /alert
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .  

CMD ["python", "alert.py"]
