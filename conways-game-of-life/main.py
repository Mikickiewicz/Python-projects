#!/usr/bin/env python3
"""
Conway's Game of Life - Main Application

A terminal-based implementation of Conway's Game of Life cellular automaton.
This file provides the main game loop and user interface for the simulation.

Usage:
    python main.py [options]
    
Examples:
    python main.py                    # Run with default settings
    python main.py --width 80 --height 25  # Custom grid size
    python main.py --pattern glider   # Start with a glider pattern
    python main.py --random          # Start with random configuration
"""

import argparse
import time
import sys
import signal
from typing import Optional

from game_of_life import GameOfLife
from display import create_display
from patterns import Patterns, apply_pattern


class GameController:
    """Main controller for the Game of Life simulation"""
    
    def __init__(self, width: int = 50, height: int = 25, 
                 display_type: str = "console", delay: float = 0.1):
        """
        Initialize the game controller
        
        Args:
            width: Width of the game grid
            height: Height of the game grid
            display_type: Type of display ("console" or "color")
            delay: Delay between generations in seconds
        """
        self.game = GameOfLife(width, height)
        self.display = create_display(display_type)
        self.delay = delay
        self.running = False
        self.paused = False
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals (Ctrl+C) for graceful shutdown"""
        print("\n\nShutting down gracefully...")
        self.running = False
        sys.exit(0)
    
    def run_interactive(self):
        """Run the game in interactive mode with menu options"""
        while True:
            self.display.clear_screen()
            print("=" * 60)
            print("Conway's Game of Life - Interactive Mode")
            print("=" * 60)
            print()
            self.display.display_grid(self.game)
            print()
            
            print("Options:")
            print("  1. Start simulation")
            print("  2. Step once")
            print("  3. Clear grid")
            print("  4. Randomize grid")
            print("  5. Load pattern")
            print("  6. Settings")
            print("  q. Quit")
            print()
            
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'q' or choice == 'quit':
                break
            elif choice == '1':
                self.run_simulation()
            elif choice == '2':
                self.game.next_generation()
            elif choice == '3':
                self.game.clear_grid()
            elif choice == '4':
                probability = input("Enter probability (0.0-1.0, default 0.3): ").strip()
                try:
                    prob = float(probability) if probability else 0.3
                    self.game.randomize(prob)
                except ValueError:
                    print("Invalid probability. Using default 0.3")
                    self.game.randomize(0.3)
                input("Press Enter to continue...")
            elif choice == '5':
                self.load_pattern_interactive()
            elif choice == '6':
                self.settings_menu()
            else:
                print("Invalid choice. Press Enter to continue...")
                input()
    
    def settings_menu(self):
        """Display and handle the settings menu"""
        while True:
            self.display.clear_screen()
            print("Settings")
            print("=" * 20)
            print(f"Current delay: {self.delay} seconds")
            print(f"Grid size: {self.game.width}x{self.game.height}")
            print()
            print("1. Change delay")
            print("2. Change grid size")
            print("3. Change display type")
            print("b. Back to main menu")
            print()
            
            choice = input("Enter your choice: ").strip().lower()
            
            if choice == 'b' or choice == 'back':
                break
            elif choice == '1':
                try:
                    new_delay = float(input(f"Enter new delay (current: {self.delay}): "))
                    if new_delay >= 0:
                        self.delay = new_delay
                    else:
                        print("Delay must be non-negative")
                except ValueError:
                    print("Invalid delay value")
                input("Press Enter to continue...")
            elif choice == '2':
                try:
                    width = int(input(f"Enter new width (current: {self.game.width}): "))
                    height = int(input(f"Enter new height (current: {self.game.height}): "))
                    if width > 0 and height > 0:
                        self.game = GameOfLife(width, height)
                    else:
                        print("Width and height must be positive")
                except ValueError:
                    print("Invalid dimensions")
                input("Press Enter to continue...")
            elif choice == '3':
                print("Available display types:")
                print("1. console (simple)")
                print("2. color (with colors)")
                display_choice = input("Choose display type (1-2): ").strip()
                if display_choice == '1':
                    self.display = create_display("console")
                elif display_choice == '2':
                    self.display = create_display("color")
                else:
                    print("Invalid choice")
                input("Press Enter to continue...")
    
    def load_pattern_interactive(self):
        """Interactive pattern selection and placement"""
        patterns = {
            '1': ('Glider', Patterns.glider()),
            '2': ('Blinker', Patterns.blinker()),
            '3': ('Block', Patterns.block()),
            '4': ('Beehive', Patterns.beehive()),
            '5': ('Loaf', Patterns.loaf()),
            '6': ('Boat', Patterns.boat()),
            '7': ('Toad', Patterns.toad()),
            '8': ('Beacon', Patterns.beacon()),
            '9': ('Lightweight Spaceship', Patterns.lightweight_spaceship()),
            '10': ('Pulsar', Patterns.pulsar()),
            '11': ('Gosper Glider Gun', Patterns.gosper_glider_gun()),
        }
        
        self.display.clear_screen()
        print("Available Patterns:")
        print("=" * 30)
        for key, (name, _) in patterns.items():
            print(f"{key:2s}. {name}")
        print()
        
        choice = input("Select pattern (number): ").strip()
        if choice in patterns:
            name, pattern = patterns[choice]
            print(f"Selected: {name}")
            
            # Get placement position
            try:
                x = int(input(f"Enter X position (0-{self.game.width-1}): "))
                y = int(input(f"Enter Y position (0-{self.game.height-1}): "))
                
                if 0 <= x < self.game.width and 0 <= y < self.game.height:
                    apply_pattern(self.game, pattern, x, y)
                    print(f"Pattern '{name}' placed at ({x}, {y})")
                else:
                    print("Position out of bounds")
            except ValueError:
                print("Invalid position")
        else:
            print("Invalid pattern selection")
        
        input("Press Enter to continue...")
    
    def run_simulation(self):
        """Run the main simulation loop"""
        self.running = True
        self.paused = False
        
        print("\nStarting simulation...")
        print("Controls:")
        print("  Space: Pause/Resume")
        print("  Ctrl+C: Stop simulation")
        print("\nPress Enter to start...")
        input()
        
        try:
            while self.running:
                self.display.clear_screen()
                self.display.display_grid(self.game)
                
                if self.paused:
                    print("\n[PAUSED] - Press Enter to resume...")
                    input()
                    self.paused = False
                    continue
                
                # Check if simulation has ended (no living cells)
                if self.game.is_empty():
                    print("\nSimulation ended - no living cells remaining.")
                    input("Press Enter to return to menu...")
                    break
                
                self.game.next_generation()
                time.sleep(self.delay)
                
        except KeyboardInterrupt:
            self.running = False
            print("\n\nSimulation stopped by user.")
    
    def run_automatic(self, generations: Optional[int] = None):
        """
        Run the simulation automatically for a specified number of generations
        
        Args:
            generations: Number of generations to run (None for infinite)
        """
        self.running = True
        generation_count = 0
        
        try:
            while self.running:
                self.display.clear_screen()
                self.display.display_grid(self.game)
                
                if generations and generation_count >= generations:
                    print(f"\nCompleted {generations} generations.")
                    break
                
                if self.game.is_empty():
                    print(f"\nSimulation ended after {generation_count} generations - no living cells.")
                    break
                
                self.game.next_generation()
                generation_count += 1
                time.sleep(self.delay)
                
        except KeyboardInterrupt:
            print(f"\n\nSimulation stopped after {generation_count} generations.")


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py --auto --generations 100 # Run 100 generations automatically
  python main.py --pattern glider         # Start with glider pattern
  python main.py --random --width 80      # Random 80x25 grid
        """
    )
    
    parser.add_argument('--width', type=int, default=50,
                       help='Width of the grid (default: 50)')
    parser.add_argument('--height', type=int, default=25,
                       help='Height of the grid (default: 25)')
    parser.add_argument('--delay', type=float, default=0.1,
                       help='Delay between generations in seconds (default: 0.1)')
    parser.add_argument('--display', choices=['console', 'color'], default='console',
                       help='Display type (default: console)')
    parser.add_argument('--pattern', type=str,
                       help='Initial pattern (glider, blinker, block, etc.)')
    parser.add_argument('--random', action='store_true',
                       help='Start with random configuration')
    parser.add_argument('--probability', type=float, default=0.3,
                       help='Probability for random initialization (default: 0.3)')
    parser.add_argument('--auto', action='store_true',
                       help='Run simulation automatically (non-interactive)')
    parser.add_argument('--generations', type=int,
                       help='Number of generations to run in auto mode')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive integers")
        sys.exit(1)
    
    if args.delay < 0:
        print("Error: Delay must be non-negative")
        sys.exit(1)
    
    if args.probability < 0 or args.probability > 1:
        print("Error: Probability must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Create game controller
    controller = GameController(args.width, args.height, args.display, args.delay)
    
    # Initialize grid based on arguments
    if args.random:
        controller.game.randomize(args.probability)
    elif args.pattern:
        pattern_name = args.pattern.lower()
        pattern_map = {
            'glider': Patterns.glider(),
            'blinker': Patterns.blinker(),
            'block': Patterns.block(),
            'beehive': Patterns.beehive(),
            'loaf': Patterns.loaf(),
            'boat': Patterns.boat(),
            'toad': Patterns.toad(),
            'beacon': Patterns.beacon(),
            'lwss': Patterns.lightweight_spaceship(),
            'pulsar': Patterns.pulsar(),
            'gun': Patterns.gosper_glider_gun(),
        }
        
        if pattern_name in pattern_map:
            # Center the pattern
            center_x = args.width // 2
            center_y = args.height // 2
            apply_pattern(controller.game, pattern_map[pattern_name], center_x, center_y)
        else:
            print(f"Error: Unknown pattern '{args.pattern}'")
            print("Available patterns:", ', '.join(pattern_map.keys()))
            sys.exit(1)
    
    # Run the simulation
    if args.auto:
        controller.run_automatic(args.generations)
    else:
        controller.run_interactive()


if __name__ == "__main__":
    main()