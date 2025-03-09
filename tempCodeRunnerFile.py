import pygame
import sys
import numpy as np
from Search import Search
from SokobanPuzzle import SokobanPuzzle
from Node import Node

# Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40  # Size of each grid cell
BACKGROUND_COLOR = (245, 245, 220)  # Beige background
TEXT_COLOR = (0, 0, 0)
FPS = 10  # Frame rate for the simulation

def draw_grid(screen, grid):
    """Draws the grid for the Sokoban puzzle."""
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            x = col * GRID_SIZE
            y = row * GRID_SIZE
            if grid[row][col] == 'O':
                pygame.draw.rect(screen, (0, 0, 0), (x, y, GRID_SIZE, GRID_SIZE))  # Wall
            elif grid[row][col] == ' ':
                pygame.draw.rect(screen, BACKGROUND_COLOR, (x, y, GRID_SIZE, GRID_SIZE))  # Empty
            elif grid[row][col] == 'B':
                pygame.draw.rect(screen, (255, 165, 0), (x, y, GRID_SIZE, GRID_SIZE))  # Box
            elif grid[row][col] == 'R':
                pygame.draw.rect(screen, (0, 0, 255), (x, y, GRID_SIZE, GRID_SIZE))  # Player
            elif grid[row][col] == 'S':
                pygame.draw.rect(screen, (0, 255, 0), (x, y, GRID_SIZE, GRID_SIZE))  # Target
            elif grid[row][col] == '*':
                pygame.draw.rect(screen, (255, 0, 0), (x, y, GRID_SIZE, GRID_SIZE))  # Box on Target
            elif grid[row][col] == '.':
                pygame.draw.rect(screen, (255, 255, 0), (x, y, GRID_SIZE, GRID_SIZE))  # Player on Target

def display_text(screen, text, pos):
    """Displays text on the Pygame window."""
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, pos)

def main():
    """Main function to run the Pygame interface."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Sokoban Solver Simulation')

    # Sample grid and robot position for testing
    grid = np.array([
        ['O', 'O', 'O', 'O', 'O'],
        ['O', ' ', 'S', 'B', 'O'],
        ['O', 'R', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O']
    ])
    robot_start_position = (2, 1)
    puzzle = SokobanPuzzle(grid, robot_start_position)

    # Perform the search
    initial_node = Node(puzzle)  # Only pass the puzzle object
    result_node, _ = Search.Astar(initial_node)  # Assuming A* returns a Node with the solution

    if result_node is not None:
        # Draw the initial state
        clock = pygame.time.Clock()
        steps = result_node.get_path()  # Ensure this returns the correct path
        cost = result_node.g  # Get the cost of the solution

        # Main loop
        running = True
        step_index = 0  # Index to track the current step

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear the screen
            screen.fill(BACKGROUND_COLOR)

            # Split the screen into two sections
            left_width = 300  # Width for the left section
            right_width = WINDOW_WIDTH - left_width

            # Draw the cost and steps on the left
            pygame.draw.rect(screen, (255, 255, 255), (0, 0, left_width, WINDOW_HEIGHT))  # White background for text area
            display_text(screen, f'Cost: {cost}', (10, 10))
            display_text(screen, f'Steps: {len(steps)}', (10, 50))

            # Draw the grid at the current step on the right
            if step_index < len(steps):
                current_state = steps[step_index].state.grid  # Get the current state directly from steps
                draw_grid(screen, current_state)  # Pass the state directly to draw_grid
                step_index += 1  # Move to the next step in the solution

            # Update the display
            pygame.display.flip()

            # Control the simulation speed
            clock.tick(FPS)  # Use clock to manage FPS
    else:
        print("No solution found!")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
