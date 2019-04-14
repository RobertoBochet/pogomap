#!/usr/bin/env python3
from .Portal import Portal
from .Pokestop import Pokestop
from .Gym import Gym

def mkentity(data):
	if data["type"] == "portal":
		return Portal(data)
	elif data["type"] == "pokestop":
		return Pokestop(data)
	elif data["type"] == "gym":
		return Gym(data)