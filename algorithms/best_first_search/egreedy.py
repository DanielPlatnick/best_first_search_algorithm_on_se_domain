from generic_defs.search_engine import *
import heapq
import random

class GBFS(SearchEngine):
    """
    Greedy Best First Search algorithm
    """

    def __init__(self, w=1):
        super().__init__()
        self.open = []
        self.closed = []
        self.w = w

    def search(self, start, goal):
        self.open = [start]
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            self.number_of_expanded_nodes += 1
            if self.goal_test(current):
                self.path = self.reconstruct_path(current)
                self.actions = self.reconstruct_path_actions(current)
                self.visited = self.closed
                self.cost = current.g
                self.status = SearchStatus.TERMINATED
                return self.path, self.actions
            for action, child in self.transition_system(current):
                if child in self.closed:
                    continue
                if child not in self.open:
                    child.parent = current
                    child.action = action
                    child.g = self.cost_function(current, action)
                    self.open.append(child)
                else:
                    if child.g < current.g:
                        self.open.remove(child)
                        child.parent = current
                        child.action = action
                        child.g = self.cost_function(current, action)
                        self.open.append(child)
            
            # put the current fscore in the heap
            heapq.heapify(self.open)
            # get the lowest fscore from the heap
            self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (self.w * self.heuristic(x)))
        self.status = SearchStatus.TERMINATED
        return None

    def heuristic(self, node):
        self.heuristic(node)

    def reconstruct_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent

        path.append(current)
        return path[::-1]
    
    def reconstruct_path_actions(self, current):
        path = []
        while current.parent:
            path.append(current.action)
            current = current.parent
        return path[::-1]

class EGBFS(GBFS):
    """
    Epsilon Greedy Best First Search algorithm
    """

    def __init__(self, w=1, epsilon=0.1):
        super().__init__(w)
        self.epsilon = epsilon

    def search(self, start, goal):
        self.open = [start]
        self.closed = []
        while self.open:
            current = self.open.pop(0)
            self.closed.append(current)
            self.number_of_expanded_nodes += 1
            if self.goal_test(current):
                self.path = self.reconstruct_path(current)
                self.actions = self.reconstruct_path_actions(current)
                self.visited = self.closed
                self.cost = current.g
                self.status = SearchStatus.TERMINATED
                return self.path, self.actions
            for action, child in self.transition_system(current):
                if child in self.closed:
                    continue
                if child not in self.open:
                    child.parent = current
                    child.action = action
                    child.g = self.cost_function(current, action)
                    self.open.append(child)
                else:
                    if child.g < current.g:
                        self.open.remove(child)
                        child.parent = current
                        child.action = action
                        child.g = self.cost_function(current, action)
                        self.open.append(child)
            
            # put the current fscore in the heap
            heapq.heapify(self.open)
            # get the lowest fscore from the heap
            self.open = heapq.nsmallest(len(self.open), self.open, key=lambda x: (self.w * self.heuristic(x)))
            # epsilon greedy randomization
            if random.random() < self.epsilon:
                self.open = random.sample(self.open, len(self.open))
        self.status = SearchStatus.TERMINATED
        return None

    def heuristic(self, node):
        self.heuristic(node)

    def reconstruct_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent

        path.append(current)
        return path[::-1]
    
    def reconstruct_path_actions(self, current):
        path = []
        while current.parent:
            path.append(current.action)
            current = current.parent
        return path[::-1]