class DBRequest:
	def __init__(self, db, target):
		self.db = db
		self.target = target

	def get(self):
		with self.db.connect() as connection:
			result = connection.execute("SELECT * FROM {}".format(self.target))
			for r in result:
				yield dict(r)
