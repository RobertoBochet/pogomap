import logging
import time
from typing import List, Union

import geopy.distance
from sqlalchemy import *
from sqlalchemy.exc import OperationalError
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

            except OperationalError:
                self.logger.info("Failed to connect to db. Will retry early...")
                time.sleep(1)

        self.logger.error("Failed to connect to db")

    def get_entities(self, entity_type):
        self.logger.debug("Get entities {}".format(entity_type))

        if entity_type not in GET_ENTITIES:
            raise InvalidEntity()

        session = self.Session()
        with session.begin():
            for r in session.execute(GET_ENTITIES[entity_type][0].select()).fetchall():
                yield GET_ENTITIES[entity_type][1](**r)

    def is_editor_key_valid(self, key):
        session = self.Session()
        with session.begin():
            return True if session.execute(select([func.count()]).where(
                tables.editor_keys.c.key == key)).scalar() == 1 else False

    def set_entity(self, entity_id, entity_type, is_eligible):
        self.logger.info("Try to set entity {}".format(entity_id))

        session = self.Session()
        with session.begin():

            there_is = True if session.execute(
                select([func.count()]).where(tables.entities.c.id == entity_id)).scalar() == 1 else False

            if not there_is:
                if entity_type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(
                    tables.entities.insert().values(id=entity_id, type=entity_type, is_eligible=is_eligible))

                self.logger.info("Entity {} now is verified".format(entity_id))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(
                        GET_ENTITIES["verified"][0].c.id == entity_id)).fetchone())

            elif there_is and entity_type == "unverified":

                session.execute(tables.entities.delete().where(tables.entities.c.id == entity_id))

                self.logger.info("Entity {} now is unverified".format(entity_id))

                return GET_ENTITIES["unverified"][1](**session.execute(
                    GET_ENTITIES["unverified"][0].select().where(
                        GET_ENTITIES["unverified"][0].c.id == entity_id)).fetchone())

            elif there_is:
                if entity_type not in ["portal", "pokestop", "gym"]:
                    raise InvalidEntity()

                session.execute(
                    tables.entities.update().where(tables.entities.c.id == entity_id).values(id=entity_id,
                                                                                             type=entity_type,
                                                                                             is_eligible=is_eligible))

                self.logger.info(
                    "Entity {} now is a {} {}".format(entity_id, entity_type,
                                                      "eligible" if is_eligible else "not eligible"))

                return GET_ENTITIES["verified"][1](**session.execute(
                    GET_ENTITIES["verified"][0].select().where(
                        GET_ENTITIES["verified"][0].c.id == entity_id)).fetchone())

    def add_entities(self, *args, **kwargs) -> List[Portal]:
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

        portals: List[Portal] = []
        for e in entities:
            portals.append(Portal(**e, id=0))

        self.logger.info("{} possible new portals".format(len(portals)))

        session = self.Session()
        with session.begin():
            new_portals = []
            for p in portals:
                # Check if the portal is already in the db yet
                if session.execute(select([func.count()])
                                           .where(tables.portals.c.name == p.name)
                                           .where(tables.portals.c.latitude == p.latitude)
                                           .where(tables.portals.c.longitude == p.longitude)).scalar() != 0:
                    continue

                # Create the where clause to find similar portal
                where = or_(
                    tables.portals.c.name == p.name,
                    and_(
                        tables.portals.c.latitude == p.latitude,
                        tables.portals.c.longitude == p.longitude
                    ))
                # If the portal has a image use also it to find similar portal
                if p.image != "":
                    where = or_(where,
                                tables.portals.c.image == "//" + p.image.split("//")[1])

                similar_id = []
                # Search similar entities in the db
                for r in session.execute(tables.portals.select().where(where)).fetchall():
                    # Manages different position
                    # Updates if the name and the image are the same or the name is the same and positions are close
                    if r["latitude"] != p.latitude or r["longitude"] != p.longitude:
                        if r["name"] == p.name:
                            if r["image"] == "//" + p.image.split("//")[1] or geopy.distance.vincenty(
                                    (r["latitude"], r["longitude"]),
                                    (p.latitude, p.longitude)
                            ).km < 0.2:
                                similar_id.append(r["id"])

                    # Manages different name
                    # Updates if position or image are the same
                    elif r["name"] != p.name:
                        if r["image"] == "//" + p.image.split("//")[1] or (
                                r["latitude"] == p.latitude and r["longitude"] == p.longitude):
                            similar_id.append(r["id"])

                    # Manages different image
                    # Updates if position and name are the same
                    elif r["image"] != "//" + p.image.split("//")[1]:
                        if r["name"] == p.name and (
                                r["latitude"] == p.latitude and r["longitude"] == p.longitude):
                            similar_id.append(r["id"])

                # If there is a only one similar entity, updates it
                if len(similar_id) == 1:
                    session.execute(tables.portals.update().where(tables.portals.c.id == similar_id[0])
                                    .values(name=p.name,
                                            latitude=p.latitude,
                                            longitude=p.longitude,
                                            image=p.image))
                    self.logger.info("Entity {} updated".format(p.name))

                # If there is not a similar entity, prepare for addition
                elif len(similar_id) == 0:
                    new_portals.append(p)

                # Log conflict
                else:
                    self.logger.warning("Found a conflict in the db")

            if len(new_portals) != 0:

                for p in new_portals:
                    # Add the discovered entities to the db
                    session.execute(tables.portals.insert(), p.__dict__)

                    # Discover the id that was assigned to the portal
                    result = session.execute(tables.portals.select()
                                             .where(tables.portals.c.name == p.name)
                                             .where(tables.portals.c.latitude == p.latitude)
                                             .where(tables.portals.c.longitude == p.longitude)
                                             ).fetchone()
                    p.id = result["id"]

                    self.logger.info("New portal {} was added".format(p.name))

                self.logger.info("Added {} new entities".format(len(new_portals)))

                return new_portals

            else:
                self.logger.info("No new entities")
                return []

    def remove_entities(self, *args: Union[List[int], int]):
        self.logger.info("Try to remove entities")

        entities = []
        # Validates the entities provided
        for a in args:
            if isinstance(a, list):
                entities += a
            elif isinstance(a, int):
                entities.append(a)
            else:
                raise ValueError("The method requires a list of id")

        self.logger.info("{} entities are wanted to delete".format(len(entities)))

        session = self.Session()
        with session.begin():
            for e in entities:
                # Check if the portal is already in the db yet
                self.logger.debug(str(tables.portals.delete().where(tables.portals.c.id == e)))
                session.execute(tables.portals.delete().where(tables.portals.c.id == e))

                self.logger.info("Portal {} was deleted".format(e))
