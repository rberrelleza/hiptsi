import json
import os
import logging
import sys
import uuid

import jinja2
import webapp2

from hiptsi import application
from tenant import Tenant, TenantStore

logger = logging.getLogger(__name__)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def send_notification(tenantId, roomId, userName, roomName):
    tenant = TenantStore.get(tenantId)
    random_name = "{}{}".format(roomName.replace(" ", ""), str(uuid.uuid4()).replace("-", ""))
    url = "{}/{}".format(application.config["hiptsi"]["jitsi_url"], random_name)
    response = "{} has started a video conference. <a href={}>Click here to join<a>.".format(userName, url)
    tenant.sendNotification(roomId, response)

class CapabilitiesHandler(webapp2.RequestHandler):

    def get(self):
        logger.debug("GET CapabilitiesHandler")
        template = JINJA_ENVIRONMENT.get_template('capabilities.json')

        pattern = r'(?i)^r?\\/jitsi'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(template.render(dict(base_url=application.config["hiptsi"]["public_url"], pattern=pattern)))


class WebhookHandler(webapp2.RequestHandler):

    def post(self):
        logger.debug("POST WebhookHandler")
        body = json.loads(self.request.body)
        event = body.get("event")
        tenantId = body.get("oauth_client_id")
        message = body.get("item")["message"]["message"]
        roomName= body.get("item")["room"]["name"]
        roomId= body.get("item")["room"]["id"]
        userName= body.get("item")["message"]["from"]["name"]

        tenant = TenantStore.get(tenantId)

        if message.startswith("/video"):
            send_notification(tenantId, roomId, userName, roomName)
        else:
            response = "Sorry, I didn't understand your command"

        self.response.status = 204

    def random_name(self, roomName):
        return "{}{}".format(roomName.replace(" ", ""), str(uuid.uuid4()).replace("-", ""))

class StartVideoHandler(webapp2.RequestHandler):

    def get(self):
        logger.debug("GET StartVideoHandler")
        template = JINJA_ENVIRONMENT.get_template('start.json')
        self.response.write(template.render(dict(base_url=application.config["hiptsi"]["public_url"])))

    def post(self):
        logger.debug("POST StartVideo")
        body = json.loads(self.request.body)
        tenantId = body.get("oauth_client_id")
        message = body.get("item")["message"]["message"]
        roomName= body.get("item")["room"]["name"]
        roomId= body.get("item")["room"]["id"]
        userName= body.get("item")["message"]["from"]["name"]

        send_notification(tenantId, roomId, userName, roomName)
        self.response.status = 204

class InstallableHandler(webapp2.RequestHandler):

    def post(self):
        logger.debug("POST InstallableHandler")

        try:
            logger.info("Installing addon for: {}-{}".format(
                self.request.json.get("groupId"), self.request.json.get("roomId")))
            body = json.loads(self.request.body)
            tenant = TenantStore.create(body)
            logger.info("Installed {}".format(tenant.tenantId))
            self.response.status = 204
        except Exception as ex:
            logger.error("Error {} {}".format(self.request.body, ex))
            self.response.status = 500

    def delete(self, tenantId):
        logger.debug("DELETE InstallableHandler")
        logger.info("Uninstalling {}".format(tenantId))
        TenantStore.delete(tenantId)
        self.response.status = 204
