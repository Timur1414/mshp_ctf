FROM python:latest
LABEL authors="timat"
ENV PYTHONUNBUFFERED 1
RUN apt update && apt upgrade -y
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY main ./main
COPY mshp_ctf ./mshp_ctf
COPY manage.py .

EXPOSE 8000
