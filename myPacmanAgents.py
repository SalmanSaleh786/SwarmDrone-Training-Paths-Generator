# myPacmanAgents.py

from pacman import Directions
from game import Agent

class MyPacmanAgent(Agent):

    def getAction(self, state):
        return Directions.STOP


