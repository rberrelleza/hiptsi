import json
import logging
import os
import sys
import uuid

import jinja2
import webapp2

from tenant import Tenant, TenantStore

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HomeHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class CapabilitiesHandler(webapp2.RequestHandler):
    BASEURL_VAR = "HIPTSI_BASEURL"

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('capabilities.json')

        pattern = r'(?i)^r?\\/jitsi'

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(template.render(dict(base_url=os.environ[self.BASEURL_VAR], pattern=pattern)))


class WebhookHandler(webapp2.RequestHandler):
    JITSIURL_VAR = "JITSI_URL"
    COMMANDS = ["/jitsi"]

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, WebhookHandler!')

    def post(self):
        body = json.loads(self.request.body)
        event = body.get("event")
        tenant_id = body.get("oauth_client_id")
        message = body.get("item")["message"]["message"]
        room_name= body.get("item")["room"]["name"]
        user_name= body.get("item")["message"]["from"]["name"]

        tenant = TenantStore.get_tenant(tenant_id)

        if message.startswith("/jitsi"):
            url = "{}/{}".format(os.environ[self.JITSIURL_VAR], self.random_room(room_name))
            response = "{} has started a Jitsi Meet. <a href={}>Click here to join<a>.".format(user_name, url)
        else:
            response = "Sorry, I didn't understand your command"

        tenant.send_notification(room_id, response)
        self.response.status = 204

    def random_name(room_name):
        return "{}-{}".format(room_name.replace(" ", ""), uuid.uuid4())

class InstallableHandler(webapp2.RequestHandler):

    def post(self):
        body = json.loads(self.request.body)
        tenant = TenantStore.create_tenant(body)
        logging.info("Installed {}".format(tenant.tenant_id))
        self.response.status = 204

    def delete(self, tenant_id):
        logging.info("Uninstalling {}".format(tenant_id))
        TenantStore.delete_tenant(tenant_id)
        self.response.status = 204
