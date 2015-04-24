import json
import os
import logging
import sys
import uuid

import jinja2
import webapp2

from hiptsi import application
from tenant import Tenant, TenantStore

logger = logging.getLogger("waitress.handlers")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class CapabilitiesHandler(webapp2.RequestHandler):

    def get(self):
        logger.debug("GET CapabilitiesHandler")
        template = JINJA_ENVIRONMENT.get_template('capabilities.json')

        pattern = r'(?i)^r?\\/jitsi'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(template.render(dict(base_url=application.config["hiptsi"]["public_url"], pattern=pattern)))


class WebhookHandler(webapp2.RequestHandler):

    def get(self):
        logger.debug("GET WebhookHandler")
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, WebhookHandler!')

    def post(self):
        logger.debug("POST WebhookHandler")
        body = json.loads(self.request.body)
        event = body.get("event")
        tenant_id = body.get("oauth_client_id")
        message = body.get("item")["message"]["message"]
        room_name= body.get("item")["room"]["name"]
        room_id= body.get("item")["room"]["id"]
        user_name= body.get("item")["message"]["from"]["name"]

        tenant = TenantStore.get_tenant(tenant_id)

        if message.startswith("/jitsi"):
            url = "{}/{}".format(application.config["hiptsi"]["jitsi_url"], self.random_name(room_name))
            response = "{} has started a Jitsi Meet. <a href={}>Click here to join<a>.".format(user_name, url)
        else:
            response = "Sorry, I didn't understand your command"

        tenant.send_notification(room_id, response)
        self.response.status = 204

    def random_name(self, room_name):
        return "{}{}".format(room_name.replace(" ", ""), str(uuid.uuid4()).replace("-", ""))


class InstallableHandler(webapp2.RequestHandler):

    def post(self):
        logger.debug("POST InstallableHandler")

        try:
            logger.info("Installing addon for: {}".format(self.request.body))
            body = json.loads(self.request.body)
            tenant = TenantStore.create_tenant(body)
            logger.info("Installed {}".format(tenant.tenant_id))
            self.response.status = 204
        except Exception as ex:
            logger.error("Error {} {}".format(self.request.body, ex))
            self.response.status = 500

    def delete(self, tenant_id):
        logger.debug("DELETE InstallableHandler")
        logger.info("Uninstalling {}".format(tenant_id))
        TenantStore.delete_tenant(tenant_id)
        self.response.status = 204
