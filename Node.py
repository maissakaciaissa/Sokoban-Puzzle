import numpy as np
from math import inf

class Node:
    def __init__(self, sokobanPuzzle, parent=None, action="", g=1):
        self.state = sokobanPuzzle  
        self.parent = parent
        self.action = action
        self.g = g if parent is None else parent.g + g
        self.depth = 0 if parent is None else parent.depth + 1
        self.moves = "" if parent is None else parent.moves + action
        self.tab_stat = self.state.grid

    def costHeur(self, heuristique):
        """Calculates the cost based on the selected heuristic."""
        return self.f(heuristique)  # Assuming f() computes the cost
    def get_path(self):
        """Returns a list of states representing the path from the initial state to the current node."""
        path = []
        node = self
        while node is not None:
            path.append(node.state.grid)  # Use the current state grid instead of tab_dyn
            node = node.parent
        return path[::-1]  # Return the path from initial state to goal

    def f(self, heuristic=1): 
        """Calculates the cost of the current node using the selected heuristic."""
        heuristics = {
            1: self.heuristic1(),
            2: self.heuristic2(),
            3: self.heuristic3()
        }
        return self.g + heuristics[heuristic]  # Total cost = g + heuristic

    def heuristic1(self):
        """First heuristic: Number of left storage cells."""
        tab_stat = self.tab_stat  # Use instance variable instead of class variable
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')  # Storage indices
        
        left_storage = len(S_indices_x)  # Total storage cells
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.state.grid[ind_x][ind_y] == 'B':  # If occupied by a box
                left_storage -= 1

        return left_storage

    def heuristic2(self):
        """Second heuristic: 2 * Number of left storage + Min Manhattan distance to storage goals."""
        tab_stat = self.tab_stat  # Use instance variable instead of class variable
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')
        tab_dyn = np.array(self.state.grid)  # Current dynamic state
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')

        sum_distance = 0
        storage_left = len(S_indices_x)
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            min_distance = inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)
                if distance == 0: storage_left -= 1  # If box is on storage
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        
        return sum_distance + 2 * storage_left

    def heuristic3(self):
        """Third heuristic: Min Manhattan distances from blocks to storage + robot to blocks + 2 * Number of left storage."""
        tab_stat = self.tab_stat  # Use instance variable instead of class variable
        S_indices_x, S_indices_y = np.where(tab_stat == 'S')
        tab_dyn = np.array(self.state.grid)  # Current dynamic state
        B_indices_x, B_indices_y = np.where(tab_dyn == 'B')

        sum_distance = 0
        storage_left = len(S_indices_x)
        min_distance_br = inf
        
        for b_ind_x, b_ind_y in zip(B_indices_x, B_indices_y):
            # Distance from box to robot
            distance_br = abs(b_ind_x - self.state.robot_position[0]) + abs(b_ind_y - self.state.robot_position[1])
            if distance_br < min_distance_br:
                min_distance_br = distance_br

            # Distance from box to nearest storage
            min_distance = inf
            for s_ind_x, s_ind_y in zip(S_indices_x, S_indices_y):
                distance = abs(b_ind_x - s_ind_x) + abs(b_ind_y - s_ind_y)
                if distance == 0: storage_left -= 1  # If box is on storage
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
            
        return sum_distance + min_distance_br + 2 * storage_left
    def get_solution(self):  # Line 93
     """Returns the solution to the search problem as a list of moves."""  # Indented
     node = self
     solution = []
     while node:
        solution.append(node.action)  # Store action leading to this node
        node = node.parent
     return solution[::-1]  # Reverse to get actions from start to goal
