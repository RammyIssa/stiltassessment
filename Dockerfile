FROM python:3
COPY . /stiltassessment
WORKDIR /stiltassessment
RUN pip3 install -r requirements.txt
