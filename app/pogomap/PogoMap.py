#!/usr/bin/env python3
from .Response import Response
from .DBRequest import DBRequest
from .entities import Entity, Portal, Gym
import sqlalchemy
import time
import logging


class PogoMap:
	def __init__(self, db_host, db_user, db_pass, db_name):
		self.db = sqlalchemy.create_engine("postgresql://{}:{}@{}/{}".format(db_user,db_pass,db_host,db_name))
		self.wait_db()
		

	def wait_db(self):
		logging.info("Try to connect to db")
		while True:
			try:
				with self.db.connect() as connection:

					result = connection.execute('SELECT version()')

					logging.debug("db version: "+result.fetchone()[0])

				logging.info("Connected to db")
				return
				
			except (Exception):
				logging.info("Failed to connect to db. Will retry early...")
				time.sleep(1)
		
		logging.error("Failed to connect to db")

	@property
	def pokestops(self):
		with self.db.connect() as connection:
			result = connection.execute("SELECT * FROM pokestops")
			for r in result:
				yield Gym(r)

	@property
	def pokestops_eligible(self):
		with self.db.connect() as connection:
			result = connection.execute("SELECT * FROM pokestops_eligible")
			for r in result:
				yield Gym(r)

	@property
	def gyms(self):
		req = DBRequest(self.db, "gyms_eligible")
		for r in req.get():
			yield Gym(r)

	@property
	def gyms_eligible(self):
		req = DBRequest(self.db, "gyms_eligible")
		for r in req.get():
			yield Gym(r)

	def query(self, query):
		entities = None
		try:
			if query == "pokestops":
				entities = self.pokestops
			elif query == "pokestops_eligible":
				entities = self.pokestops_eligible
			elif query == "gyms":
				entities = self.gyms
			elif query == "gyms_eligible":
				entities = self.gyms_eligible
		except Exception:
			return Response(error="no")

		return Response(entities)