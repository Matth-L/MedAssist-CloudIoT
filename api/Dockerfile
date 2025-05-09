FROM python:3.11-slim

ARG PASSWORD
ENV PASSWORD=$PASSWORD

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .  

CMD ["python", "iot_captor_sim.py"]
