from DFSAgents import CustomAgent
from game import Agent, Directions


class GNNAgents(Agent):
    def __init__(self, agentIdx):
        self.index = agentIdx
        self.stack = []
        self.visited = set()#j

    # direction, neighPos, visited, layoutText
    def getDirection(self, agent, next):
        if agent[1] < next[1]:
            return Directions.NORTH
        if agent[1] > next[1]:
            return Directions.SOUTH
        if agent[0] < next[0]:
            return Directions.EAST
        if agent[0] > next[0]:
            return Directions.WEST
        return Directions.STOP

    def findObject(self, x, y, walls, fires, foods, agentPositions):
        if fires.data[x][y] == True:
            return 'F'
        if foods.data[x][y] == True:
            return '.'
        if walls.data[x][y] == True:
            return '%'
        for agentPos in agentPositions:
            if agentPos[0] == x and agentPos[1] == y:
                return 'G'
        return ''

    def getAllNeighbours(self, maxY, maxX, agentPositions, fires, foods, walls, x, y):
        neighbours = []  # Use an empty list to store tuples
        # y row
        # x col
        if x > 0:  # Right
            object = self.findObject(x - 1, y, walls, fires, foods, agentPositions)
            neighbours.append(CustomAgent(Directions.EAST, (x - 1, y), False,
                                          object))

        if y > 0:  # Bottom
            object = self.findObject(x, y - 1, walls, fires, foods, agentPositions)
            neighbours.append(CustomAgent(Directions.SOUTH, (x, y - 1), False,
                                          object))

        if y < maxY - 1:  # Top
            object = self.findObject(x, y + 1, walls, fires, foods, agentPositions)
            neighbours.append(CustomAgent(Directions.NORTH, (x, y + 1), False,
                                          object))
        if x < maxX - 1:  # Left
            object = self.findObject(x + 1, y, walls, fires, foods, agentPositions)
            neighbours.append(CustomAgent(Directions.WEST, (x + 1, y), False,
                                          object))

        return neighbours

    def getAction(self, state):
        return