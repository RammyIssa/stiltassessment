FROM ubuntu:latest
COPY . /stiltassessment
WORKDIR /stiltassessment
RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt
