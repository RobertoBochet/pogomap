import logging
import time

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker

from . import tables
from .DBRequest import DBRequest
from .entities import *
from .exceptions import *


class PogoMap:
    def __init__(self, db_host, db_user, db_pass, db_name):
        self.db = sqlalchemy.create_engine("postgresql://{}:{}@{}/{}".format(db_user, db_pass, db_host, db_name))
        self.Session = sessionmaker(bind=self.db, autocommit=True)
        self.wait_db()

        self.VALID_ENTITIES = [
            "unverified",
            "verified",
            "not_in_pogo",
            "in_pogo",
            "portals",
            "pokestops",
            "pokestops_eligible",
            "gyms",
            "gyms_eligible"
        ]
        self.GET_ENTITIES = {
            "unverified": self.get_unverified,
            "verified": self.get_verified,
            "not_in_pogo": self.get_not_in_pogo,
            "in_pogo": self.get_in_pogo,
            "portals": self.get_portals,
            "pokestops": self.get_pokestops,
            "pokestops_eligible": self.get_pokestops_eligible,
            "gyms": self.get_gyms,
            "gyms_eligible": self.get_gyms_eligible
        }

    def wait_db(self):
        logging.info("Try to connect to db")
        while True:
            try:
                with self.db.connect() as connection:

                    result = connection.execute('SELECT version()')

                    logging.debug("db version: " + result.fetchone()[0])

                logging.info("Connected to db")
                return

            except (Exception):
                logging.info("Failed to connect to db. Will retry early...")
                time.sleep(1)

        logging.error("Failed to connect to db")

    def get_unverified(self):
        req = DBRequest(self.db, "unverified")
        for r in req.get():
            yield Unverified(**r)

    def get_verified(self):
        req = DBRequest(self.db, "verified")
        for r in req.get():
            yield Entity(**r)

    def get_not_in_pogo(self):
        req = DBRequest(self.db, "not_in_pogo")
        for r in req.get():
            yield Portal(**r)

    def get_in_pogo(self):
        req = DBRequest(self.db, "in_pogo")
        for r in req.get():
            yield Entity(**r)

    def get_portals(self):
        req = DBRequest(self.db, "portals")
        for r in req.get():
            yield Portal(**r)

    def get_portals_eligible(self):
        req = DBRequest(self.db, "portals_eligible")
        for r in req.get():
            yield Portal(**r)

    def get_pokestops(self):
        req = DBRequest(self.db, "pokestops")
        for r in req.get():
            yield Pokestop(**r)

    def get_pokestops_eligible(self):
        req = DBRequest(self.db, "pokestops_eligible")
        for r in req.get():
            yield Pokestop(**r)

    def get_gyms(self):
        req = DBRequest(self.db, "gyms")
        for r in req.get():
            yield Gym(**r)

    def get_gyms_eligible(self):
        req = DBRequest(self.db, "gyms_eligible")
        for r in req.get():
            yield Gym(**r)

    def get_entities(self, type):
        logging.info("Get entities {}".format(type))

        if not type in self.GET_ENTITIES:
            raise InvalidEntity()

        return self.GET_ENTITIES[type]()

    def is_editor_key_valid(self, key):
        session = self.Session()
        with session.begin():
            return session.query(session.query(tables.EditorKey).filter(tables.EditorKey.key == key).exists()).scalar()
