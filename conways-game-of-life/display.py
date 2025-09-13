"""
Display module for Conway's Game of Life

This module handles the visualization of the Game of Life grid
using console-based output with various display options.
"""

import os
import sys
from typing import Optional


class ConsoleDisplay:
    """Console-based display for Game of Life"""
    
    def __init__(self, alive_char: str = "█", dead_char: str = " ", border: bool = True):
        """
        Initialize the console display
        
        Args:
            alive_char: Character to represent alive cells
            dead_char: Character to represent dead cells
            border: Whether to show a border around the grid
        """
        self.alive_char = alive_char
        self.dead_char = dead_char
        self.border = border
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_grid(self, game, show_stats: bool = True):
        """
        Display the current state of the game grid
        
        Args:
            game: GameOfLife instance
            show_stats: Whether to show generation and cell count statistics
        """
        if show_stats:
            living_cells = len(game.get_living_cells())
            print(f"Generation: {game.generation}")
            print(f"Living cells: {living_cells}")
            print(f"Grid size: {game.width}x{game.height}")
            print()
        
        # Top border
        if self.border:
            print("+" + "-" * game.width + "+")
        
        # Grid rows
        for y in range(game.height):
            row = ""
            if self.border:
                row += "|"
            
            for x in range(game.width):
                if game.get_cell(x, y):
                    row += self.alive_char
                else:
                    row += self.dead_char
            
            if self.border:
                row += "|"
            
            print(row)
        
        # Bottom border
        if self.border:
            print("+" + "-" * game.width + "+")
    
    def display_with_coordinates(self, game):
        """
        Display the grid with coordinate labels
        
        Args:
            game: GameOfLife instance
        """
        print(f"Generation: {game.generation}")
        print(f"Living cells: {len(game.get_living_cells())}")
        print()
        
        # Column numbers header
        print("   ", end="")
        for x in range(min(game.width, 10)):
            print(f"{x}", end="")
        if game.width > 10:
            print("   ", end="")
            for x in range(10, min(game.width, 100), 10):
                print(f"{x//10}", end=" " * 9)
        print()
        
        # Grid with row numbers
        for y in range(game.height):
            print(f"{y:2d} ", end="")
            for x in range(game.width):
                if game.get_cell(x, y):
                    print(self.alive_char, end="")
                else:
                    print(self.dead_char, end="")
            print(f" {y}")
        
        # Column numbers footer
        print("   ", end="")
        for x in range(min(game.width, 100)):
            if x < 10:
                print(f"{x}", end="")
            else:
                print(f"{x%10}", end="")
        print()


class ColorConsoleDisplay(ConsoleDisplay):
    """Enhanced console display with color support"""
    
    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
    }
    
    def __init__(self, alive_char: str = "█", dead_char: str = " ", 
                 alive_color: str = 'green', dead_color: str = 'black',
                 border: bool = True):
        """
        Initialize the color console display
        
        Args:
            alive_char: Character to represent alive cells
            dead_char: Character to represent dead cells
            alive_color: Color for alive cells
            dead_color: Color for dead cells
            border: Whether to show a border around the grid
        """
        super().__init__(alive_char, dead_char, border)
        self.alive_color = self.COLORS.get(alive_color, '')
        self.dead_color = self.COLORS.get(dead_color, '')
        self.reset_color = self.COLORS['reset']
    
    def display_grid(self, game, show_stats: bool = True):
        """
        Display the current state of the game grid with colors
        
        Args:
            game: GameOfLife instance
            show_stats: Whether to show generation and cell count statistics
        """
        if show_stats:
            living_cells = len(game.get_living_cells())
            print(f"{self.COLORS['cyan']}Generation: {game.generation}{self.reset_color}")
            print(f"{self.COLORS['yellow']}Living cells: {living_cells}{self.reset_color}")
            print(f"{self.COLORS['blue']}Grid size: {game.width}x{game.height}{self.reset_color}")
            print()
        
        # Top border
        if self.border:
            print(f"{self.COLORS['white']}+{'-' * game.width}+{self.reset_color}")
        
        # Grid rows
        for y in range(game.height):
            row = ""
            if self.border:
                row += f"{self.COLORS['white']}|{self.reset_color}"
            
            for x in range(game.width):
                if game.get_cell(x, y):
                    row += f"{self.alive_color}{self.alive_char}{self.reset_color}"
                else:
                    row += f"{self.dead_color}{self.dead_char}{self.reset_color}"
            
            if self.border:
                row += f"{self.COLORS['white']}|{self.reset_color}"
            
            print(row)
        
        # Bottom border
        if self.border:
            print(f"{self.COLORS['white']}+{'-' * game.width}+{self.reset_color}")


def create_display(display_type: str = "console", **kwargs):
    """
    Factory function to create display objects
    
    Args:
        display_type: Type of display ("console" or "color")
        **kwargs: Additional arguments for the display constructor
        
    Returns:
        Display instance
    """
    if display_type == "color":
        return ColorConsoleDisplay(**kwargs)
    else:
        return ConsoleDisplay(**kwargs)