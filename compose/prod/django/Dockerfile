FROM ubuntu:18.04

LABEL maintainer="luispenagos91@gmail.com"

ENV TERM=xterm

RUN apt-get update && \
apt-get install -y build-essential && \
apt-get install -y python3 python3-pip libmysqlclient-dev && \
apt-get clean &&\
pip3 install --upgrade pip

# RUN mkdir -p /var/www/html/Mt2Web.py/ && \
# wget https://raw.githubusercontent.com/luisito666/Mt2Web.py/master/requirements.txt --directory-prefix=/var/www/html/Mt2Web.py/
ADD ./requirements.txt /var/www/html/Mt2Web.py/

# ADD nginx/default /etc/nginx/sites-available/default

WORKDIR /var/www/html/Mt2Web.py

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 -w 1 --threads 4 core.wsgi:application

# CMD ["python3", "manage.py", "runserver"]
