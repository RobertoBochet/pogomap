#!/usr/bin/env python3
from ..entities import Entity

class Gym(Entity):
	
	@property
	def type(self):
		return "gym"