#!/usr/bin/env python3
import mysql.connector
from .entities import Entity,Portal,Gym

class PogoMap:
	def __init__(self,db_host,db_user,db_pass,db_name):
		self.db = mysql.connector.connect(
			host = db_host,
			user = db_user,
			passwd = db_pass,
			database = db_name
		)

	@property
	def gyms(self):
		cursor = self.db.cursor()
		cursor.execute(f"SELECT * FROM gyms")
		for r in cursor:
			yield Gym(r)

