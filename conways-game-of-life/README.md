# Conway's Game of Life

A terminal-based implementation of Conway's Game of Life cellular automaton, written in Python.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Patterns](#patterns)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## About

Conway's Game of Life is a cellular automaton devised by mathematician John Horton Conway in 1970. It consists of a grid of cells that can be either alive or dead, and evolves over discrete time steps according to simple mathematical rules. Despite its simplicity, the Game of Life is Turing complete and can simulate universal computation.

This implementation provides both interactive and automatic modes, supports various classic patterns, and offers customizable display options.

## Features

- 🎮 **Interactive Mode**: Menu-driven interface for easy exploration
- ⚡ **Automatic Mode**: Run simulations for specified generations
- 🎨 **Multiple Display Options**: Console and color-enhanced displays
- 🧩 **Classic Patterns**: 11 pre-built famous patterns (Glider, Pulsar, Gosper Gun, etc.)
- 🎲 **Random Generation**: Create random initial configurations
- ⚙️ **Configurable**: Customizable grid size, speed, and display settings
- 📊 **Statistics**: Real-time generation and cell count tracking
- 🎯 **Pattern Placement**: Interactive pattern positioning
- ⌨️ **Keyboard Controls**: Pause, resume, and stop functionality

## Installation

### Prerequisites

- Python 3.6 or higher
- Terminal with ANSI color support (for color display mode)

### Clone the Repository

```bash
git clone <repository-url>
cd conways-game-of-life
```

### No Additional Dependencies

This project uses only Python standard library modules, so no additional packages need to be installed.

## Usage

### Basic Usage

Run in interactive mode with default settings:
```bash
python main.py
```

### Command Line Options

```bash
python main.py [OPTIONS]
```

#### Available Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--width` | int | 50 | Width of the grid |
| `--height` | int | 25 | Height of the grid |
| `--delay` | float | 0.1 | Delay between generations (seconds) |
| `--display` | str | console | Display type (`console` or `color`) |
| `--pattern` | str | None | Initial pattern name |
| `--random` | flag | False | Start with random configuration |
| `--probability` | float | 0.3 | Cell probability for random mode |
| `--auto` | flag | False | Run automatically (non-interactive) |
| `--generations` | int | None | Number of generations (auto mode) |

### Interactive Mode

In interactive mode, you'll see a menu with the following options:

1. **Start simulation** - Begin the Game of Life simulation
2. **Step once** - Advance by one generation
3. **Clear grid** - Remove all living cells
4. **Randomize grid** - Generate random configuration
5. **Load pattern** - Choose from 11 classic patterns
6. **Settings** - Modify delay, grid size, and display options
7. **Quit** - Exit the program

### Keyboard Controls (During Simulation)

- **Ctrl+C**: Stop simulation and return to menu
- **Enter**: Resume from pause (in interactive simulation)

## Game Rules

Conway's Game of Life follows four simple rules:

1. **Underpopulation**: Any live cell with fewer than two live neighbors dies
2. **Survival**: Any live cell with two or three live neighbors survives
3. **Overpopulation**: Any live cell with more than three live neighbors dies
4. **Reproduction**: Any dead cell with exactly three live neighbors becomes alive

These rules are applied simultaneously to all cells in each generation.

## Patterns

This implementation includes 11 classic Game of Life patterns:

### Still Life Patterns (Static)
- **Block**: A simple 2×2 square
- **Beehive**: A stable hexagonal pattern
- **Loaf**: A stable 4×4 pattern
- **Boat**: A small stable pattern

### Oscillators (Periodic)
- **Blinker**: Period-2 oscillator (3 cells in a line)
- **Toad**: Period-2 oscillator (6 cells)
- **Beacon**: Period-2 oscillator (6 cells)
- **Pulsar**: Period-3 oscillator (large symmetric pattern)

### Spaceships (Moving)
- **Glider**: Moves diagonally, period-4
- **Lightweight Spaceship (LWSS)**: Moves horizontally, period-4

### Generators
- **Gosper Glider Gun**: Produces gliders continuously, period-30

### Pattern Usage

Load patterns via command line:
```bash
python main.py --pattern glider
python main.py --pattern pulsar
python main.py --pattern gun
```

Or select them interactively using the "Load pattern" menu option.

## Examples

### Quick Start Examples

1. **Default interactive mode**:
   ```bash
   python main.py
   ```

2. **Large grid with glider**:
   ```bash
   python main.py --width 80 --height 30 --pattern glider
   ```

3. **Random configuration with color display**:
   ```bash
   python main.py --random --display color --probability 0.4
   ```

4. **Auto-run 50 generations of Gosper Gun**:
   ```bash
   python main.py --auto --pattern gun --generations 50 --width 60
   ```

5. **Fast-paced pulsar**:
   ```bash
   python main.py --pattern pulsar --delay 0.05 --display color
   ```

### Advanced Examples

1. **Dense random field**:
   ```bash
   python main.py --random --probability 0.6 --width 100 --height 40
   ```

2. **Slow, detailed observation**:
   ```bash
   python main.py --pattern toad --delay 1.0 --display color
   ```

3. **Large-scale glider gun simulation**:
   ```bash
   python main.py --auto --pattern gun --width 80 --height 40 --generations 100
   ```

## Project Structure

```
conways-game-of-life/
├── main.py              # Main application and game controller
├── game_of_life.py      # Core Game of Life logic and grid management
├── display.py           # Display systems (console and color)
├── patterns.py          # Classic pattern definitions and utilities
├── README.md           # This documentation file
└── .gitignore          # Git ignore patterns
```

### Module Overview

- **main.py**: Entry point, argument parsing, game controller, and user interface
- **game_of_life.py**: Core `GameOfLife` class with grid operations and rule logic
- **display.py**: `ConsoleDisplay` and `ColorConsoleDisplay` classes for visualization
- **patterns.py**: `Patterns` class with static methods for classic configurations

## Technical Details

### Grid Representation
- Uses a 2D list of boolean values
- Coordinate system: (0,0) at top-left, (width-1, height-1) at bottom-right
- Boundary cells are treated as permanently dead

### Performance Considerations
- Efficient neighbor counting with bounds checking
- Simultaneous rule application using separate grid buffers
- Memory usage scales linearly with grid size
- Typical performance: ~1000 generations/second on modern hardware

### Display Features
- **Console Mode**: Simple ASCII characters (█ for alive, space for dead)
- **Color Mode**: ANSI color codes for enhanced visualization
- **Cross-platform**: Works on Unix, Linux, macOS, and Windows
- **Responsive**: Real-time statistics and generation counting

## Contributing

Contributions are welcome! Here are some ways you can help:

1. **Bug Reports**: Report issues or unexpected behavior
2. **Feature Requests**: Suggest new features or improvements
3. **Pattern Library**: Add new classic patterns
4. **Display Options**: Implement new visualization modes
5. **Performance**: Optimize the core algorithm
6. **Documentation**: Improve or expand documentation

### Development Setup

1. Clone the repository
2. Make your changes
3. Test thoroughly with various patterns and configurations
4. Submit a pull request with a clear description

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Acknowledgments

- **John Horton Conway**: Creator of the Game of Life
- **Martin Gardner**: Popularized the Game of Life in Scientific American
- **LifeWiki**: Comprehensive resource for Game of Life patterns and information

---

**Enjoy exploring the fascinating world of Conway's Game of Life!** 🎮

For questions, suggestions, or discussions about cellular automata, feel free to open an issue or start a discussion.