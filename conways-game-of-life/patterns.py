"""
Classic Conway's Game of Life patterns

This module contains various well-known patterns that can be used
to initialize the Game of Life grid with interesting configurations.
"""

from typing import List, Tuple


class Patterns:
    """Collection of classic Game of Life patterns"""
    
    @staticmethod
    def glider() -> List[Tuple[int, int]]:
        """
        The Glider - a pattern that moves diagonally across the grid
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    
    @staticmethod
    def blinker() -> List[Tuple[int, int]]:
        """
        The Blinker - oscillates between horizontal and vertical line
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(0, 1), (1, 1), (2, 1)]
    
    @staticmethod
    def block() -> List[Tuple[int, int]]:
        """
        The Block - a stable 2x2 square
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(0, 0), (1, 0), (0, 1), (1, 1)]
    
    @staticmethod
    def beehive() -> List[Tuple[int, int]]:
        """
        The Beehive - a stable hexagonal pattern
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)]
    
    @staticmethod
    def loaf() -> List[Tuple[int, int]]:
        """
        The Loaf - a stable pattern
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)]
    
    @staticmethod
    def boat() -> List[Tuple[int, int]]:
        """
        The Boat - a stable pattern
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(0, 0), (1, 0), (0, 1), (2, 1), (1, 2)]
    
    @staticmethod
    def toad() -> List[Tuple[int, int]]:
        """
        The Toad - oscillates between two configurations
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)]
    
    @staticmethod
    def beacon() -> List[Tuple[int, int]]:
        """
        The Beacon - oscillates between two configurations
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)]
    
    @staticmethod
    def lightweight_spaceship() -> List[Tuple[int, int]]:
        """
        The Lightweight Spaceship (LWSS) - moves horizontally across the grid
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)]
    
    @staticmethod
    def pulsar() -> List[Tuple[int, int]]:
        """
        The Pulsar - a period-3 oscillator
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        pattern = []
        # Top part
        for x in [2, 3, 4, 8, 9, 10]:
            pattern.append((x, 0))
        
        # Upper middle part
        for y in [2, 5]:
            for x in [0, 5, 7, 12]:
                pattern.append((x, y))
        
        # Middle horizontal lines
        for x in [2, 3, 4, 8, 9, 10]:
            pattern.append((x, 5))
            pattern.append((x, 7))
        
        # Lower middle part
        for y in [7, 10]:
            for x in [0, 5, 7, 12]:
                pattern.append((x, y))
        
        # Bottom part
        for x in [2, 3, 4, 8, 9, 10]:
            pattern.append((x, 12))
        
        return pattern
    
    @staticmethod
    def gosper_glider_gun() -> List[Tuple[int, int]]:
        """
        The Gosper Glider Gun - produces gliders continuously
        
        Returns:
            List of (x, y) coordinates for the pattern
        """
        return [
            # Left square
            (0, 4), (0, 5), (1, 4), (1, 5),
            # Left part
            (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (12, 2), (12, 8),
            (13, 2), (13, 8), (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6),
            (17, 5),
            # Right part
            (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4), (22, 1), (22, 5),
            (24, 0), (24, 1), (24, 5), (24, 6),
            # Right square
            (34, 2), (34, 3), (35, 2), (35, 3)
        ]


def apply_pattern(game, pattern: List[Tuple[int, int]], offset_x: int = 0, offset_y: int = 0):
    """
    Apply a pattern to the game grid
    
    Args:
        game: GameOfLife instance
        pattern: List of (x, y) coordinates for the pattern
        offset_x: X offset to apply to the pattern
        offset_y: Y offset to apply to the pattern
    """
    for x, y in pattern:
        game.set_cell(x + offset_x, y + offset_y, True)