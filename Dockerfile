FROM python:3
COPY . /stiltassessment
WORKDIR /stiltassessment
CMD pip3 install -r requirements.txt
CMD python simulator.py