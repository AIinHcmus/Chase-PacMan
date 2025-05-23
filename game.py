"""
Main game class for the Pac-Man Search Algorithms project.
"""
import pygame
from pygame import K_RIGHT, K_DOWN, K_LEFT, K_UP, QUIT, KEYDOWN, K_q, K_SPACE, K_ESCAPE, K_RETURN, K_p, K_s, K_d, SRCALPHA
import sys
import math
from pygame.locals import *
from constants.game_constants import *
from utils.game_utils import calculate_maze_offset, find_initial_positions, is_valid_move
from algorithms.search_algorithms import BFSAlgorithm, DFSAlgorithm, UCSAlgorithm, AStarAlgorithm

class PacmanGame:
    def __init__(self):
        """Initialize the game."""
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pac-Man Search Algorithms')
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_state = MENU
        self.current_level = 1
        
        # Font setup
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 36)
        
        # Calculate maze offset
        self.maze_offset_x, self.maze_offset_y = calculate_maze_offset()
        
        # Store a copy of the original maze layout
        self.original_maze_layout = [row[:] for row in MAZE_LAYOUT]
        
        # Initialize positions
        self.reset_game()
        
        # Pacman animation
        self.pacman_direction = RIGHT
        self.pacman_animation_time = 0
        self.pacman_animation_speed = 5.25
        
        # Stats display
        self.show_stats = False
        self.stats = {
            "expanded_nodes": 0,
            "search_time": 0,
            "memory_usage": 0
        }
        
        # Path display
        self.show_path = False
        self.current_path = []
        
        # Ghost movement timers
        self.ghost_move_timer = 0
        self.ghost_move_delay = 0.2  # seconds between moves
        # Pacman movement timers
        self.pacman_move_timer = 0
        self.pacman_move_delay = 0.15  # seconds between moves

        # Level completion
        self.level_complete = False
        self.level_complete_timer = 0
     
        # Debug mode
        self.debug_mode = False

        # Ghost algorithms and paths for level 5
        self.ghost_algorithms = {
            'blue': BFSAlgorithm(MAZE_LAYOUT),
            'pink': DFSAlgorithm(MAZE_LAYOUT),
            'orange': UCSAlgorithm(MAZE_LAYOUT),
            'red': AStarAlgorithm(MAZE_LAYOUT)
        }

        self.ghost_paths = {
            'blue': [],
            'pink': [],
            'orange': [],
            'red': []
        }
    
    def reset_game(self):
        """Reset the game state."""
        # Restore the maze layout to its original state
        global MAZE_LAYOUT
        MAZE_LAYOUT = [row[:] for row in self.original_maze_layout]  # Deep copy to restore food
        
        # Find initial positions
        self.pacman_pos, self.ghost_positions = find_initial_positions()
        
        # Tùy chỉnh vị trí ghost nếu muốn
        # Ví dụ: đặt ghost ở vị trí cụ thể
        # self.ghost_positions['blue'] = [9, 8]   # Vị trí ghost xanh
        # self.ghost_positions['pink'] = [10, 8]  # Vị trí ghost hồng
        # self.ghost_positions['orange'] = [8, 8] # Vị trí ghost cam
        # self.ghost_positions['red'] = [11, 8]   # Vị trí ghost đỏ
        
        # Reset animation
        self.pacman_animation_time = 0
        self.pacman_direction = RIGHT
        
        # Reset stats
        self.stats = {
            "expanded_nodes": 0,
            "search_time": 0,
            "memory_usage": 0
        }
        
        # Reset path
        self.current_path = []

        self.ghost_paths = {
            'blue': [],
            'pink': [],
            'orange': [],
            'red': []
        }
        self.show_path = False
        
        # Reset level completion
        self.level_complete = False
        self.level_complete_timer = 0
    
    def draw_menu(self):
        """Draw the main menu screen."""
        self.screen.fill(BLACK)
        
        # Draw title
        title_text = self.title_font.render("Pac-Man Search Algorithms", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw menu options
        start_text = self.font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(start_text, start_rect)
        
        quit_text = self.font.render("Press Q to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(quit_text, quit_rect)
        
        # Draw project info
        info_text = self.font.render("Project 1: Search - CS14003", True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(info_text, info_rect)
    
    def draw_level_select(self):
        """Draw the level selection screen."""
        self.screen.fill(BLACK)
        
        # Draw title
        title_text = self.title_font.render("Select Level", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw level options
        for i, desc in enumerate(LEVEL_DESCRIPTIONS):
            level_num = i + 1
            color = YELLOW if level_num == self.current_level else WHITE
            level_text = self.font.render(f"{level_num}. {desc}", True, color)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 120 + i * 60))
            self.screen.blit(level_text, level_rect)
        
        # Draw instructions
        instr_text = self.font.render("Use UP/DOWN arrows to select, ENTER to start, ESC to go back", True, WHITE)
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH//2, 550))
        self.screen.blit(instr_text, instr_rect)
    
    def draw_pacman(self, x, y):
        """Draw Pac-Man at the specified position."""
        screen_x = self.maze_offset_x + x * CELL_SIZE + CELL_SIZE // 2
        screen_y = self.maze_offset_y + y * CELL_SIZE + CELL_SIZE // 2
        center = (screen_x, screen_y)

        radius = CELL_SIZE // 2 - 2

        angle_deg = self.pacman_direction * 90
        mouth_angle_deg = 45 * abs(math.sin(self.pacman_animation_time))

        start_angle = math.radians(angle_deg - mouth_angle_deg)
        end_angle = math.radians(angle_deg + mouth_angle_deg)

        pygame.draw.circle(self.screen, YELLOW, center, radius)

        num_points = 30
        points = [center]
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * (i / num_points)
            x_point = screen_x + radius * math.cos(angle)
            y_point = screen_y + radius * math.sin(angle)
            points.append((x_point, y_point))

        pygame.draw.polygon(self.screen, BLACK, points)


    def draw_ghost(self, x, y, color):
        """Draw a ghost at the specified position with the given color."""
        # Calculate screen position
        screen_x = self.maze_offset_x + x * CELL_SIZE + CELL_SIZE // 2
        screen_y = self.maze_offset_y + y * CELL_SIZE + CELL_SIZE // 2
        
        # Draw ghost body
        pygame.draw.circle(self.screen, color, (screen_x, screen_y), CELL_SIZE // 2 - 2)
        pygame.draw.rect(self.screen, color, (
            screen_x - (CELL_SIZE // 2 - 2),
            screen_y,
            CELL_SIZE - 4,
            CELL_SIZE // 2 - 2
        ))
        
        # Draw ghost eyes
        eye_offset = 4
        pygame.draw.circle(self.screen, WHITE, (screen_x - eye_offset, screen_y - eye_offset), 4)
        pygame.draw.circle(self.screen, WHITE, (screen_x + eye_offset, screen_y - eye_offset), 4)
        pygame.draw.circle(self.screen, BLACK, (screen_x - eye_offset, screen_y - eye_offset), 2)
        pygame.draw.circle(self.screen, BLACK, (screen_x + eye_offset, screen_y - eye_offset), 2)
    
    def draw_maze(self):
        """Draw the maze layout."""
        for y, row in enumerate(MAZE_LAYOUT):
            for x, cell in enumerate(row):
                # Calculate screen position
                screen_x = self.maze_offset_x + x * CELL_SIZE
                screen_y = self.maze_offset_y + y * CELL_SIZE
                
                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                elif cell == 2:  # Food
                    pygame.draw.circle(self.screen, WHITE, (screen_x + CELL_SIZE // 2, screen_y + CELL_SIZE // 2), 3)
    
    def draw_path(self, path, color, ghost_type=None):
        """Draw a path on the maze."""
        if not path or len(path) < 2:
            return
        
        # Calculate offset based on ghost type
        offset = 0
        if ghost_type == 'blue':
            offset = -2
        elif ghost_type == 'pink':
            offset = 2
        elif ghost_type == 'orange':
            offset = -4
        elif ghost_type == 'red':
            offset = 4

        for i in range(len(path) - 1):
            start_x = self.maze_offset_x + path[i][0] * CELL_SIZE + CELL_SIZE // 2 + offset
            start_y = self.maze_offset_y + path[i][1] * CELL_SIZE + CELL_SIZE // 2 + offset
            end_x = self.maze_offset_x + path[i+1][0] * CELL_SIZE + CELL_SIZE // 2 + offset
            end_y = self.maze_offset_y + path[i+1][1] * CELL_SIZE + CELL_SIZE // 2 + offset
            
            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.circle(self.screen, color, (start_x, start_y), 3)
        
        # Draw the last point
        last_x = self.maze_offset_x + path[-1][0] * CELL_SIZE + CELL_SIZE // 2 + offset
        last_y = self.maze_offset_y + path[-1][1] * CELL_SIZE + CELL_SIZE // 2 + offset
        pygame.draw.circle(self.screen, color, (last_x, last_y), 3)
    
    def draw_stats(self):
        """Draw performance statistics on the screen."""
        if not self.show_stats:
            return
        
        # Create a semi-transparent background
        stats_surface = pygame.Surface((300, 150))
        stats_surface.set_alpha(200)
        stats_surface.fill(BLACK)
        self.screen.blit(stats_surface, (SCREEN_WIDTH - 310, SCREEN_HEIGHT - 150))
        
        # Draw stats text
        stats_title = self.font.render("Search Statistics:", True, WHITE)
        self.screen.blit(stats_title, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100))
        
        nodes_text = self.font.render(f"Expanded Nodes: {self.stats['expanded_nodes']}", True, WHITE)
        self.screen.blit(nodes_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 70))
        
        time_text = self.font.render(f"Search Time: {self.stats['search_time']:.6f} sec", True, WHITE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 40))
        
        memory_text = self.font.render(f"Memory Usage: {self.stats['memory_usage']:.2f} MB", True, WHITE)
        self.screen.blit(memory_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 20))
    
    def draw_game(self):
        """Draw the game screen."""
        self.screen.fill(BLACK)
    
        # Draw maze
        self.draw_maze()
    
        # Draw path if enabled
        if self.show_path:
            if self.current_level in [1, 2, 3, 4] and self.current_path:
                ghost_color = None
                if self.current_level == 1:
                    ghost_color = BLUE
                elif self.current_level == 2:
                    ghost_color = PINK
                elif self.current_level == 3:
                    ghost_color = ORANGE
                elif self.current_level == 4:
                    ghost_color = RED
                if ghost_color:
                    self.draw_path(self.current_path, ghost_color)
            elif self.current_level in [5, 6]:
                for ghost_color in ACTIVE_GHOSTS[self.current_level]:
                    color = globals()[ghost_color.upper()]
                    self.draw_path(self.ghost_paths[ghost_color], color, ghost_color)
    
        # Draw Pac-Man
        if self.pacman_pos and (self.current_level == 6 or self.pacman_pos):
            self.draw_pacman(self.pacman_pos[0], self.pacman_pos[1])
    
        # Draw active ghosts based on current level
        for ghost_color in ACTIVE_GHOSTS[self.current_level]:
            if self.ghost_positions[ghost_color]:
                color = globals()[ghost_color.upper()]
                self.draw_ghost(self.ghost_positions[ghost_color][0], self.ghost_positions[ghost_color][1], color)
    
        # Draw level info
        level_text = self.font.render(f"Level {self.current_level}: {LEVEL_DESCRIPTIONS[self.current_level-1]}", True, WHITE)
        self.screen.blit(level_text, (10, 10))
    
        # Draw instructions
        if self.current_level == 6:
            instr_text = self.font.render("Use ARROW keys to move Pac-Man", True, WHITE)
            self.screen.blit(instr_text, (10, SCREEN_HEIGHT - 30))
    
        # Draw toggle options
        path_text = self.font.render(f"P: {'Hide' if self.show_path else 'Show'} Path", True, WHITE)
        self.screen.blit(path_text, (10, 40))
    
        stats_text = self.font.render(f"S: {'Hide' if self.show_stats else 'Show'} Stats", True, WHITE)
        self.screen.blit(stats_text, (10, 70))
    
        # Draw back button
        back_text = self.font.render("ESC: Back to Menu", True, WHITE)
        back_rect = back_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(back_text, back_rect)
    
        # Draw stats if enabled
        self.draw_stats()
    
        # Draw level complete message if applicable
        if self.level_complete:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
        
            # Draw level complete message
            complete_text = self.title_font.render("Level Complete!", True, YELLOW)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            self.screen.blit(complete_text, complete_rect)
        
            # Draw continue message
            continue_text = self.font.render("Press ENTER to continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            self.screen.blit(continue_text, continue_rect)
    
    def update_pacman(self, dt):
        """Update Pac-Man's position and animation."""
        # Update animation
        self.pacman_animation_time += self.pacman_animation_speed * dt

        # In level 6, allow user control
        if self.current_level == 6:
            self.pacman_move_timer += dt
        
            if self.pacman_move_timer >= self.pacman_move_delay:
                self.pacman_move_timer = 0
            
                keys = pygame.key.get_pressed()
                new_pos = self.pacman_pos.copy()
                new_direction = self.pacman_direction
            
                # Define possible directions in order of priority (last pressed key wins)
                directions = [
                    (K_RIGHT, RIGHT, (1, 0)),  # Move right: x += 1
                    (K_DOWN, DOWN, (0, 1)),    # Move down: y += 1
                    (K_LEFT, LEFT, (-1, 0)),   # Move left: x -= 1
                    (K_UP, UP, (0, -1))        # Move up: y -= 1
                ]
            
                # Check each direction in order
                for key, direction, (dx, dy) in directions:
                    if keys[key]:
                        # Try this direction
                        new_pos = [self.pacman_pos[0] + dx, self.pacman_pos[1] + dy]
                        new_direction = direction
                        # Stop checking other directions after finding the last pressed key
                        break
            
                # Check if the new position is valid (not a wall)
                if is_valid_move(new_pos[0], new_pos[1]):
                    self.pacman_pos[0] = new_pos[0]
                    self.pacman_pos[1] = new_pos[1]
                    self.pacman_direction = new_direction  # Update direction only if move is valid
                
                    # Check for food at the new position
                    if MAZE_LAYOUT[new_pos[1]][new_pos[0]] == 2:  # Food cell
                        MAZE_LAYOUT[new_pos[1]][new_pos[0]] = 0  # Remove food
                        # Check if all food is eaten
                        if not self.has_food_left():
                            self.level_complete = True
                            self.level_complete_timer = 0

    def has_food_left(self):
        """Check if there is any food left in the maze."""
        for row in MAZE_LAYOUT:
            if 2 in row:  # Food cell
                return True
        return False
    
    def update_ghosts(self, dt):
        """Update ghost positions based on their search algorithms."""
        # Increment the ghost movement timer
        self.ghost_move_timer += dt
        
        # Only move ghosts when the timer exceeds the delay
        if self.ghost_move_timer >= self.ghost_move_delay:
            self.ghost_move_timer = 0
            
            # Level 1: Blue Ghost using BFS
            if self.current_level == 1 and 'blue' in ACTIVE_GHOSTS[self.current_level]:
                # If we don't have a path or reached the end of the current path, calculate a new one
                if not self.current_path or len(self.current_path) <= 1:
                    # Create a BFS algorithm instance
                    bfs = BFSAlgorithm(MAZE_LAYOUT)
                    
                    # Get the current positions of the ghost and Pac-Man
                    ghost_pos = tuple(self.ghost_positions['blue'])
                    pacman_pos = tuple(self.pacman_pos)
                    
                    # Find a path from the ghost to Pac-Man using BFS
                    self.current_path, stats = bfs.search(ghost_pos, pacman_pos)
                    
                    # Update the stats display
                    self.stats = stats
                
                # Move the ghost along the path
                if self.current_path and len(self.current_path) > 1:
                    # Move to the next position in the path
                    self.ghost_positions['blue'] = [self.current_path[1][0], self.current_path[1][1]]
                    self.current_path.pop(0)
            
            # Level 2: Pink Ghost using DFS
            elif self.current_level == 2 and 'pink' in ACTIVE_GHOSTS[self.current_level]:
                # If we don't have a path or reached the end of the current path, calculate a new one
                if not self.current_path or len(self.current_path) <= 1:
                    # Create a DFS algorithm instance
                    dfs = DFSAlgorithm(MAZE_LAYOUT)

                    # Get the current positions of the ghost and Pac-Man
                    ghost_pos = tuple(self.ghost_positions['pink'])
                    pacman_pos = tuple(self.pacman_pos)

                    # Find a path from the ghost to Pac-Man using DFS
                    self.current_path, stats = dfs.search(ghost_pos, pacman_pos)

                    # Update the stats display
                    self.stats = stats
                # Placeholder for DFS implementation
                if self.current_path and len(self.current_path) > 1:
                    self.ghost_positions['pink'] = [self.current_path[1][0], self.current_path[1][1]]
                    self.current_path.pop(0)
            
            # Level 3: Orange Ghost using UCS
            elif self.current_level == 3 and 'orange' in ACTIVE_GHOSTS[self.current_level]:
                # If no path exists or we've reached the end of the current path, calculate a new one
                if not self.current_path or len(self.current_path) <= 1:
                    # Initialize UCS algorithm
                    ucs = UCSAlgorithm(MAZE_LAYOUT)

                    # Get current positions (convert to tuples for consistency)
                    ghost_pos = tuple(self.ghost_positions['orange'])
                    pacman_pos = tuple(self.pacman_pos)

                    # Calculate shortest path using UCS
                    self.current_path, stats = ucs.search(ghost_pos, pacman_pos)

                    # Update performance stats for display
                    self.stats = stats
                # Placeholder for UCS implementation
                if self.current_path and len(self.current_path) > 1:
                    self.ghost_positions['orange'] = [self.current_path[1][0], self.current_path[1][1]]
                    self.current_path.pop(0)
            
            # Level 4: Red Ghost using A*
            elif self.current_level == 4 and 'red' in ACTIVE_GHOSTS[self.current_level]:
                if not self.current_path or len(self.current_path) <= 1:
                    # Initialize A* algorithm instance
                    astar = AStarAlgorithm(MAZE_LAYOUT)

                    # Get current positions
                    ghost_pos = tuple(self.ghost_positions['red'])
                    pacman_pos = tuple(self.pacman_pos)

                    # Calculate optimal path using A*
                    self.current_path, stats = astar.search(ghost_pos, pacman_pos)

                    # Update performance metrics
                    self.stats = stats
                # Placeholder for A* implementation
                if self.current_path and len(self.current_path) > 1:
                    self.ghost_positions['red'] = [self.current_path[1][0], self.current_path[1][1]]
                    self.current_path.pop(0)
            
            # Level 5: All ghosts using their respective algorithms
            elif self.current_level == 5:
                # Create a temporary dictionary to store new positions
                new_positions = {}

                for ghost_color in ACTIVE_GHOSTS[self.current_level]:
                    # Calculate the new position as usual
                    if not self.ghost_paths[ghost_color] or len(self.ghost_paths[ghost_color]) <= 1:
                        ghost_pos = tuple(self.ghost_positions[ghost_color])
                        pacman_pos = tuple(self.pacman_pos)
                        self.ghost_paths[ghost_color], stats = self.ghost_algorithms[ghost_color].search(ghost_pos, pacman_pos)
                        if ghost_color == 'blue':
                            self.stats = stats

                    if self.ghost_paths[ghost_color] and len(self.ghost_paths[ghost_color]) > 1:
                        new_pos = list(self.ghost_paths[ghost_color][1])
                        new_positions[ghost_color] = new_pos

                # Check for collisions between ghosts
                positions = list(new_positions.values())
                if len(positions) == len(set(tuple(pos) for pos in positions)):  # No overlapping positions
                    for ghost_color, new_pos in new_positions.items():
                        self.ghost_positions[ghost_color] = new_pos
                        self.ghost_paths[ghost_color].pop(0)
                else:
                    # If there's a conflict, only move the first ghost (or handle differently)
                    for ghost_color, new_pos in new_positions.items():
                        if list(new_pos) not in positions[:list(new_positions.keys()).index(ghost_color)]:
                            self.ghost_positions[ghost_color] = new_pos
                            self.ghost_paths[ghost_color].pop(0)
            # Level 6: User-Controlled Pac-Man with ghosts actively chasing
            elif self.current_level == 6:
                new_positions = {}
                occupied_positions = set()
                pacman_pos_tuple = tuple(self.pacman_pos)  # Store Pac-Man's position for comparison

                for ghost_color in ACTIVE_GHOSTS[self.current_level]:
                    # Recalculate path only if necessary
                    if not self.ghost_paths[ghost_color] or len(self.ghost_paths[ghost_color]) <= 1:
                        ghost_pos = tuple(self.ghost_positions[ghost_color])
                        pacman_pos = tuple(self.pacman_pos)
                        self.ghost_paths[ghost_color], stats = self.ghost_algorithms[ghost_color].search(ghost_pos, pacman_pos)
                        if ghost_color == 'blue':  # Update stats using blue ghost as reference
                            self.stats = stats

                    # Move the ghost along the path
                    if self.ghost_paths[ghost_color] and len(self.ghost_paths[ghost_color]) > 1:
                        new_pos = list(self.ghost_paths[ghost_color][1])
                        new_pos_tuple = tuple(new_pos)

                        # Avoid collisions with other ghosts
                        if new_pos_tuple not in occupied_positions:
                            # Check for collision with Pac-Man
                            if new_pos_tuple == pacman_pos_tuple:
                                self.reset_game()  # Trigger game over immediately
                                return  # Stop updating ghosts to avoid further movement

                            new_positions[ghost_color] = new_pos
                            occupied_positions.add(new_pos_tuple)
                        else:
                            # If the position is occupied, try to find a new path in the next update
                            self.ghost_paths[ghost_color] = []  # Clear the current path to force recalculation
                            continue
                    else:
                        # If no path is found, the ghost stays in place (or you can add random movement here)
                        continue

                # Update ghost positions
                for ghost_color, new_pos in new_positions.items():
                    self.ghost_positions[ghost_color] = new_pos
                    self.ghost_paths[ghost_color].pop(0)

    def check_collisions(self):
        """Check for collisions between Pac-Man and ghosts."""
        for ghost_color in ACTIVE_GHOSTS[self.current_level]:
            if (self.ghost_positions[ghost_color] and 
                self.ghost_positions[ghost_color][0] == self.pacman_pos[0] and 
                self.ghost_positions[ghost_color][1] == self.pacman_pos[1]):
                # In a real game, this would trigger game over
                # For this demo, we'll just reset the positions
                self.reset_game()
                return True
        return False
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    return False
                
                if self.game_state == MENU:
                    if event.key == K_SPACE:
                        self.game_state = LEVEL_SELECT
                
                elif self.game_state == LEVEL_SELECT:
                    if event.key == K_ESCAPE:
                        self.game_state = MENU
                    elif event.key == K_RETURN:
                        self.game_state = GAME
                        self.reset_game()
                    elif event.key == K_UP:
                        self.current_level = max(1, self.current_level - 1)
                    elif event.key == K_DOWN:
                        self.current_level = min(len(LEVEL_DESCRIPTIONS), self.current_level + 1)
                
                elif self.game_state == GAME:
                    if event.key == K_ESCAPE:
                        self.game_state = LEVEL_SELECT
                    elif event.key == K_p:
                        # Toggle path display
                        self.show_path = not self.show_path
                    elif event.key == K_s:
                        # Toggle stats display
                        self.show_stats = not self.show_stats
                    elif event.key == K_d:
                        self.debug_mode = not self.debug_mode
                    elif event.key == K_RETURN and self.level_complete:
                        self.current_level = min(len(LEVEL_DESCRIPTIONS), self.current_level + 1)
                        self.reset_game()
                        self.level_complete = False
        
        return True
    
    def run(self):
        """Main game loop."""
        running = True
        
        # For calculating delta time
        last_time = pygame.time.get_ticks() / 1000.0
        
        while running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            running = self.handle_events()
            
            # Update game state
            if self.game_state == GAME and not self.level_complete:
                self.update_pacman(dt)
                self.update_ghosts(dt)
                self.check_collisions()
            
            # Draw current game state
            if self.game_state == MENU:
                self.draw_menu()
            elif self.game_state == LEVEL_SELECT:
                self.draw_level_select()
            elif self.game_state == GAME:
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()