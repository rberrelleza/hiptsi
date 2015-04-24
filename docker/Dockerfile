FROM ubuntu:utopic

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-dev curl git python-distribute python-pip=1.5.6-2
RUN curl -L https://github.com/rberrelleza/hiptsi/archive/0.1.tar.gz | tar xvz
RUN mv hiptsi-0.1 hiptsi
RUN pip install virtualenv
RUN virtualenv env
RUN env/bin/pip install --upgrade pip==1.5.6
RUN env/bin/pip install -r hiptsi/requirements.txt

EXPOSE 8080
VOLUME hiptsi/tenants.db
CMD env/bin/python2.7 hiptsi/app.py
