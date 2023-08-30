"""
A shared state between all stages.
"""

from src.logic.animal import Elephant,Turtle,Gorilla,Porpoise,Orangutan,Leopards,Rhinos,Gazelle,Owl,Dove
from datetime import date
from random import randint

class State:
    def __init__(self):
        self.encounterTypeId = 1
        self.berryCounts = [0, 0, 0, 0, 0]
        self.analyzedAnimals = [
            # Elephant(None),
            # Turtle(None),
            # Gorilla(None),
            # Porpoise(None),
            # Orangutan(None),
            # Leopards(None),
            # Rhinos(None),
            # Gazelle(None),
            # Owl(None),
            # Dove(None)
        ]

        self.load = False
        self.area = "parrishHome"
        self.player_pos = [20, 25]
        self.player_facing = "down"
        self.playerID = str(randint(100000,999999))
        self.licenseDateStr = str(date.today())

BERRY_TYPES = ["berry-sweet", "berry-sour", "berry-blue", "berry-red", "berry-star"]
BERRY_NAMES = ["sweet berry", "sour berry", "blueberry", "strawberry", "star berry"]
