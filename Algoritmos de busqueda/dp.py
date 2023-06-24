from search import SearchAlgorithm

class DynamicProgramming(SearchAlgorithm):
    def __init__(self, problem):
        self.fCosts = {}
        self.backrefs = {}
        self.futureQueue = [problem.endState()]
        self.currentState = problem.startState()
        self.finished = False

    def futureCosts(self):
        state = self.futureQueue.pop(0)

        if self.problem.isEnd(state):
            self.fCosts[state] = 0
            for _, previousState, _ in self.problem.successorsAndCosts(state):
                self.futureQueue.append(previousState)
        elif state not in self.fCosts:
            self.fCosts[state] = min(nextCost + self.fCosts[nextState] for nextState, nextCost in ((nextState, nextCost) for _, nextState, nextCost in self.problem.successorsAndCosts(state) if nextState not in self.fCosts))

    def stateCost(self, state):
        return self.fCosts.get(state, None)

    def step(self):
        if self.finished:
            path = []
            while self.currentState != self.problem.startState():
                action, prevState = self.backrefs[self.currentState]
                path.append(self.currentState)
                self.currentState = prevState
            path.reverse()
            return path

        self.futureCosts()

        if self.problem.isEnd(self.currentState):
            self.finished = True
            path = []
            while self.currentState != self.problem.startState():
                action, prevState = self.backrefs[self.currentState]
                path.append(self.currentState)
                self.currentState = prevState
            path.reverse()
            return path

        nextState = self.currentState
        for action, neighbour, _ in self.problem.successorsAndCosts(self.currentState):
            if neighbour not in self.fCosts:
                self.futureQueue.append(neighbour)
            elif self.fCosts[neighbour] < self.fCosts[nextState]:
                nextState = neighbour
                bestAction = action

        self.backrefs[nextState] = (bestAction, self.currentState)
        self.currentState = nextState
        path = []
        while self.currentState != self.problem.startState():
            action, prevState = self.backrefs[self.currentState]
            path.append(self.currentState)
            self.currentState = prevState
        path.reverse()
        return path