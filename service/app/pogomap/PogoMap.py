import logging
import time

from sqlalchemy import *
from sqlalchemy.orm.session import sessionmaker

from . import tables
from .entities import *
from .exceptions import *

GET_ENTITIES = {
    "unverified": (tables.unverified, Unverified),
    "verified": (tables.verified, Entity),
    "not_in_pogo": (tables.not_in_pogo, Portal),
    "in_pogo": (tables.in_pogo, Entity),
    "portals": (tables.portals, Portal),
    "pokestops": (tables.pokestops, Pokestop),
    "pokestops_eligible": (tables.pokestops_eligible, Pokestop),
    "gyms": (tables.gyms, Gym),
    "gyms_eligible": (tables.gyms_eligible, Gym)
}


class PogoMap:
    def __init__(self, db_host, db_user, db_pass, db_name):
        self.db = create_engine("postgresql://{}:{}@{}/{}".format(db_user, db_pass, db_host, db_name))
        self.Session = sessionmaker(bind=self.db, autocommit=True)
        self.wait_db()

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

    def get_entities(self, type):
        logging.info("Get entities {}".format(type))

        if not type in GET_ENTITIES:
            raise InvalidEntity()

        session = self.Session()
        with session.begin():
            for r in session.execute(GET_ENTITIES[type][0].select()).fetchall():
                yield GET_ENTITIES[type][1](**r)

    def is_editor_key_valid(self, key):
        session = self.Session()
        with session.begin():
            return True if session.execute(select([func.count()]).where(
                tables.editor_keys.c.key == key)).scalar() == 1 else False
