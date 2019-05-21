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
        logging.debug("Get entities {}".format(type))

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

    def set_entity(self, id, type, is_eligible):
        logging.info("Try to set entity {}".format(id))

        session = self.Session()
        with session.begin():

            there_is = True if session.execute(
                select([func.count()]).where(tables.entities.c.id == id)).scalar() == 1 else False

            if not there_is:
                if type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(tables.entities.insert().values(id=id, type=type, is_eligible=is_eligible))

                logging.info("Entity {} now is verified".format(id))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(GET_ENTITIES["verified"][0].c.id == id)).fetchone())

            elif there_is and type == "unverified":

                session.execute(tables.entities.delete().where(tables.entities.c.id == id))

                logging.info("Entity {} now is unverified".format(id))

                return GET_ENTITIES["unverified"][1](**session.execute(
                    GET_ENTITIES["unverified"][0].select().where(GET_ENTITIES["unverified"][0].c.id == id)).fetchone())

            elif there_is:
                if type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(tables.entities.update().where(tables.entities.c.id == id) \
                                .values(id=id, type=type, is_eligible=is_eligible))

                logging.info(
                    "Entity {} now is a {} {}".format(id, type, "eligible" if is_eligible else "not eligible"))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(GET_ENTITIES["verified"][0].c.id == id)).fetchone())

    def add_entities(self, *args, **kwargs):
        logging.info("Try to add entities")

        entities = []
        for a in args:
            if isinstance(a, (list,)):
                entities += a
            elif isinstance(a, (dict,)):
                entities.append(a)
            else:
                raise Exception()

        if len(kwargs) is not 0:
            entities += [{kwargs}]

        logging.info("{} possible new portals".format(len(entities)))

        session = self.Session()
        with session.begin():
            new_entities = []
            for e in entities:
                if session.execute(select([func.count()]).where(tables.portals.c.guid == e["guid"])).scalar() == 0:
                    new_entities.append(e)
                    logging.info("Discovered new portal {}".format(e["name"]))

            if len(new_entities) != 0:
                session.execute(tables.portals.insert(), new_entities)
                logging.info("Added {} new entities".format(len(new_entities)))

            else:
                logging.info("No new entities")
