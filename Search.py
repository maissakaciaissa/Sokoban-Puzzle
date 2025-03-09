from Node import *
from collections import deque
from tkinter import *

class Search:  # Search class

    @staticmethod  # BFS search algorithm 
    def breadthFirst(initial_node):  # initial_node is a Node object representing the initial state of the puzzle
        
        # Check if the start element is the goal
        if initial_node.state.is_goal(Node.tab_stat):  # Corrected method name
            return initial_node, 0  # Return the initial node and the number of nodes expanded

        # Create the OPEN FIFO queue and the CLOSED list
        open = deque([initial_node])  # A FIFO queue of Node objects
        closed = []  # A list of Node objects 
        
        step = 0  # Number of nodes expanded
        while True:  # Loop until the goal is found or the OPEN queue is empty
            step += 1  # Increment the number of nodes expanded
            
            # Check if the OPEN queue is empty => goal not found 
            if len(open) == 0:  # If the OPEN queue is empty
                return None, -1  # Return None and -1
            
            # Get the first element of the OPEN queue
            current = open.popleft()  # current is a Node object
            closed.append(current)  # current is a Node object                    

            # Generate the successors of the current node
            succ = current.succ()  # Ensure this is a deque
            for child in succ:  # Use a for loop to iterate over successors
                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.tab_dyn not in [n.state.tab_dyn for n in closed] and 
                    child.state.tab_dyn not in [n.state.tab_dyn for n in open]): 

                    # Put the child in the OPEN queue 
                    open.append(child)  # child is a Node object  

                    # Check if the child is the goal
                    if child.state.is_goal(Node.tab_stat):  # Corrected method name
                        return child, step  # Return the child node and the number of nodes expanded 

    @staticmethod  # A* algorithm
    def Astar(init_node, heuristique=1):
        # Check if the start element is the goal
        if init_node.state.is_goal():  # Call without the grid argument
            return init_node, 0  # Return the initial node and the number of nodes expanded

        init_node.costHeur(heuristique)
        # Create the OPEN priority queue and the CLOSED list
        open = deque([init_node])  # A priority queue of Node objects
        closed = list()  # A list of Node objects
        step = 0

        while True:  # Loop until the goal is found or the OPEN queue is empty
            step += 1  # Increment the number of nodes expanded
            
            # Check if the OPEN queue is empty => goal not found
            if len(open) == 0:  # If the OPEN queue is empty
                return None, -1  # Return None and -1
            
            # Sort the open list by the f value
            open = deque(sorted(list(open), key=lambda node: node.f(heuristique)))

            # Get the first element of the OPEN queue
            current = open.popleft()  # current is a Node object

            # Put the current node in the CLOSED list
            closed.append(current)  # current is a Node object

            # Check if the current node is the goal
            if current.state.is_goal():  # Use current state's grid for checking
                return current, step  # Return the current node and the number of nodes expanded
            
            # Generate the successors of the current node
            succ = current.succ()  # Assuming succ() returns a list of Node objects
            while len(succ) != 0:  # Loop until the successors list is empty
                child = succ.popleft()  # child is a Node object
                child.costHeur(heuristique)

                # Check if the child is not in the OPEN queue
                if child.state.tab_dyn in [node.state.tab_dyn for node in open]:
                    index = [node.state.tab_dyn for node in open].index(child.state.tab_dyn)
                    if child.f(heuristique) < open[index].f(heuristique):
                        open[index] = child
                # Check if the child is not in CLOSED list
                elif child.state.tab_dyn not in [node.state.tab_dyn for node in closed]:
                    # Put the child in the OPEN queue 
                    open.append(child)
                # Check if the child is in CLOSED list    
                else:
                    index = [node.state.tab_dyn for node in closed].index(child.state.tab_dyn)
                    if child.f(heuristique) < closed[index].f(heuristique):
                        closed.remove(closed[index])
                        open.append(child)
