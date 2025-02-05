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
    def __init__(self, direction, pos, neighbours, visited, layoutText, layoutRowCol):
        self.direction = direction
        self.pos = pos
        self.neighbours = neighbours
        self.visited = visited
        self.layoutText = layoutText
        self.layoutRowCol = layoutRowCol

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
        self.visited = []

    def getAction(self, state):
        #time.sleep(1)
        gameStateData = state.data
        gameStateData.layout.layoutText = self.updateLayoutText(gameStateData.layout.layoutText,
                                                                gameStateData.agentStates)

        currPos = gameStateData.agentStates[self.index].configuration.pos
        # height = len(gameStateData.layout.layoutText)
        # maxY = height - 1
        # layoutChar = gameStateData.layout.layoutText[maxY - currPos[1]][currPos[0]]
        # if layoutChar!='P':
        #     print("p not found")
        # for y in range(self.height):
        #    for x in range(self.width):
        #        layoutChar = layoutText[maxY - y][x]


        length = len(gameStateData.layout.layoutText)
        currCol = int(currPos[0])
        currRow = int(length - currPos[1] - 1)
        currLayoutPos = (currRow, currCol)
        char = gameStateData.layout.layoutText[currRow][currCol]

        agent = None
        if len(self.stack) > 0:
            agent = self.stack.pop()
        else:
            agent = CustomAgent(Directions.STOP, currPos, (), False, char, currLayoutPos)

        # if agent.exists_in_stack(self.stack, agent):
        #     idx = agent.find_index_in_stack(self.stack, agent)
        #     if idx>-1:
        #         self.stack[idx]=agent
        # else:
        #     self.stack.append(agent)

        isVisited = agent.visited
        self.visited.append(currLayoutPos)
        if isVisited == False:
            agent.visited = True

            neighbours = self.getAllNeighbours(currPos, currLayoutPos, gameStateData.layout)
            neighbours = self.getNewNeighbours(neighbours, self.visited)
            neighbours = self.choosePossibleNeighbour(neighbours, state)
            for neighbor in neighbours:
                if not neighbor.visited:
                    self.stack.append(neighbor)
        return self.stack.pop().direction
    # while len(self.stack) != 0:
    #     currentAgent = self.stack.pop()
    #

    # self.updateLayoutText(gameStateData.layout.layoutText,
    #                       gameStateData.agentStates)
    #
    # if currPos not in self.visited:
    #     self.visited.append(currPos)
    #

    # selectedDirection=self.chooseBestNeighbour(neighbours, gameStateData.layout)
    # return selectedDirection


    def getNewNeighbours(self, neighbours, visited):
        return [neighbour for neighbour in neighbours if neighbour.layoutRowCol not in visited]


    def updateLayoutText(self, layoutText, agentStates):


        length = len(layoutText)
        char_to_find = "P"
        # Find positions where the character appears
        positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]

        layoutText = self.updateString(layoutText, positions[0][0], positions[0][1], ' ')

        char_to_find = "G"
        positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]
        for pos in positions:
            layoutText = self.updateString(layoutText, pos[0], pos[1], ' ')

        for agentState in agentStates:
            pos = agentState.configuration.pos
            currCol = int(pos[0])
            currRow = int(length - pos[1] - 1)
            layoutText = self.updateString(layoutText, currRow, currCol, "P" if agentState.isPacman else "G")
        return layoutText


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


    def getAllNeighbours(self, currPos, currLayoutPos, layout):
        neighbours = []  # Use an empty list to store tuples

        length = len(layout.layoutText)
        currCol = int(currLayoutPos[1])
        currRow = int(currLayoutPos[0])


        # length = len(layout.layoutText)
        # currRow = int(currPos[0])
        # currCol = int(currPos[1])

        # (Directions.Stop, currPos, currLayoutPos, False)
        # Boundary checks before accessing indexes
        # Directions.STOP, currPos, (), False,  char,currLayoutPos
        if currCol > 0:  # LEFT
            neighbours.append(CustomAgent(Directions.WEST, (currPos[0] - 1, currPos[1]), (), False,
                                          layout.layoutText[currRow][currCol - 1], (currRow, currCol - 1)))

        if currRow > 0:  # TOP
            neighbours.append(CustomAgent(Directions.NORTH, (currPos[0], currPos[1] - 1), (), False,
                                          layout.layoutText[currRow - 1][currCol], (currRow - 1, currCol)))

        if currCol < len(layout.layoutText[currRow]) - 1:  # RIGHT
            neighbours.append(CustomAgent(Directions.EAST, (currPos[0] + 1, currPos[1]), (), False,
                                          layout.layoutText[currRow][currCol + 1], (currRow, currCol + 1)))

        if currRow < length - 1:  # BOTTOM
            neighbours.append(CustomAgent(Directions.SOUTH, (currPos[0], currPos[1] + 1), (), False,
                                          layout.layoutText[currRow + 1][currCol], (currRow + 1, currCol)))

        return neighbours


    # 0 - direction
    # 1 - LayoutText
    # 2 - Position
    def choosePossibleNeighbour(self, neighbours, state):
        # left, top, right, bottom
        # fireFound = any(neighbour[1] == 'F' for neighbour in neighbours)
        # if fireFound:
        #     for neighbour in neighbours:
        #         if neighbour[1]=='F':
        #             return neighbour[0]
        #         layout.fire[neighbour[2][0]][neighbour[2][1]]=False;
        #         layout.layoutText=self.updateString(layout.layoutText,
        #                                             neighbour[2][0],
        #                                             neighbour[2][1],
        #                                             '.')
        # return Directions.STOP

        avoidArray = ['%', 'P', 'G']
        noObstacleNeighbours = []
        # alreadyVisited=[]
        for neighbour in neighbours:
            if neighbour.layoutText not in avoidArray:
                noObstacleNeighbours.append(neighbour)
        legalDirections=PacmanRules.getLegalActions(state)
        finalOptions=[]
        for neighbour in noObstacleNeighbours:
            dir=neighbour.direction
            isValidDir = any(neighbour.direction == dir for legalDir in legalDirections)
            if isValidDir:
                finalOptions.append(neighbour)
        return finalOptions
        #     if neighbour[2] in self.visited and neighbour[1] not in avoidArray:
        #         alreadyVisited.append(neighbour)
        # if len(possibleOptions)==0:
        #     if len(alreadyVisited)>0:
        #         possibleOptions=alreadyVisited
        #     else:
        #         return Directions.STOP
        #
        # choosenNeighbour=random.choice(possibleOptions)
        # if choosenNeighbour[2] not in self.visited:
        #     self.visited.append(choosenNeighbour[2])
        # return choosenNeighbour[0]


    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()
