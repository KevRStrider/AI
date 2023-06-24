from search import SearchAlgorithm
import random


class Backtracking(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = []
        self.BestPath = None
        self.BestCost = float('inf')
        self.pastCosts[self.startState] = 0
        
        
    def stateCost(self, state):
        return self.pastCosts.get(state, None)

def step(self):
    problem = self.problem
    startState = self.startState
    frontier = self.frontier

    if not frontier and self.BestPath is None:
        frontier.append([0, [startState]])

    if not frontier:
        return self.BestPath

    cost, path = frontier.pop()
    lastState = path[-1]

    if problem.isEnd(lastState):
        if cost < self.BestCost:
            self.BestCost = cost
            self.BestPath = path
        return self.BestPath

    if self.BestPath != None and frontier == []:
        print(f'BestCost: {self.BestCost}, BestPath: {self.BestPath}')
        return self.BestPath

    for _, newState, newcost in problem.successorsAndCosts(lastState):
        if newState not in path:
            frontier.append([cost+newcost, path + [newState]])
            self.pastCosts[newState] = self.pastCosts[lastState] + newcost

    # Check if any of the new states are end states
    for _, newState, _ in problem.successorsAndCosts(lastState):
        if problem.isEnd(newState):
            if cost + newcost < self.BestCost:
                self.BestCost = cost + newcost
                self.BestPath = path + [newState]
    return path