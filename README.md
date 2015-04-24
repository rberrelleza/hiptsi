# hiptsi
HipChat bot to start meet.jitsi.org meetings

##How to run:

- Create a /data directory in your docker-capablehost
- docker pull ramiro/hiptsi
- docker run -p 8080:8080 -e “HIPTSI_BASEURL=http://meet.jitsi.org" -v /root/data/hiptsi-tenants.db:/hiptsi/tenants.db -d hiptsi/0.1
