import os
import logging

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
    logger.setLevel(logging.INFO)

    logger = logging.getLogger("pewee")
    logger.setLevel(logging.INFO)

    logging.basicConfig(filename='hiptsi.log',level=logging.DEBUG)
    serve(application, port='8080')

if __name__ == '__main__':
    main()
