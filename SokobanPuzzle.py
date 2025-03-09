# SokobanPuzzle.py
import numpy as np
from copy import deepcopy

# Define constants for grid elements
PLAYER = 'R'
WALL = 'O'
EMPTY = ' '
TARGET = 'S'
BOX = 'B'
PLAYER_ON_TARGET = '.'
BOX_ON_TARGET = '*'

class SokobanPuzzle:
    def __init__(self, grid, robot_position):
        self.grid = np.array(grid)  # Dynamic elements of the puzzle (robot, boxes)
        self.robot_position = robot_position  # Robot's position tuple
        self.moves = {
            "U": (-1, 0),  # Move Up
            "D": (1, 0),   # Move Down
            "L": (0, -1),  # Move Left
            "R": (0, 1)    # Move Right
        }

    def is_goal(self):
        # Check if all targets ('S') have boxes ('B' or '*')
        S_indices_x, S_indices_y = np.where(self.grid == TARGET)  # Get all target spaces
        for ind_x, ind_y in zip(S_indices_x, S_indices_y):
            if self.grid[ind_x][ind_y] != BOX and self.grid[ind_x][ind_y] != BOX_ON_TARGET:
                return False
        return True

    def execute_move(self, direction):
        # Determine new position based on direction
        new_r, new_c = self.robot_position
        if direction == 'U':
            new_r -= 1
        elif direction == 'D':
            new_r += 1
        elif direction == 'L':
            new_c -= 1
        elif direction == 'R':
            new_c += 1

        # Check if the new position is a wall
        if self.grid[new_r][new_c] == WALL:
            return False

        # Check if the new position is a box
        if self.grid[new_r][new_c] in (BOX, BOX_ON_TARGET):
            next_r, next_c = new_r, new_c
            if direction == 'U':
                next_r -= 1
            elif direction == 'D':
                next_r += 1
            elif direction == 'L':
                next_c -= 1
            elif direction == 'R':
                next_c += 1

            # Ensure the next position is not a wall or another box
            if self.grid[next_r][next_c] in (EMPTY, TARGET):
                # Move the box
                if self.grid[next_r][next_c] == TARGET:
                    self.grid[next_r][next_c] = BOX_ON_TARGET
                else:
                    self.grid[next_r][next_c] = BOX

                # Restore target if the box was on one
                if self.grid[new_r][new_c] == BOX_ON_TARGET:
                    self.grid[new_r][new_c] = TARGET
                else:
                    self.grid[new_r][new_c] = EMPTY
            else:
                return False

        # Move the robot
        if self.grid[new_r][new_c] == TARGET:
            self.grid[new_r][new_c] = PLAYER_ON_TARGET
        else:
            self.grid[new_r][new_c] = PLAYER

        # Restore target if the robot was on one
        if self.grid[self.robot_position[0]][self.robot_position[1]] == PLAYER_ON_TARGET:
            self.grid[self.robot_position[0]][self.robot_position[1]] = TARGET
        else:
            self.grid[self.robot_position[0]][self.robot_position[1]] = EMPTY

        # Update robot position
        self.robot_position = (new_r, new_c)
        return True

    def move(self, direction):
        """General method to move the robot in the given direction."""
        dx, dy = direction
        robot_x, robot_y = self.robot_position
        new_robot_x, new_robot_y = robot_x + dx, robot_y + dy

        # Check boundaries and wall
        if not self.is_in_bounds(new_robot_x, new_robot_y) or self.grid[new_robot_x][new_robot_y] == WALL:
            return False
        # Check if the robot is moving towards a box
        if self.grid[new_robot_x][new_robot_y] == BOX:
            # Check if the box can be pushed
            new_box_x, new_box_y = new_robot_x + dx, new_robot_y + dy
            if not self.is_in_bounds(new_box_x, new_box_y) or self.grid[new_box_x][new_box_y] == BOX or self.grid[new_box_x][new_box_y] == WALL:
                return False  # Can't push the box
            # Move the box
            self.update_position((new_box_x, new_box_y), (new_robot_x, new_robot_y), BOX)
        # Move the robot
        self.update_position((new_robot_x, new_robot_y), (robot_x, robot_y), PLAYER)
        self.robot_position = (new_robot_x, new_robot_y)
        return True

    def perform_action(self, action):
        """Perform an action and return the new state."""
        next_state = deepcopy(self)  # Create a deep copy of the current state
        if next_state.execute_move(action):  # Attempt to execute the action
            return next_state  # Return the new state if the action was successful
        return None  # Return None if the action was not successful

    def is_in_bounds(self, x, y):
        """Check if the position is within the bounds of the grid."""
        return 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1]

    def update_position(self, new_pos, old_pos, element):
        """Update the position of the robot or box."""
        new_x, new_y = new_pos
        old_x, old_y = old_pos
        # Update the new position (check if it's a target space or not)
        if self.grid[new_x][new_y] == TARGET:
            self.grid[new_x][new_y] = BOX_ON_TARGET if element == BOX else PLAYER_ON_TARGET
        else:
            self.grid[new_x][new_y] = element
        # Update the old position
        if self.grid[old_x][old_y] == BOX_ON_TARGET:
            self.grid[old_x][old_y] = TARGET
        else:
            self.grid[old_x][old_y] = EMPTY

    def print_board(self):
        """Print the current dynamic state of the board."""
        for row in self.grid:
            print(''.join(row))
        print("\n")

    def succ(self):
        """Generates pairs of (action, successor) representing all valid moves."""
        successors = []
        for action, direction in self.moves.items():
            next_state = deepcopy(self)  # Create a deep copy of the current puzzle state
            if next_state.execute_move(action):  # Check if the move is valid
                successors.append((action, next_state))
        return successors

    def get_possible_actions(self):
        """Return a list of possible actions (U, D, L, R)."""
        return list(self.moves.keys())

"""
grid = [
    ['O', 'O', 'O', 'O', 'O'],
    ['O', ' ', 'S', 'B', 'O'],
    ['O', 'R', ' ', ' ', 'O'],
    ['O', 'O', 'O', 'O', 'O']
]
robot_start_position = (2, 1)  # Starting position of the robot
target_positions = [(1, 2)]  # Position of the target
box_positions = [(1, 3)]  # Position of the box

# Create instances
puzzle_first = SokobanPuzzle(grid, robot_start_position)
puzzle_mixed = SokobanPuzzle(grid, robot_start_position)

# Print initial state
print("Initial state for both implementations:")
puzzle_first.print_board()
puzzle_mixed.print_board()

# Execute moves
for action in ['U', 'R']:  # Move Up and then Right
    print(f"Executing move {action} in the first implementation:")
    puzzle_first.execute_move(action)
    puzzle_first.print_board()
    print(f"Executing move {action} in the mixed implementation:")
    puzzle_mixed.execute_move(action)
    puzzle_mixed.print_board()

# Check goal state
print("First implementation is goal:", puzzle_first.is_goal())
print("Mixed implementation is goal:", puzzle_mixed.is_goal())
"""
