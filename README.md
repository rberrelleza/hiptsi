# hiptsi
HipChat bot to start meet.jitsi.org meetings

##How to run on a VM:
- virtualenv venv
- venv/bin/pip install -r requirements.txt
- JITSI_URL=http://meet.jitsi.org HIPTSI_BASEURL=http://localhost:8080 venv/bin/python app.py

##How to run as a docker container:
- Create a /data directory in your docker-capablehost
- docker pull ramiro/hiptsi
- docker run -p 8080:8080 -e “HIPTSI_BASEURL=http://meet.jitsi.org" -e "HIPTSI_BASEURL=http://localhost:8080" -e "DATA_DIRECTORY=/data" -v /data/hiptsi:/data -d ramiro/hiptsi

In order to be able to test the bot with hipchat.com or your hipchat server, I recommend you look into https://ngrok.com/ so it's exposed via the internet.
