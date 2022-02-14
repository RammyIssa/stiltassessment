FROM python:3
copy . /stiltassessment
WORKDIR /stiltassessment
CMD pip install -r requirements.txt
CMD python simulator.py