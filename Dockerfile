FROM python:3.11

WORKDIR /example

COPY requirements.txt /example/
RUN pip install -r requirements.txt

COPY example /example
COPY data /example/data
