#!/usr/bin/env python3
from .entities import Entity, Portal, Gym
import psycopg2
import time


class PogoMap:
	def __init__(self, db_host, db_port, db_user, db_pass, db_name):
		self.db = psycopg2.connect(
			host=db_host,
			port=db_port,
			user=db_user,
			password=db_pass,
			dbname=db_name)
		self.wait_db()

	def wait_db(self):
		while True:
			try:
				cur = self.db.cursor()
				
				cur.execute('SELECT version()')

				db_version = cur.fetchone()
				print(db_version)
				cur.close()
				break
			except (Exception, psycopg2.DatabaseError):
				time.sleep(1)

	@property
	def gyms(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM gyms")
		for r in cursor:
			yield Gym(r)

	@property
	def gyms_eligible(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM _eligible")
		for r in cursor:
			yield Gym(r)
