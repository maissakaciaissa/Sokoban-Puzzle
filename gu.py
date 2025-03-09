import tkinter as tk
import random
from PIL import Image, ImageTk  # Ensure you have PIL installed
from SokobanPuzzle import SokobanPuzzle  # Import your SokobanPuzzle class
from Node import Node  # Import your Node class

class SokobanGUI:
    def __init__(self, master, puzzle, wall_image, robot_image):
        self.master = master
        self.puzzle = puzzle
        self.robot_position = puzzle.robot_position  # Initialize robot position
        self.moves = 0  # Track player moves
        self.master.title("Sokoban Game")
        self.wall_image = wall_image  # Store the wall image
        self.robot_image = robot_image  # Store the robot image
        self.create_widgets()
        self.update_board()
        self.master.bind('<Up>', self.move_up)
        self.master.bind('<Down>', self.move_down)
        self.master.bind('<Left>', self.move_left)
        self.master.bind('<Right>', self.move_right)
        self.center_window()

    def create_widgets(self):
        # Create a frame to hold the game info and buttons
        self.info_frame = tk.Frame(self.master, bg='beige')  # Set background to beige
        self.info_frame.grid(row=0, column=0, pady=10)

        # Display moves
        self.moves_label = tk.Label(self.info_frame, text=f"Your moves: {self.moves}", bg='beige')
        self.moves_label.pack()

        # Create a canvas for better control over graphics
        self.canvas = tk.Canvas(self.master, width=300, height=300, bg='beige')  # Set background to beige
        self.canvas.grid(row=1, column=0, padx=10, pady=10)
        self.cell_size = 60

    def update_board(self):
        # Clear the canvas
        self.canvas.delete("all")
        for r in range(len(self.puzzle.grid)):
            for c in range(len(self.puzzle.grid[0])):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                symbol = self.puzzle.grid[r][c]

                if symbol == 'O':
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.wall_image)  # Use wall image
                elif symbol == 'R' or symbol == '.':
                    self.canvas.create_image(x1, y1, anchor=tk.NW, image=self.robot_image)  # Use robot image
                elif symbol == 'B':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown')
                elif symbol == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow')
                elif symbol == '*':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='beige')  # Set empty space to beige

        # Check for win condition
        if self.check_win():
            self.canvas.create_text(150, 150, text="WON", font=("Helvetica", 24), fill="green")

    def check_win(self):
        # Check if all boxes are on storage locations
        for r in range(len(self.puzzle.grid)):
            for c in range(len(self.puzzle.grid[0])):
                if self.puzzle.grid[r][c] == 'B':
                    return False
        return True

    def move_robot(self, direction):
        # Generalize the move logic based on direction
        move_made = False
        r, c = self.robot_position
        if direction == 'U' and r > 0:
            move_made = self.puzzle.execute_move('U')
        elif direction == 'D' and r < len(self.puzzle.grid) - 1:
            move_made = self.puzzle.execute_move('D')
        elif direction == 'L' and c > 0:
            move_made = self.puzzle.execute_move('L')
        elif direction == 'R' and c < len(self.puzzle.grid[0]) - 1:
            move_made = self.puzzle.execute_move('R')

        if move_made:
            self.robot_position = self.puzzle.robot_position
            self.moves += 1
            self.moves_label.config(text=f"Your moves: {self.moves}")
            self.update_board()

    def move_up(self, event):
        self.move_robot('U')

    def move_down(self, event):
        self.move_robot('D')

    def move_left(self, event):
        self.move_robot('L')

    def move_right(self, event):
        self.move_robot('R')

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

def generate_random_grid(rows, cols, num_boxes, num_storage):
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    # Place outer walls
    for r in range(rows):
        grid[r][0] = 'O'
        grid[r][cols - 1] = 'O'
    for c in range(cols):
        grid[0][c] = 'O'
        grid[rows - 1][c] = 'O'

    def is_valid_position(grid, r, c):
        # Check if the position is valid for placing a box (not in a corner, etc.)
        if grid[r][c] != ' ':
            return False
        if grid[r-1][c] == 'O' and grid[r][c-1] == 'O':
            return False
        if grid[r-1][c] == 'O' and grid[r][c+1] == 'O':
            return False
        if grid[r+1][c] == 'O' and grid[r][c-1] == 'O':
            return False
        if grid[r+1][c] == 'O' and grid[r][c+1] == 'O':
            return False
        return True

    # Randomly place boxes (B) and storage locations (S)
    placed_boxes = 0
    placed_storage = 0
    while placed_boxes < num_boxes or placed_storage < num_storage:
        r, c = random.randint(1, rows-2), random.randint(1, cols-2)
        if placed_boxes < num_boxes and is_valid_position(grid, r, c):
            grid[r][c] = 'B'
            placed_boxes += 1
        elif placed_storage < num_storage and grid[r][c] == ' ':
            grid[r][c] = 'S'
            placed_storage += 1

    while True:
        r, c = random.randint(1, rows-2), random.randint(1, cols-2)
        if grid[r][c] == ' ':
            grid[r][c] = 'R'
            robot_position = (r, c)
            break
    
    return grid, robot_position

if __name__ == "__main__":
    root = tk.Tk()
    rows, cols = 6, 6  # Example dimensions, you can adjust these
    num_boxes = 3
    num_storage = 3
    grid, robot_start_position = generate_random_grid(rows, cols, num_boxes, num_storage)
    puzzle = SokobanPuzzle(grid, robot_start_position)

    # Load the wall and robot images
    wall_image_path = "wall.png"  # Path to the wall image file
    robot_image_path = "robot.png"  # Path to the robot image file
    wall_image = ImageTk.PhotoImage(Image.open(wall_image_path).resize((60, 60)))
    robot_image = ImageTk.PhotoImage(Image.open(robot_image_path).resize((60, 60)))

    app = SokobanGUI(root, puzzle, wall_image, robot_image)
    root.mainloop()
