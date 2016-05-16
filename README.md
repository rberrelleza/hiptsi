# hiptsi
HipChat bot to start meet.jitsi.org meetings

##How to run as a docker container:
- docker run --name hiptsi-mongo -d mongo
- docker built -t ramiro/hiptsi .
- docker run --name hiptsi  --link hiptsi-mongo:mongo -p 5000:5000  -e NODE_ENV="production" -e LOCAL_BASE_URL="https://FQDN" -e PORT=5000 -e JITSI_ENV="https://meet.jitsi.org" ramiro/hiptsi

In order to be able to test the bot with hipchat.com or your hipchat server, I recommend you look into https://ngrok.com/ so it's exposed via the internet.
