#!/usr/bin/env python3
from .Entity import Entity

class Portal(Entity):
	@property
	def type(self):
		return "portal"