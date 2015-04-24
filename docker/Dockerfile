FROM ubuntu:utopic

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-dev curl git python-distribute python-pip=1.5.6-2
RUN curl -L https://github.com/rberrelleza/hiptsi/archive/v0.2.tar.gz | tar xvz
RUN mv hiptsi-0.2 /hiptsi
RUN pip install virtualenv
RUN virtualenv /hiptsi/venv
RUN /hiptsi/venv/bin/pip install --upgrade pip==6.1.1
RUN /hiptsi/venv/bin/pip install -r /hiptsi/requirements.txt

EXPOSE 8080
VOLUME /data
CMD /hiptsi/venv/bin/python /hiptsi/app.py
