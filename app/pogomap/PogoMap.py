#!/usr/bin/env python3
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
	def gyms(self):
		with self.db.connect() as connection:
			result = connection.execute("SELECT * FROM gyms")
			for r in result:
				yield Gym(r)

	@property
	def gyms_eligible(self):
		with self.db.connect() as connection:
			result = connection.execute("SELECT * FROM gyms_eligible")
			for r in result:
				yield Gym(r)

	def respose_gyms(self):
		respose = {}
		respose["status"] = True
		respose[""]