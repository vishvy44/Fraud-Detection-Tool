FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install apt-transport-https vim -y && apt-get clean 
# App setup
ADD . /code
WORKDIR /code
# Requirements installation
RUN pip install --no-cache-dir -r requirements.txt
