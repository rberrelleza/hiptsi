import json
import logging
import hashlib
import os

import requests
from requests.auth import HTTPBasicAuth

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from hiptsi import application

logger = logging.getLogger(__name__)
logger.info("Using DB {}".format(application.config["hiptsi"]["mysql_connection"]))

engine = create_engine(application.config["hiptsi"]["mysql_connection"], echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"

    tenantId = Column(String(1000), primary_key=True)
    oauthSecret = Column(String(1000))
    group = Column(Integer)
    room = Column(Integer, nullable=True)
    apiUrl = Column(String(1000))
    tokenUrl = Column(String(1000))

    def __init__(self, tenantId, oauthSecret, group, room, apiUrl, tokenUrl):
        self.tenantId = tenantId
        self.oauthSecret = oauthSecret
        self.group = group
        self.room = room
        self.apiUrl = apiUrl
        self.tokenUrl = tokenUrl

    def _getToken(self, scopes):
        if len(scopes) == 0:
            raise ValueError("At least one scope is required")

        body = dict(grant_type="client_credentials", scope=" ".join(scopes))
        response = requests.post(self.tokenUrl, auth=HTTPBasicAuth(self.tenantId, self.oauthSecret), data=body)
        response.raise_for_status()
        tokenData = response.json()
        logger.debug("tokenData {}".format(tokenData))
        return tokenData["access_token"]

    def sendNotification(self, room_id, message):
        token = self._getToken(["send_notification"])
        resourceUrl = "{}/room/{}/notification".format(self.apiUrl, room_id)
        response = requests.post(
            resourceUrl,
            data=json.dumps({"message": message}),
            headers={"Authorization": "Bearer {token}".format(token=token), "Content-Type": "application/json"})

        response.raise_for_status()

Base.metadata.create_all(engine)

class TenantStore(object):

    @classmethod
    def create(cls, body):
        logger.info("Creating tenant")
        capabilitiesUrl = body["capabilitiesUrl"]
        response = requests.get(capabilitiesUrl)
        response.raise_for_status()
        capabilities = response.json()
        apiUrl = capabilities["links"]["api"]
        tokenUrl = capabilities["capabilities"]["oauth2Provider"]["tokenUrl"]

        tenant = Tenant(
            tenantId=body["oauthId"],
            oauthSecret=body["oauthSecret"],
            group=body.get("groupId"),
            room=body.get("roomId"),
            apiUrl=apiUrl,
            tokenUrl=tokenUrl)

        session = Session()
        try:
            session.add(tenant)
            session.commit()
            logger.info("Created tenant {}".format(tenant.tenantId))
            return tenant
        finally:
            session.close()

    @classmethod
    def get(cls, tenantId):
        logger.debug("Retrieving tenant {}".format(tenantId))

        session = Session()
        try:
            return session.query(Tenant).filter(
                Tenant.tenantId == tenantId).first()
        except DoesNotExist as ex:
            logging.error(ex)
            raise ValueError("Tenant {} doesn't exist".format(tenantId))
        finally:
            session.close()

    @classmethod
    def delete(cls, tenantId):
        session = Session()
        logger.info("Deleting tenant {}".format(tenantId))

        try:
            tenant = TenantStore.get(tenantId)
            session.delete(tenant)
            session.commit()
            logger.info("Deleted tenant {}".format(tenantId))
        except ValueError:
            logger.info("Tenant {} doesn't exist".format(tenantId))
        finally:
            session.close()
