# FROM python:3.9-buster
FROM jjuanda/numpy-pandas:latest

COPY . /middleware
WORKDIR /middleware

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
