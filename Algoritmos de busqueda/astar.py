from search import SearchAlgorithm
from pq import PriorityQueue
import math

class AStar(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = PriorityQueue()
        self.backrefs = {}
        self.endState = problem.endState()
        self.frontier.update(self.startState, 0.0)

    def stateCost(self, state):
        return self.pastCosts.get(state, None)

    def path(self, state):
        path = []
        while state != self.startState:
            _, prevState = self.backrefs[state]
            path.append(state)
            state = prevState
        path.reverse()
        return path

    def heuristic(self, state):
        return math.sqrt((state[0] - self.endState[0])**2 + (state[1] - self.endState[1])**2)

    def step(self):
        if self.actions:
            return self.path(self.endState)

        state, pastCost = self.frontier.removeMin()
        if state is None or pastCost is None:
            return []

        self.pastCosts[state] = pastCost
        self.numStatesExplored += 1
        path = self.path(state)

        if self.problem.isEnd(state):
            self.actions = []
            while state != self.startState:
                action, prevState = self.backrefs[state]
                self.actions.append(action)
                state = prevState
            self.actions.reverse()
            self.pathCost = pastCost
            return path

        for action, newState, cost in self.problem.successorsAndCosts(state):
            newCost = pastCost + cost + self.heuristic(newState)
            if self.frontier.update(newState, newCost):
                self.backrefs[newState] = (action, state)

        return path
