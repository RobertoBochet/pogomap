#!/usr/bin/env python3

class Entity:
	def __init__(self, data):
		self.data = data

	@property
	def id(self):
		return self.data["id"]
	@property
	def name(self):
		return self.data["name"]
	@property
	def latitude(self):
		return self.data["latitude"]
	@property
	def longitude(self):
		return self.data["longitude"]
	@property
	def guid(self):
		return self.data["guid"]
	@property
	def type(self):
		return self.data["type"]
	