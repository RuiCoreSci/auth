FROM python:3.8.3-buster

WORKDIR /home/ruicore/auth

COPY . /home/ruicore/auth

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

LABEL ruicore="hrui835@gmail.com" version="v.0.0.1"