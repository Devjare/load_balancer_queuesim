# FROM ubuntu:latest
FROM anthonyzou/alpine-build-essentials:latest

# LOAD ENV Variables.
ARG SAMPLES
ARG SIZE
ARG INTER_ARRIVAL
ARG READ_RATIO
ARG SAS
ARG DISTRIBUTION
ARG MEAN
ARG STDEV
ARG CONCURRENCY

COPY . /generator
WORKDIR /generator

# RUN apt-get -y update 
# RUN apt-get install -y build-essential
RUN make clean && make

CMD ["/bin/ash", "generate.sh"]
