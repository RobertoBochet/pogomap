#!/usr/bin/env python3
from .Entity import Entity
from .Portal import Portal
from .Pokestop import Pokestop
from .Gym import Gym

def mkentity(data):
	if not "type" in data:
		return Entity(data)
	if data["type"] == "portal":
		return Portal(data)
	elif data["type"] == "pokestop":
		return Pokestop(data)
	elif data["type"] == "gym":
		return Gym(data)