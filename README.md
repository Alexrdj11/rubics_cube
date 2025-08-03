# Rubik's Cube Solver
A complete 3×3 Rubik's Cube solver with multiple algorithms and efficient implementation.
## Quick Start
### Run the Program
**Option 1: Interactive Mode (Recommended)**
```bash
python main.py
```

**Option 2: Full Demo**
```bash
python final_demo.py
```

**Option 3: Quick Test**
```bash
python utils.py
```

## File Structure

| File | Purpose | Usage |
|------|---------|-------|
| `main.py` | **Main app** | Interactive menu |
| `final_demo.py` | **Full demo** | Complete showcase |
| `cube.py` | Core cube logic | `python cube.py` |
| `solver.py` | Basic solver | `python solver.py` |
| `optimal_solver.py` | Advanced solver | `python optimal_solver.py` |
| `complete_solver.py` | Ultimate solver | `python complete_solver.py` |
| `piece_detector.py` | Piece tracking | Analysis functions |
| `utils.py` | Utilities | `python utils.py` |

## Features

- 18 complete moves (U, D, L, R, F, B + primes + doubles)  
- Multiple solving algorithms (basic to speedcubing)  
- Real-time state tracking and analysis  
- Efficient operations for all functions
- accurate move simulation
- 3D visualization of cube solving process

## Example

```python
from cube import RubiksCube
from solver import RubiksSolver

cube = RubiksCube()
cube.execute_moves("R U R' U' F R F'")
solver = RubiksSolver()
solution = solver.solve(cube)
```

## Project Overview

This Rubik's Cube solver provides a complete implementation that can solve a 3×3 Rubik's Cube from any scrambled state using standard cube moves.

## Implementation Details

### 1. Cube Representation

The cube is represented as a 3D array with 6 faces, each with a 3×3 grid:
- Face Indices: 0=White, 1=Yellow, 2=Red, 3=Orange, 4=Blue, 5=Green
- Colors are mapped to numerical values 0-5
- Memory Layout: `cube[face][row][col]` for efficient access

### 2. Move System

All 18 standard moves are implemented:
- Basic moves: U, D, L, R, F, B
- Prime (counterclockwise) versions: U', D', L', R', F', B'
- Double turns: U2, D2, L2, R2, F2, B2

### 3. Solving Algorithm

The solver uses a layer-by-layer approach with these steps:
1. White Cross
2. White Corners
3. Middle Edges
4. Yellow Cross
5. Yellow Corners

Advanced solvers use more sophisticated algorithms and piece detection.

### 4. Piece Detection

The `piece_detector.py` module provides detailed analysis:
- Edge and corner piece tracking
- Layer completion detection
- Solving progress calculation

## How to Run

### Main Application (Interactive)
```bash
python main.py
```
### Test Individual Components
```bash
# Test cube moves and representation
python cube.py

# Test basic layer-by-layer solver
python solver.py

# Test utilities and helper functions  
python utils.py

# Test advanced solver with piece detection
python optimal_solver.py

# Test comprehensive piece detection system
python piece_detector.py

# Test complete advanced solver with success tracking
python complete_solver.py

# Run comprehensive feature demonstration
python final_demo.py

# Run 3D cube visualization
python cube_visualizer.py
```

### Project Structure
```
aerohack/
├── main.py              # Interactive application
├── cube.py              # Cube representation and moves (18 moves)
├── solver.py            # Basic layer-by-layer solver
├── optimal_solver.py    # Advanced solver with piece detection
├── piece_detector.py    # Sophisticated piece detection system
├── complete_solver.py   # Complete solver with success tracking
├── utils.py             # Utility functions and testing
├── final_demo.py        # Comprehensive feature demonstration
├── cube_visualizer.py   # 3D visualization of cube solving
├── requirements.txt     # Dependencies (none required)
└── README.md            # This document
```

## Algorithm Capabilities

- **Basic Solver:** Complete layer-by-layer method (5 stages)
- **Optimal Solver:** Advanced piece detection + optimized algorithms
- **Complete Solver:** Full algorithm library + success rate tracking
- **Piece Detection:** Individual piece tracking and state analysis
- **Move System:** All 18 standard moves with perfect reversibility
- **State Analysis:** Comprehensive cube state evaluation

## Dependencies

The project uses only the Python standard library. No external dependencies are required for the basic implementation.

Optional dependencies for enhanced features:
- numpy (for potential performance optimizations)
- matplotlib (for additional visualization features)
- tkinter (included in standard Python installation, used for 3D visualization)
