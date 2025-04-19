import util
from DFSAgents import CustomAgent
from game import Agent, Directions
from pacman import PacmanRules, GhostRules
from multiprocessing.connection import Listener, Client

import pickle
import struct
class GNNAgents(Agent):
    client = Client(('localhost', 6000), authkey=b'password')

    def __init__(self, agentIdx):
        print ('Creating GNN Agent')
        self.index = agentIdx
        self.stack = []
        self.visited = set()

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

    def getAction(self, state, data):
        gameStateData = state.data
        currPos = gameStateData.agentStates[self.index].configuration.pos
        GNNAgents.client.send(data)

        bytes_received = GNNAgents.client.recv_bytes()
        replyPos = pickle.loads(bytes_received)
        print("Received from server:", replyPos)
        return getattr(Directions, replyPos.upper(), Directions.STOP)

#        return Directions[replyPos]

    def recvall(sock, n):
        """Receive exactly n bytes from the socket"""
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()
