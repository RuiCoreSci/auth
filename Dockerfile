
FROM python:3.8.3-buster
MAINTAINER ruicore <hrui835@gmail.com>
RUN mkdir -p /home/ruicore/auth
WORKDIR /home/ruicore/auth
COPY requirements.txt ./
RUN pip3 install --upgrade pip -i https://pypi.doubanio.com/simple && pip3 install --no-cache-dir -r requirements.txt -i https://pypi.doubanio.com/simple
COPY . /home/ruicore/auth
