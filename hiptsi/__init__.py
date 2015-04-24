import os
import webapp2
from webapp2_extras import config as webapp2_config

application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler="hiptsi.handlers.CapabilitiesHandler", methods=["GET"]),
    webapp2.Route(r'/webhook', handler="hiptsi.handlers.WebhookHandler", methods=["POST"]),
    webapp2.Route(r'/installable', handler="hiptsi.handlers.InstallableHandler", methods=["POST"]),
    webapp2.Route(r'/installable/<tenant_id>', handler="hiptsi.handlers.InstallableHandler", methods=["DELETE"])
], debug=True)

application_config = {
    "hiptsi": {
        "public_url": os.environ.get("HIPTSI_PUBLICURL", "http://localhost:8080"),
        "jitsi_url": os.environ.get("HIPTSI_JITSIURL", "http://meet.jitsi.org"),
        "data_directory": os.environ.get("HIPTSI_DATADIRECTORY", "."),
        "port": int(os.environ.get("HIPTSI_PORT", "8080"))
    }
}

application.config = webapp2_config.Config(application_config)

for var in application.config["hiptsi"]:
    if application.config["hiptsi"][var] is None:
        raise Exception("{var} must be set in the environment".format(var=var))

# Imported last so they can import the application once it's being loaded
from . import tenant, handlers
