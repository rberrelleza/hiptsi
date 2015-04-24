import json
import hashlib
import logging
import os

import requests
from requests.auth import HTTPBasicAuth

from peewee import Model, SqliteDatabase, CharField, DoesNotExist

TENANT_DATABASE_VAR = "DATABASE_PATH"
TENANT_DATABASE = os.environ.get(TENANT_DATABASE_VAR, "tenants.db")
db = SqliteDatabase(TENANT_DATABASE)


class Tenant(Model):
    tenant_id = CharField(unique=True, primary_key=True)
    oauthSecret = CharField()
    group = CharField()
    room = CharField(null=True)
    apiUrl = CharField()
    tokenUrl = CharField()

    class Meta:
        database = db

    def get_token(self, scopes):
        if len(scopes) == 0:
            raise ValueError("At least one scope is required")

        body = dict(grant_type="client_credentials", scope=" ".join(scopes))
        response = requests.post(self.tokenUrl, auth=HTTPBasicAuth(self.tenant_id, self.oauthSecret), data=body)
        response.raise_for_status()
        tokenData = response.json()
        return tokenData["access_token"]

    def send_notification(self, room_id, message):
        token = self.get_token(["send_notification"])
        resourceUrl = "{}/room/{}/notification".format(self.apiUrl, room_id)
        response = requests.post(
            resourceUrl,
            data=json.dumps({"message": message}),
            headers={"Authorization": "Bearer {token}".format(token=token), "Content-Type": "application/json"})

        response.raise_for_status()


class TenantStore(object):

    db.create_tables([Tenant], True)

    @classmethod
    def create_tenant(cls, body):
        capabilitiesUrl = body["capabilitiesUrl"]
        response = requests.get(capabilitiesUrl)
        response.raise_for_status()
        capabilities = response.json()
        apiUrl = capabilities["links"]["api"]
        tokenUrl = capabilities["capabilities"]["oauth2Provider"]["tokenUrl"]

        tenant = Tenant.create(
            tenant_id=body["oauthId"],
            oauthSecret=body["oauthSecret"],
            group=body.get("groupId"),
            room=body.get("roomId"),
            apiUrl=apiUrl,
            tokenUrl=tokenUrl)

        inserted = TenantStore.get_tenant(body["oauthId"])

        return tenant

    @classmethod
    def get_tenant(cls, tenant_id):
        logging.info("Retrieving tenant {}".format(tenant_id))

        try:
            return Tenant.select().where(Tenant.tenant_id == tenant_id).get()
        except DoesNotExist as ex:
            logging.error(ex)
            raise ValueError("Tenant {} doesn't exist".format(tenant_id))

    @classmethod
    def delete_tenant(cls, tenant_id):
        tenant = TenantStore.get_tenant(tenant_id)
        if tenant:
            logging.info("Deleting tenant {}".format(tenant_id))
            tenant.delete_instance()
        else:
            logging.info("Tenant {} doesn't exist".format(tenant_id))
