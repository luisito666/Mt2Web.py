FROM ubuntu:18.04

LABEL maintainer="luispenagos91@gmail.com"

ENV TERM=xterm

RUN apt-get update && \
apt-get install -y build-essential && \
apt-get install -y python3 python3-pip libmysqlclient-dev && \
apt-get clean &&\
pip3 install --upgrade pip &&\
mkdir -p /home/data/www

ADD ./src/requirements.txt /var/www/html/Mt2Web.py/

COPY ./compose/dev/django/start /
RUN chmod +x /start

WORKDIR /var/www/html/Mt2Web.py

RUN pip install -r requirements.txt

RUN apt-get remove -y build-essential

# CMD gunicorn --bind 0.0.0.0:8000 -w 1 --threads 4 core.wsgi:application

CMD ["/start"]
