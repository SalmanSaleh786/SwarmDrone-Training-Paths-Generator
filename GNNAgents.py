import util
from DFSAgents import CustomAgent
from game import Agent, Directions
from pacman import PacmanRules, GhostRules


class GNNAgents(Agent):
    def __init__(self, agentIdx):
        self.index = agentIdx
        self.stack = []
        self.visited = set()

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
            if agentPos[0]==x and agentPos[1]==y:
                return 'G'
        return ''
    def getAllNeighbours(self, maxY, maxX, agentPositions, fires, foods, walls, x, y):
        neighbours = []  # Use an empty list to store tuples
        # y row
        # x col
        if x > 0: #Right
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




    def getAction(self, state, data):
        global globalVisitedNodes  # Declare it as global inside the method
        gameStateData = state.data
        currPos = gameStateData.agentStates[self.index].configuration.pos
        fires = gameStateData.fire
        foods = gameStateData.food
        walls = gameStateData.layout.walls

        # for element in self.stack:
        #     if element.layoutText == 'G':
        #         element.layoutText = ''
        #
        # for element in self.stack:
        #      if any(agent.configuration.pos == element.neighPos for agent in gameStateData.agentStates):
        #          element.layoutText = 'G'

        allAgentPositions=[]
        for idx, agent in enumerate(gameStateData.agentStates):
            if idx != self.index:
                allAgentPositions.append(agent.configuration.pos)
            else:
                gameStateData.agentStates[self.index].Battery-=2
        if gameStateData.agentStates[self.index].Battery <=0:
            print("Stopping agent " + str(self.index))
            return Directions.STOP

        globalVisitedNodes.append(currPos)

        agent = CustomAgent(Directions.STOP, currPos, False, 'G')
        isVisited = agent.neighPos in self.visited
        if isVisited == False:
            agent.visited = True
            self.visited.add(agent.neighPos)
            neighbours = self.getAllNeighbours(gameStateData.layout.height, gameStateData.layout.width,
                                               allAgentPositions, fires, foods, walls, currPos[0], currPos[1])
            neighbours = self.getNewNeighbours(neighbours, self.visited)
            neighbours = self.choosePossibleNeighbour(agent, neighbours, state, self.index)
            if len(neighbours) > 0:
                for neighbor in neighbours:
                    if neighbor.neighPos not in self.visited:
                        self.stack.extend([agent, neighbor])
        if len(self.stack) > 0:
            newElement = self.stack.pop()
            if newElement.neighPos in allAgentPositions:
                newNeighbor=self.pickANewNeighbour(agent, state, allAgentPositions, fires, foods, walls, currPos)
                if newNeighbor!=None:
                    newElement=newNeighbor
                else:
                    return Directions.STOP

            validActions=[]
            if self.index == 0:
                validActions.extend(PacmanRules.getLegalActions(state))
            else:
                validActions.extend(GhostRules.getLegalActions(state, self.index))
            finalDir = self.getDirection(agent.neighPos, newElement.neighPos)
            if finalDir in validActions:
                return finalDir
        else:
            self.stack=[]
            self.visited=set()
        return Directions.STOP

    def pickANewNeighbour(self, agent, state, allAgentPositions, fires, foods, walls, currPos):
        neighbours = self.getAllNeighbours(state.data.layout.height, state.data.layout.width,
                                           allAgentPositions, fires, foods, walls, currPos[0], currPos[1])
        neighbours = self.choosePossibleNeighbour(agent, neighbours, state, self.index)
        #if len(neighbours)>0:
        return next((neighbour for neighbour in neighbours if neighbour.layoutText != 'G'), None)



    def isEveryElementVisited(self, stack, visitedStack):
        return all(element in visitedStack for element in stack)

    def getNewNeighbours(self, neighbours, visited):
        return [neighbour for neighbour in neighbours if neighbour.neighPos not in visited]

    def choosePossibleNeighbour(self, agent, neighbours, state, index):

        avoidArray = ['%', 'P', 'G']
        noObstacleNeighbours = []
        for neighbour in neighbours:
            if neighbour.layoutText not in avoidArray:
                noObstacleNeighbours.append(neighbour)
        legalDirections = None
        if index == 0:
            legalDirections = PacmanRules.getLegalActions(state)
        else:
            legalDirections = GhostRules.getLegalActions(state, index)
        finalOptions = []
        for neighbour in noObstacleNeighbours:
            isValidDir = any(self.getDirection(agent.neighPos, neighbour.neighPos) == legalDir
                             for legalDir in legalDirections)
            if isValidDir:
                finalOptions.append(neighbour)
        #random.shuffle(finalOptions)

        global globalVisitedNodes

        # Sort by whether neighPos is in globalVisitedNodes (visited nodes come first)
        finalOptions.sort(key=lambda n: n.neighPos not in globalVisitedNodes)

        finalOptions.sort(key=lambda n: '.' in n.layoutText)
        finalOptions.sort(key=lambda n: 'F' in n.layoutText)

        #if finalOptions.Last!='F' and finalOptions.Last!='.':


        return finalOptions

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()