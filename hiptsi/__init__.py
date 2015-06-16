import logging
import os
from logging.handlers import RotatingFileHandler

import webapp2
from webapp2_extras import config as webapp2_config

def setupLogging(log_directory):
    format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format)
    logging.basicConfig(level=logging.DEBUG, format=format)
    handler = RotatingFileHandler(os.path.join(log_directory, 'application.log'), maxBytes=30*1024*1024, backupCount=5)
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)


application_config = {
    "hiptsi": {
        "public_url": os.environ.get("HIPTSI_PUBLICURL", "http://localhost:8080"),
        "jitsi_url": os.environ.get("HIPTSI_JITSIURL", "https://meet.jitsi.org"),
        "mysql_connection": os.environ.get("HIPTSI_MYSQL", "sqlite:///tenants.db"),
        "logs": os.environ.get("HIPTSI_LOGS", "."),
        "port": int(os.environ.get("HIPTSI_PORT", "8080"))
    }
}

setupLogging(application_config["hiptsi"]["logs"])

application = webapp2.WSGIApplication(routes=[
    webapp2.Route(r'', handler="hiptsi.handlers.CapabilitiesHandler", methods=["GET"]),
    webapp2.Route(r'/', handler="hiptsi.handlers.CapabilitiesHandler", methods=["GET"]),
    webapp2.Route(r'/webhook', handler="hiptsi.handlers.WebhookHandler", methods=["POST"]),
    webapp2.Route(r'/installable', handler="hiptsi.handlers.InstallableHandler", methods=["POST"]),
    webapp2.Route(r'/installable/<tenantId>', handler="hiptsi.handlers.InstallableHandler", methods=["DELETE"])
], config=application_config)


for var in application.config["hiptsi"]:
    if application.config["hiptsi"][var] is None:
        raise Exception("{var} must be set in the environment".format(var=var))

# Imported last so they can import the application once it's being loaded
from . import tenant, handlers
