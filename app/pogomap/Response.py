import simplejson
import logging

class Response:
	def __init__(self, entities=None, error=None):
		self.entities = entities
		self.error = error

	@property
	def json(self):
		response = {}

		if self.error != None:
			response["done"] = False
			response["error"] = self.error
		else:
			response["done"] = True
			response["entities"] = list(self.entities)

		return simplejson.dumps(response, for_json=True, sort_keys=True, indent=4 * ' ')