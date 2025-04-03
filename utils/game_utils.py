"""
Utility functions for the Pac-Man Search Algorithms project.
"""
import pygame
import math
from constants.game_constants import *

def calculate_maze_offset():
    """Calculate the offset to center the maze on the screen."""
    maze_width = len(MAZE_LAYOUT[0]) * CELL_SIZE
    maze_height = len(MAZE_LAYOUT) * CELL_SIZE
    maze_offset_x = (SCREEN_WIDTH - maze_width) // 2
    maze_offset_y = (SCREEN_HEIGHT - maze_height) // 2
    return maze_offset_x, maze_offset_y

def find_initial_positions():
    """Find initial positions for Pac-Man and ghosts from the maze layout."""
    pacman_pos = None
    ghost_positions = {
        'blue': None,
        'pink': None,
        'orange': None,
        'red': None
    }
    
    ghost_count = 0
    for y, row in enumerate(MAZE_LAYOUT):
        for x, cell in enumerate(row):
            if cell == 5:  # Pacman spawn
                pacman_pos = [x, y]
            elif cell == 4:  # Ghost spawn
                # Assign ghosts to spawn positions
                ghost_count += 1
                if ghost_count == 1:
                    ghost_positions['blue'] = [x, y]
                elif ghost_count == 2:
                    ghost_positions['pink'] = [x, y]
                elif ghost_count == 3:
                    ghost_positions['orange'] = [x, y]
                elif ghost_count == 4:
                    ghost_positions['red'] = [x, y]
    
    return pacman_pos, ghost_positions

def is_valid_move(x, y):
    """Check if a move to the given position is valid (not a wall)."""
    if (0 <= x < len(MAZE_LAYOUT[0]) and 
        0 <= y < len(MAZE_LAYOUT) and
        MAZE_LAYOUT[y][x] != 1):
        return True
    return False

def get_neighbors(x, y):
    """Get all valid neighboring positions for a given position."""
    neighbors = []
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(new_x, new_y):
            neighbors.append((new_x, new_y))
    
    return neighbors

def manhattan_distance(x1, y1, x2, y2):
    """Calculate the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def draw_text(screen, text, font, color, x, y, align="center"):
    """Draw text on the screen with specified alignment."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    
    screen.blit(text_surface, text_rect)
    return text_rect
