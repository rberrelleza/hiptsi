import os
import logging

import webapp2
from waitress import serve

from handlers import HomeHandler, CapabilitiesHandler, WebhookHandler, InstallableHandler

application = webapp2.WSGIApplication([
    webapp2.Route(r'/addon/capabilities', handler=CapabilitiesHandler, methods=["GET"]),
    webapp2.Route(r'/addon/webhook', handler=WebhookHandler, methods=["POST"]),
    webapp2.Route(r'/addon/installable', handler=InstallableHandler, methods=["POST"]),
    webapp2.Route(r'/addon/installable/<tenant_id>', handler=InstallableHandler, methods=["DELETE"])
], debug=True)


def main():
    for var in [WebhookHandler.JITSIURL_VAR, CapabilitiesHandler.BASEURL_VAR]:
        if var not in os.environ:
            raise Exception("{var} must be set in the environment".format(var=var))

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.DEBUG)
    serve(application, port='8080')

if __name__ == '__main__':
    main()
