FROM ubuntu:utopic

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-dev curl git python-distribute python-pip=1.5.6-2
RUN curl -L https://github.com/rberrelleza/hiptsi/archive/v0.2.tar.gz | tar xvz
RUN mv hiptsi-0.2 hiptsi
RUN pip install virtualenv
RUN virtualenv venv
RUN venv/bin/pip install --upgrade pip==6.1.1
RUN venv/bin/pip install -r hiptsi/requirements.txt

EXPOSE 8080
VOLUME hiptsi/tenants.db
CMD venv/bin/python2.7 hiptsi/app.py
