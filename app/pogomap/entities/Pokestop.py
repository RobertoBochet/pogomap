#!/usr/bin/env python3
from .Entity import Entity

class Pokestop(Entity):
	@property
	def type(self):
		return "pokestop"