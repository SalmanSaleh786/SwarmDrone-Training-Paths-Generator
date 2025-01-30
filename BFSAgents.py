from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
from collections import deque
import util

class BFSAgents( Agent ):
    def __init__( self, agentIdx):
        self.index = agentIdx
        self.queue=[]
        self.visited=[]

    def getAction( self):
        return None
        #get neighbours of current node,
        # add neighbours in the queue
        # get best possible neighbor and choose its direction
    #    if self.queue:
            # Dequeue the current node
    #        node = queue.popleft()
   #         print(node)

            # Enqueue unvisited neighbors
    #        for neighbor in graph[node]:
    #            if neighbor not in visited:
    #                visited.add(neighbor)
    #                queue.append(neighbor)
    #    return Directions.STOP
    def getNeighbours(self, currPos):

        return None

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()