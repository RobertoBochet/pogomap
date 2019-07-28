import logging
import time

import geopy.distance
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
    def __init__(self, pg_host: str = "127.0.0.1", pg_user: str = "postgres", pg_pass: str = "",
                 pg_db_name: str = "pogomap"):
        # Retrieves a logger
        self.logger = logging.getLogger(__name__)

        self.db = create_engine("postgresql://{}:{}@{}/{}".format(pg_user, pg_pass, pg_host, pg_db_name))
        self.Session = sessionmaker(bind=self.db, autocommit=True)
        self.wait_db()

    def wait_db(self):
        self.logger.info("Try to connect to db")
        while True:
            try:
                with self.db.connect() as connection:

                    result = connection.execute('SELECT version()')

                    self.logger.debug("db version: " + result.fetchone()[0])

                self.logger.info("Connected to db")
                return

            except (Exception):
                self.logger.info("Failed to connect to db. Will retry early...")
                time.sleep(1)

        self.logger.error("Failed to connect to db")

    def get_entities(self, type):
        self.logger.debug("Get entities {}".format(type))

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
        self.logger.info("Try to set entity {}".format(id))

        session = self.Session()
        with session.begin():

            there_is = True if session.execute(
                select([func.count()]).where(tables.entities.c.id == id)).scalar() == 1 else False

            if not there_is:
                if type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(tables.entities.insert().values(id=id, type=type, is_eligible=is_eligible))

                self.logger.info("Entity {} now is verified".format(id))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(GET_ENTITIES["verified"][0].c.id == id)).fetchone())

            elif there_is and type == "unverified":

                session.execute(tables.entities.delete().where(tables.entities.c.id == id))

                self.logger.info("Entity {} now is unverified".format(id))

                return GET_ENTITIES["unverified"][1](**session.execute(
                    GET_ENTITIES["unverified"][0].select().where(GET_ENTITIES["unverified"][0].c.id == id)).fetchone())

            elif there_is:
                if type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(tables.entities.update().where(tables.entities.c.id == id) \
                                .values(id=id, type=type, is_eligible=is_eligible))

                self.logger.info(
                    "Entity {} now is a {} {}".format(id, type, "eligible" if is_eligible else "not eligible"))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(GET_ENTITIES["verified"][0].c.id == id)).fetchone())

    def add_entities(self, *args, **kwargs):
        self.logger.info("Try to add entities")

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

        self.logger.info("{} possible new portals".format(len(entities)))

        session = self.Session()
        with session.begin():
            new_entities = []
            for e in entities:
                # Check if the portal is already in the db yet
                if session.execute(select([func.count()])
                                           .where(tables.portals.c.name == e["name"])
                                           .where(tables.portals.c.latitude == e["latitude"])
                                           .where(tables.portals.c.longitude == e["longitude"])).scalar() != 0:
                    continue

                similar_id = []

                # Search similar entities in the db
                for r in session.execute(tables.portals.select().where(
                        or_(
                            tables.portals.c.name == e["name"],
                            and_(
                                tables.portals.c.latitude == e["latitude"],
                                tables.portals.c.longitude == e["longitude"]
                            ),
                            tables.portals.c.image == "//" + e["image"].split("//")[1]
                        ))
                ).fetchall():
                    # Manages different position
                    # Updates if the name and the image are the same or the name is the same and positions are close
                    if r["latitude"] != e["latitude"] or r["longitude"] != e["longitude"]:
                        if r["name"] == e["name"]:
                            if r["image"] == "//" + e["image"].split("//")[1] or geopy.distance.vincenty(
                                    (r["latitude"], r["longitude"]),
                                    (e["latitude"], e["longitude"])
                            ).km < 0.2:
                                similar_id.append(r["id"])

                    # Manages different name
                    # Updates if position or image are the same
                    elif r["name"] != e["name"]:
                        if r["image"] == "//" + e["image"].split("//")[1] or (
                                r["latitude"] == e["latitude"] and r["longitude"] == e["longitude"]):
                            similar_id.append(r["id"])

                    # Manages different image
                    # Updates if position and name are the same
                    elif r["image"] != "//" + e["image"].split("//")[1]:
                        if r["name"] == e["name"] and (
                                r["latitude"] == e["latitude"] and r["longitude"] == e["longitude"]):
                            similar_id.append(r["id"])

                # If there is a only one similar entity, updates it
                if len(similar_id) == 1:
                    session.execute(tables.portals.update().where(tables.portals.c.id == similar_id[0])
                                    .values(name=e["name"],
                                            latitude=e["latitude"],
                                            longitude=e["longitude"],
                                            image=e["image"]))
                    self.logger.info("Entity {} updated".format(e["name"]))

                # If there is not a similar entity, prepare for addition
                elif len(similar_id) == 0:
                    new_entities.append(e)
                    self.logger.info("Discovered new portal {}".format(e["name"]))

                # Log conflict
                else:
                    self.logger.warning("Found a conflict in the db")

            # Add the discovered entities to the db
            if len(new_entities) != 0:
                session.execute(tables.portals.insert(), new_entities)
                self.logger.info("Added {} new entities".format(len(new_entities)))

            else:
                self.logger.info("No new entities")
