FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /ormal
COPY requirements.txt /ormal/
RUN pip install -r requirements.txt
COPY . /ormal/