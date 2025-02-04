from game import Agent
from game import Actions
from game import Directions
import random

from pacman import GhostRules
from util import manhattanDistance
from collections import deque
import util


class DFSAgents(Agent):


    def __init__(self, agentIdx):
        self.index = agentIdx
        self.visited=[]

    def updateLayoutText(self, layoutText,agentStates):
        length = len(layoutText)
        char_to_find = "P"
        # Find positions where the character appears
        positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]

        layoutText=self.updateString(layoutText, positions[0][0], positions[0][1], '.')
        #layoutText[positions[0][0]][positions[0][1]] = '.'

        char_to_find = "G"
        positions = [(i, j) for i, word in enumerate(layoutText) for j, c in enumerate(word) if c == char_to_find]
        for pos in positions:
            layoutText=self.updateString(layoutText, pos[0], pos[1], '.')

        for agentState in agentStates:
            pos=agentState.configuration.pos
            currCol = int(pos[0])
            currRow = int(length - pos[1] - 1)
            layoutText=self.updateString(layoutText, currRow, currCol, "P" if agentState.isPacman else "G")

    def updateString(self, layoutText, row_index, col_index, char):
        # Convert the row to a list of characters
        #row_index, col_index = positions[0]  # Get the first match
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
    def getAction(self, state):
        gameStateData = state.data
        if self.getTotalFires(gameStateData.layout.layoutText)==0:
            print("GameOver!")

        currPos = gameStateData.agentStates[self.index].configuration.pos
        length = len(gameStateData.layout.layoutText)
        currCol = int(currPos[0])
        currRow = int(length - currPos[1] - 1)
        currPos=(currRow, currCol)

        self.updateLayoutText(gameStateData.layout.layoutText,
                              gameStateData.agentStates)

        if currPos not in self.visited:
            self.visited.append(currPos)

        neighbours = self.getNeighbours(currPos, gameStateData.layout)
        selectedDirection=self.chooseBestNeighbour(neighbours, gameStateData.layout)
        return selectedDirection

    def getNeighbours(self, currPos, layout):
        neighbours = []  # Use an empty list to store tuples

        length = len(layout.layoutText)
        currRow = int(currPos[0])
        currCol = int(currPos[1])

        # Boundary checks before accessing indexes
        if currCol > 0:  # LEFT
            neighbours.append((Directions.WEST, layout.layoutText[currRow][currCol - 1], (currRow, currCol-1)))

        if currRow > 0:  # TOP
            neighbours.append((Directions.NORTH, layout.layoutText[currRow - 1][currCol], (currRow-1, currCol)))

        if currCol < len(layout.layoutText[currRow]) - 1:  # RIGHT
            neighbours.append((Directions.EAST, layout.layoutText[currRow][currCol + 1], (currRow, currCol+1)))

        if currRow < length - 1:  # BOTTOM
            neighbours.append((Directions.SOUTH, layout.layoutText[currRow + 1][currCol], (currRow+1, currCol)))

        return neighbours


#0 - direction
    #1 - LayoutText
    #2 - Position
    def chooseBestNeighbour(self, neighbours, layout):
        # left, top, right, bottom
        fireFound = any(neighbour[1] == 'F' for neighbour in neighbours)
        if fireFound:
            for neighbour in neighbours:
                if neighbour[1]=='F':
                    return neighbour[0]
            #         layout.fire[neighbour[2][0]][neighbour[2][1]]=False;
            #         layout.layoutText=self.updateString(layout.layoutText,
            #                                             neighbour[2][0],
            #                                             neighbour[2][1],
            #                                             '.')
            #return Directions.STOP

        avoidArray = ['%', 'P', 'G']
        possibleOptions=[]
        alreadyVisited=[]
        for neighbour in neighbours:
            if neighbour[1] not in avoidArray and neighbour[2] not in self.visited:
                possibleOptions.append(neighbour)
            if neighbour[2] in self.visited and neighbour[1] not in avoidArray:
                alreadyVisited.append(neighbour)
        if len(possibleOptions)==0:
            if len(alreadyVisited)>0:
                possibleOptions=alreadyVisited
            else:
                return Directions.STOP

        choosenNeighbour=random.choice(possibleOptions)
        if choosenNeighbour[2] not in self.visited:
            self.visited.append(choosenNeighbour[2])
        return choosenNeighbour[0]


def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()
