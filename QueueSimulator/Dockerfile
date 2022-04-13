# FROM ubuntu:latest
# FROM ubuntu:latest
FROM anthonyzou/alpine-build-essentials:latest

COPY . /simulator
WORKDIR /simulator

ARG TEST_NO

# RUN apt-get -y update
# RUN apt-get -y install build-essential
RUN make clean && make

# ENTRYPOINT "/bin/ash"
# CMD ["/bin/ash", "simul.sh"]
