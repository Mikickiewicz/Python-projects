#!/usr/bin/env python3
"""
Conway's Game of Life Implementation

The Game of Life is a cellular automaton devised by John Conway.
It consists of a grid of cells which, based on a few mathematical rules,
can live, die or multiply.

Rules:
1. Any live cell with fewer than two live neighbors dies (underpopulation)
2. Any live cell with two or three live neighbors lives on to the next generation
3. Any live cell with more than three live neighbors dies (overpopulation)
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction)
"""

import time
import os
import random
from typing import List, Tuple, Set


class GameOfLife:
    """Conway's Game of Life implementation"""
    
    def __init__(self, width: int = 50, height: int = 25):
        """
        Initialize the Game of Life grid
        
        Args:
            width: Width of the grid
            height: Height of the grid
        """
        self.width = width
        self.height = height
        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self.generation = 0
    
    def clear_grid(self):
        """Clear the entire grid"""
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0
    
    def set_cell(self, x: int, y: int, alive: bool = True):
        """
        Set a cell's state
        
        Args:
            x: X coordinate
            y: Y coordinate
            alive: Whether the cell should be alive
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = alive
    
    def get_cell(self, x: int, y: int) -> bool:
        """
        Get a cell's state
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if cell is alive, False otherwise
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return False
    
    def count_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Number of live neighbors
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if self.get_cell(x + dx, y + dy):
                    count += 1
        return count
    
    def next_generation(self):
        """Calculate and apply the next generation"""
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                current_cell = self.grid[y][x]
                
                # Apply Conway's rules
                if current_cell:  # Cell is alive
                    if neighbors < 2:  # Underpopulation
                        new_grid[y][x] = False
                    elif neighbors in [2, 3]:  # Survival
                        new_grid[y][x] = True
                    else:  # Overpopulation
                        new_grid[y][x] = False
                else:  # Cell is dead
                    if neighbors == 3:  # Reproduction
                        new_grid[y][x] = True
        
        self.grid = new_grid
        self.generation += 1
    
    def randomize(self, probability: float = 0.3):
        """
        Randomize the grid
        
        Args:
            probability: Probability of each cell being alive
        """
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = random.random() < probability
        self.generation = 0
    
    def is_empty(self) -> bool:
        """Check if the grid is empty (no living cells)"""
        for row in self.grid:
            if any(row):
                return False
        return True
    
    def get_living_cells(self) -> Set[Tuple[int, int]]:
        """Get set of coordinates of all living cells"""
        living = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    living.add((x, y))
        return living