from inspect import stack

from game import Agent
from game import Actions
from game import Directions
import random

from pacman import GhostRules, PacmanRules
from util import manhattanDistance
from collections import deque
import util


class CustomAgent():
    def __init__(self, direction, neighPos, visited, layoutText):
        self.direction = direction
        self.neighPos = neighPos

        self.visited = visited
        self.layoutText = layoutText
        # self.layoutRowCol = layoutRowCol

    # Check if an object with a specific element exists
    def exists_in_stack(self, stack, target_element):
        return any(obj.pos == target_element.pos for obj in stack)

    def find_index_in_stack(self, stack, target_element):
        for index, obj in enumerate(stack):
            if obj.pos == target_element.pos:
                return index  # Return the index when found
        return -1  # Return -1 if not found


import time


class DFSAgents(Agent):
    def __init__(self, agentIdx):
        self.index = agentIdx
        self.stack = []
        self.visited = set()
        # self.idx = 0

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
        if x > 0:  # LEFT
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
        if x < maxX - 1:  # RIGHT
            object = self.findObject(x + 1, y, walls, fires, foods, agentPositions)
            neighbours.append(CustomAgent(Directions.WEST, (x + 1, y), False,
                                          object))

        return neighbours

    def getAction(self, state):
        # time.sleep(1)
        # self.idx=self.idx+1
        gameStateData = state.data

        currPos = gameStateData.agentStates[self.index].configuration.pos
        # length = len(gameStateData.layout.layoutText)
        # currCol = int(currPos[0])
        # currRow = int(length - currPos[1] - 1)
        # currLayoutPos = (currRow, currCol)
        agent = gameStateData.agentStates[self.index]

        fires = gameStateData.fire
        foods = gameStateData.food
        walls = gameStateData.layout.walls
        allAgentPositions=[]
        for idx, agent in enumerate(gameStateData.agentStates):
            if idx != self.index:
                allAgentPositions.append(agent.configuration.pos)
        # allAgentPositions = [agent.configuration.pos and agent.index!=self.index for agent in gameStateData.agentStates]
        # gameStateData.layout.layoutText = self.updateLayoutText(agent, self.index, gameStateData.layout)
        agent = CustomAgent(Directions.STOP, currPos, False, 'P' if agent.isPacman else 'G')
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
                        self.stack.extend([agent.neighPos, neighbor.neighPos])
        if len(self.stack) > 0:
            newElement = self.stack.pop()
            # if any(agent1.configuration.pos == newElement for idx, agent1 in enumerate(gameStateData.agentStates)
            #        if idx != self.index):
            #     self.stack.pop()
            #     return Directions.STOP

            validActions=[]
            if self.index == 0:
                validActions.extend(PacmanRules.getLegalActions(state))
            else:
                validActions.extend(GhostRules.getLegalActions(state, self.index))

            finalDir = self.getDirection(agent.neighPos, newElement)
            if finalDir in validActions:
                return finalDir
            # self.stack.append(newElement)
        return Directions.STOP

    def isEveryElementVisited(self, stack, visitedStack):
        return all(element in visitedStack for element in stack)

    def getNewNeighbours(self, neighbours, visited):
        return [neighbour for neighbour in neighbours if neighbour.neighPos not in visited]

    # def updateLayoutText(self, agent, index, layoutText):
    #     length = len(layoutText)
    #     char_to_find = "P"
    #     # Find positions where the character appears
    #     positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]
    #
    #     layoutText = self.updateString(layoutText, positions[0][0], positions[0][1], ' ')
    #
    #     char_to_find = "G"
    #     positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]
    #     for pos in positions:
    #         layoutText = self.updateString(layoutText, pos[0], pos[1], ' ')
    #
    #     for agentState in agentStates:
    #         pos = agentState.configuration.pos
    #         currCol = int(pos[0])
    #         currRow = int(length - pos[1] - 1)
    #         layoutText = self.updateString(layoutText, currRow, currCol, "P" if agentState.isPacman else "G")
    #     return layoutText

    def updateString(self, layoutText, row_index, col_index, char):
        # Convert the row to a list of characters
        # row_index, col_index = positions[0]  # Get the first match
        row_as_list = list(layoutText[row_index])  # Convert string to list

        # Modify the character
        row_as_list[col_index] = char

        # Convert back to a string and update layoutText
        layoutText[row_index] = ''.join(row_as_list)

        return layoutText  # Updated text

    def getTotalFires(self, layoutText):
        char_to_find = "G"
        positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]
        return len(positions)

    # def getAllNeighbours(self, currPos, currLayoutPos, layout):
    #     neighbours = []  # Use an empty list to store tuples
    #
    #     length = len(layout.layoutText)
    #     currCol = int(currLayoutPos[1])
    #     currRow = int(currLayoutPos[0])
    #
    #     # length = len(layout.layoutText)
    #     # currRow = int(currPos[0])
    #     # currCol = int(currPos[1])
    #
    #     # (Directions.Stop, currPos, currLayoutPos, False)
    #     # Boundary checks before accessing indexes
    #     # Directions.STOP, currPos, (), False,  char,currLayoutPos
    #     if currCol > 0:  # LEFT
    #         neighbours.append(CustomAgent(Directions.WEST, (currPos[0] - 1, currPos[1]), currLayoutPos, False,
    #                                       layout.layoutText[currRow][currCol - 1], (currRow, currCol - 1)))
    #
    #     if currRow > 0:  # TOP
    #         neighbours.append(CustomAgent(Directions.NORTH, (currPos[0], currPos[1] - 1), currLayoutPos, False,
    #                                       layout.layoutText[currRow - 1][currCol], (currRow - 1, currCol)))
    #
    #     if currCol < len(layout.layoutText[currRow]) - 1:  # RIGHT
    #         neighbours.append(CustomAgent(Directions.EAST, (currPos[0] + 1, currPos[1]), currLayoutPos, False,
    #                                       layout.layoutText[currRow][currCol + 1], (currRow, currCol + 1)))
    #
    #     if currRow < length - 1:  # BOTTOM
    #         neighbours.append(CustomAgent(Directions.SOUTH, (currPos[0], currPos[1] + 1), currLayoutPos, False,
    #                                       layout.layoutText[currRow + 1][currCol], (currRow + 1, currCol)))
    #
    #     return neighbours

    # 0 - direction
    # 1 - LayoutText
    # 2 - Position
    # def getFireNeighbours(self, neighbours):
    #     filtered_neighbors = [n for n in neighbours if 'F' == n.layoutText]  # Store neighbors containing 'F'
    #     neighbors = [n for n in neighbours if 'F' != n.layoutText]  # Remove them from the original list
    #     return (filtered_neighbors, neighbors)
    import random
    def choosePossibleNeighbour(self, agent, neighbours, state, index):
        avoidArray = ['%', 'P', 'G']
        noObstacleNeighbours = []
        # alreadyVisited=[]
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
            isValidDir = any(self.getDirection(agent.neighPos, neighbour.neighPos) == legalDir for legalDir in legalDirections)
            if isValidDir:
                finalOptions.append(neighbour)
        # finalOptions.sort(key=lambda n: 'F' in n.layoutText)
        random.shuffle(finalOptions)
        return finalOptions
    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()
