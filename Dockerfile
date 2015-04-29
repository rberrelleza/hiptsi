FROM ubuntu:utopic

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-dev curl git python-distribute python-pip=1.5.6-2
ADD /hiptsi /hiptsi
ADD app.py /app.py
ADD requirements.txt /requirements.txt
RUN pip install virtualenv
RUN virtualenv /hiptsi/venv
RUN /hiptsi/venv/bin/pip install --upgrade pip==6.1.1
RUN /hiptsi/venv/bin/pip install -r /requirements.txt

EXPOSE 8080
VOLUME /data
CMD /hiptsi/venv/bin/python /app.py
