FROM apache/airflow:3.0.2

USER root

#Dependencias del sistema necesarias para algunos paquetes Python 
RUN apt-get update && apt-get install -y gcc

USER airflow

# Istala dependencias del proyecto 
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt