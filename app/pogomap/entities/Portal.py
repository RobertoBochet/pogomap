#!/usr/bin/env python3
from . import Entity

class Portal(Entity):
	@property
	def type(self):
		return "portal"