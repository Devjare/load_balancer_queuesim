# FROM python:3.9-buster
FROM ubuntu:latest

COPY . /middleware
WORKDIR /middleware

# RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash"]
