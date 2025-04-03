"""
Search algorithms for the Pac-Man Search Algorithms project.
This module provides a template for implementing the search algorithms.
The actual implementation will be done by the user's team.
"""
from collections import deque
import time
import os
from utils.game_utils import get_neighbors

# Try to import psutil for memory measurement, but provide a fallback if not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Note: psutil not installed. Memory usage stats will not be available.")
    print("To install: pip install psutil")

class SearchAlgorithm:
    """Base class for search algorithms."""
    
    def __init__(self, maze):
        """Initialize the search algorithm with the maze layout."""
        self.maze = maze
        self.expanded_nodes = 0
        self.search_time = 0
        self.memory_usage = 0
    
    def search(self, start, goal):
        """
        Search for a path from start to goal.
        
        Args:
            start: Tuple (x, y) representing the start position
            goal: Tuple (x, y) representing the goal position
            
        Returns:
            path: List of positions from start to goal
            stats: Dictionary containing performance metrics
        """
        raise NotImplementedError("Subclasses must implement search method")
    
    def get_stats(self):
        """Get the performance metrics for the search."""
        return {
            "expanded_nodes": self.expanded_nodes,
            "search_time": self.search_time,
            "memory_usage": self.memory_usage
        }
    
    def _measure_memory(self):
        """Measure the current memory usage in MB."""
        if HAS_PSUTIL:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / (1024 * 1024)  # Convert to MB
        else:
            return 0.0  # Return 0 if psutil is not available

class BFSAlgorithm(SearchAlgorithm):
    """Breadth-First Search algorithm implementation."""
    
    def search(self, start, goal):
        """
        Implement BFS to find a path from start to goal.
        
        BFS (Breadth-First Search) explores all neighbors at the current depth
        before moving to nodes at the next depth level.
        """
        # Record start time and memory
        start_time = time.time()
        start_memory = self._measure_memory()
        
        # Initialize BFS data structures
        queue = deque([(start[0], start[1])])
        visited = set([(start[0], start[1])])
        parent = {(start[0], start[1]): None}
        
        # BFS loop
        while queue:
            current = queue.popleft()
            self.expanded_nodes += 1
            
            # Check if we've reached the goal
            if current[0] == goal[0] and current[1] == goal[1]:
                break
            
            # Get neighbors
            for neighbor in get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
        
        # Reconstruct path
        path = []
        current = (goal[0], goal[1])
        
        # Check if a path was found
        if current in parent or current == (start[0], start[1]):
            while current:
                path.append(current)
                current = parent.get(current)
            path.reverse()
        
        # Record end time and memory
        end_time = time.time()
        end_memory = self._measure_memory()
        
        # Update metrics
        self.search_time = end_time - start_time
        self.memory_usage = end_memory - start_memory
        
        return path, self.get_stats()

class DFSAlgorithm(SearchAlgorithm):
    """Depth-First Search algorithm implementation."""
    
    def search(self, start, goal):
        """
        Implement DFS to find a path from start to goal.
        
        This is a placeholder. The actual implementation will be done by the user's team.
        """
        # Placeholder for DFS implementation
        return [], self.get_stats()

class UCSAlgorithm(SearchAlgorithm):
    """Uniform-Cost Search algorithm implementation."""
    
    def search(self, start, goal):
        """
        Implement UCS to find a path from start to goal.
        
        This is a placeholder. The actual implementation will be done by the user's team.
        """
        # Placeholder for UCS implementation
        return [], self.get_stats()

class AStarAlgorithm(SearchAlgorithm):
    """A* Search algorithm implementation."""
    
    def search(self, start, goal):
        """
        Implement A* to find a path from start to goal.
        
        This is a placeholder. The actual implementation will be done by the user's team.
        """
        # Placeholder for A* implementation
        return [], self.get_stats()
