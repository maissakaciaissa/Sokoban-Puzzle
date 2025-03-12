# Sokoban-Puzzle
🧩 Sokoban Puzzle Solver with BFS and A* 🚀
This repository contains a Python implementation of the Sokoban puzzle game, solved using Breadth-First Search (BFS) and A search algorithms*. Sokoban is a classic puzzle where the player pushes boxes to target spaces in a maze-like warehouse. The project includes modeling the game, implementing search algorithms, and creating a GUI using Pygame.
### 🎯 Objective
Model the Sokoban game using Python 🐍.
Implement BFS and A* algorithms to solve the puzzle.
Create a Pygame GUI to visualize the solution.
Detect and handle deadlocks (corner and line) to optimize the search.

### 📜 Game Rules
🎮 The player moves in four directions (UP, DOWN, LEFT, RIGHT).
📦 Boxes can only be pushed, not pulled.
🎯 The goal is to place all boxes on target spaces.
🚫 Deadlocks occur when boxes get stuck in corners or against walls.
### 🧠 Search Algorithms
#### Breadth-First Search (BFS):
Explores all possible moves level by level.
Guarantees the shortest path but can be slow for complex puzzles.
#### A Search*:
Uses heuristics to guide the search.
Two heuristics implemented:
h1: Number of boxes not on targets.
h2: h1 + Manhattan distance of boxes to nearest targets.
h3: Custom heuristic (to be proposed by you).

