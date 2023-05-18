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
    def maxValue(self, state, depth):
        if state.isWinningState() or state.isLosingState() or depth == self.depth:
            return state.getScore()

        v = float("-inf")

        for action in state.getPossibleActions():
            successor_state = state.generateNextState(state, action)
            v = max(v, self.expectValue(successor_state, depth + 1))
        return v

    def expectValue(self, state, depth):
        if state.isWinningState() or state.isLosingState():
            return state.getScore()
        v = 0
        actions = state.getPossibleActions()
        p = 1.0 / len(actions)  # Uniform probability for each action
        for action in actions:
            successor_state = state.generateNextState(state, action)
            v += p * self.maxValue(successor_state, depth)
        return v

    def getAction(self, gameState):
        best_action = None
        best_score = float("-inf")
        for action in gameState.getPossibleActions():
            successor_state = gameState.generateNextState(gameState, action)
            score = self.expectValue(successor_state, 0)
            if score > best_score:
                best_score = score
                best_action = action

        return best_action
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (exercise 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
