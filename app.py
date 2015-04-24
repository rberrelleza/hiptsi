import os
import logging
from logging.handlers import RotatingFileHandler

import webapp2
from waitress import serve

from handlers import CapabilitiesHandler, WebhookHandler, InstallableHandler

application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=CapabilitiesHandler, methods=["GET"]),
    webapp2.Route(r'/webhook', handler=WebhookHandler, methods=["POST"]),
    webapp2.Route(r'/installable', handler=InstallableHandler, methods=["POST"]),
    webapp2.Route(r'/installable/<tenant_id>', handler=InstallableHandler, methods=["DELETE"])
], debug=True)


def main():
    for var in [WebhookHandler.JITSIURL_VAR, CapabilitiesHandler.BASEURL_VAR]:
        if var not in os.environ:
            raise Exception("{var} must be set in the environment".format(var=var))

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.DEBUG)

    data_location = os.environ.get("DATA_DIRECTORY", "/var/log/hiptsi")
    handler = RotatingFileHandler('{}/application.log'.format(data_location), maxBytes=30*1024*1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    serve(application, port='8080')

if __name__ == '__main__':
    main()
