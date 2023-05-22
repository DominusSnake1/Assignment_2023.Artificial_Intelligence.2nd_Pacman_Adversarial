# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def maxValue(self, state, depth):
        if state.isWinningState() or state.isLosingState() or depth == self.depth: return self.evaluationFunction(state)

        v = float("-inf")

        for possibleAction in state.getPossibleActions(0):
            successor = state.generateNextState(0, possibleAction)
            v = max(v, self.minValue(successor, depth, 1))
        return v

    def minValue(self, state, depth, agentIndex):
        if state.isWinningState() or state.isLosingState(): return self.evaluationFunction(state)

        v = float("inf")
        numberOfAgents = state.getNumAgents()

        if agentIndex == numberOfAgents: return self.maxValue(state, depth + 1)

        for possibleAction in state.getPossibleActions(agentIndex):
            successor = state.generateNextState(agentIndex, possibleAction)
            v = min(v, self.minValue(successor, depth, agentIndex + 1))
        return v

    def getAction(self, gameState):
        legalActions = gameState.getPossibleActions(0)

        scores = []
        for action in legalActions:
            scores.append(self.minValue(gameState.generateNextState(0, action), 0, 1))
        bestScore = max(scores)

        bestIndices = []
        for index in range(len(scores)):
            if scores[index] == bestScore: bestIndices.append(index)

        randomIndex = random.choice(bestIndices)

        return legalActions[randomIndex]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):

    def maxValue(self, state, agentIndex, depth, a, b):
        if state.isWinningState() or state.isLosingState() or depth == self.depth: return self.evaluationFunction(state)

        v = float('-inf')
        possibleActions = state.getPossibleActions(agentIndex)

        for action in possibleActions:
            successor = state.generateNextState(agentIndex, action)
            v = max(v, self.minValue(successor, agentIndex + 1, depth, a, b))

            if v > b: return v

            a = max(a, v)
        return v

    def minValue(self, state, agentIndex, depth, a, b):
        if state.isWinningState() or state.isLosingState(): return self.evaluationFunction(state)

        v = float('inf')
        possibleActions = state.getPossibleActions(agentIndex)

        for action in possibleActions:
            successor = state.generateNextState(agentIndex, action)
            numberOfAgents = state.getNumAgents()

            if agentIndex == numberOfAgents - 1:
                v = min(v, self.maxValue(successor, 0, depth + 1, a, b))
            else:
                v = min(v, self.minValue(successor, agentIndex + 1, depth, a, b))

            if v < a: return v

            b = min(b, v)
        return v

    def getAction(self, gameState):
        bestAction = None
        bestValue = float('-inf')
        a = float('-inf')
        b = float('inf')

        possibleActions = gameState.getPossibleActions(0)

        for action in possibleActions:
            successor = gameState.generateNextState(0, action)
            value = self.minValue(successor, 1, 0, a, b)

            if value > bestValue:
                bestValue = value
                bestAction = action
            a = max(a, bestValue)
        return bestAction
        # util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    def maxValue(self, agentIndex, depth, state):
        if depth == 0 or state.isWinningState() or state.isLosingState(): return self.evaluationFunction(state)

        v = float('-inf')
        bestAction = None
        possibleActions = state.getPossibleActions(agentIndex)

        for action in possibleActions:
            successor = state.generateNextState(agentIndex, action)
            score = self.expectValue(1, depth, successor)

            if score > v:
                v = score
                bestAction = action

        if depth == self.depth:
            return bestAction

        return v

    def expectValue(self, agentIndex, depth, state):
        if depth == 0 or state.isWinningState() or state.isLosingState(): return self.evaluationFunction(state)

        v = 0
        numberOfAgents = state.getNumAgents()
        possibleActions = state.getPossibleActions(agentIndex)
        p = 1 / len(possibleActions)

        for action in possibleActions:
            successor = state.generateNextState(agentIndex, action)

            if agentIndex == numberOfAgents - 1:
                score = p * self.maxValue(0, depth - 1, successor)
            else:
                score = p * self.expectValue(agentIndex + 1, depth, successor)

            v += score

        return v

    def getAction(self, gameState):
        return self.maxValue(0, self.depth, gameState)
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    score = currentGameState.getScore()
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostAgents = range(1, currentGameState.getNumAgents())
    ghostDistances = []

    for ghost in ghostAgents:
        ghostState = currentGameState.getGhostState(ghost)
        ghostPos = ghostState.getPosition()
        distance = manhattanDistance(pacmanPosition, ghostPos)
        ghostDistances.append(distance)

    closestGhostDistance = min(ghostDistances)

    threateningGhosts = 0
    for distance in ghostDistances:
        if distance <= 2: threateningGhosts += 1

    evaluation = score - closestGhostDistance - threateningGhosts

    return evaluation

    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
