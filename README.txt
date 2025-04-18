# Pac-Man Search Algorithms

This project implements a Pac-Man game where ghosts use different search algorithms to chase Pac-Man.

## Requirements

- Python 3.x
- Pygame 2.6.1 or later

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. Navigate to the project directory:
   ```
   cd pacman_search
   ```

2. Run the game:
   ```
   python main.py
   ```

## Game Controls

- **Main Menu**:
  - SPACE: Start the game
  - Q: Quit the game

- **Level Selection**:
  - UP/DOWN arrows: Select level
  - ENTER: Start selected level
  - ESC: Go back to main menu

- **In Game**:
  - ESC: Return to level selection
  - ARROW keys: Move Pac-Man (Level 6 only)

## Levels

1. Level 1: Blue Ghost using BFS
2. Level 2: Pink Ghost using DFS
3. Level 3: Orange Ghost using UCS
4. Level 4: Red Ghost using A*
5. Level 5: All Ghosts in Parallel
6. Level 6: User-Controlled Pac-Man

## Implementation Notes

This implementation focuses on the UI aspects of the game. The search algorithms (BFS, DFS, UCS, A*) need to be implemented separately as per the project requirements.
