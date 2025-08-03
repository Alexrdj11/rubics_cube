"""
Utility functions for working with Rubik's Cube solver
"""

from cube import RubiksCube
from solver import RubiksSolver

def test_solve_simple():
    """Test the solver with a simple scramble."""
    cube = RubiksCube()
    scramble = "R U R' U'"
    
    print(f"Testing solver with scramble: {scramble}")
    cube.execute_moves(scramble)
    
    solver = RubiksSolver()
    solution = solver.solve(cube)
    
    print(f"Solved: {cube.is_solved()}")
    
    return cube.is_solved()

def benchmark_solver():
    """Benchmark the solver with various scrambles."""
    scrambles = [
        "R U R' U'",
        "F R U R' U' F'",
        "R U R' U R U2 R'",
        "R' F R F' R U2 R' U' R U' R'",
    ]
    
    results = []
    
    for scramble in scrambles:
        cube = RubiksCube()
        cube.execute_moves(scramble)
        
        solver = RubiksSolver()
        solution = solver.solve(cube)
        
        results.append({
            "scramble": scramble,
            "solved": cube.is_solved(),
            "solution_length": len(solution.split()) if isinstance(solution, str) else len(solution)
        })
    
    print("\nBenchmark Results:")
    print("-----------------")
    for result in results:
        status = "✅" if result["solved"] else "❌"
        print(f"{status} Scramble: {result['scramble']}")
        print(f"   Solution length: {result['solution_length']} moves")
    
    success_rate = sum(1 for r in results if r["solved"]) / len(results) * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")

def reverse_moves(moves_string):
    """Reverse a sequence of moves to undo them."""
    moves = moves_string.split()
    reversed_moves = []
    
    for move in reversed(moves):
        if move.endswith("'"):
            # Remove the prime and make it a normal move
            reversed_moves.append(move[0])
        elif move.endswith("2"):
            # Double moves are their own inverse
            reversed_moves.append(move)
        else:
            # Normal move becomes a prime
            reversed_moves.append(f"{move}'")
    
    return " ".join(reversed_moves)

def create_scrambled_cube(num_moves=20):
    """Create a scrambled cube with random moves.
    
    Args:
        num_moves: Number of random moves to apply
        
    Returns:
        tuple: (scrambled cube, list of moves applied)
    """
    import random
    
    cube = RubiksCube()
    
    # Available move types
    moves = ["U", "U'", "U2", "D", "D'", "D2", 
             "R", "R'", "R2", "L", "L'", "L2", 
             "F", "F'", "F2", "B", "B'", "B2"]
    
    # Generate random sequence of moves
    scramble_sequence = []
    for _ in range(num_moves):
        # Avoid immediate repetition of the same face
        if scramble_sequence and scramble_sequence[-1][0] == moves[0][0]:
            potential_moves = [m for m in moves if m[0] != scramble_sequence[-1][0]]
            move = random.choice(potential_moves)
        else:
            move = random.choice(moves)
        
        scramble_sequence.append(move)
        cube.execute_moves(move)
    
    return cube, scramble_sequence

def print_cube_simple(cube):
    """Print a simple text representation of the cube state."""
    color_map = {
        0: 'W',  # White
        1: 'Y',  # Yellow
        2: 'R',  # Red
        3: 'O',  # Orange
        4: 'B',  # Blue
        5: 'G',  # Green
    }
    
    face_names = ['Bottom (White)', 'Top (Yellow)', 'Front (Red)', 
                 'Back (Orange)', 'Right (Blue)', 'Left (Green)']
    
    for face_idx, face in enumerate(cube.cube):
        print(f"\n{face_names[face_idx]}:")
        for row in face:
            print(' '.join(color_map[cell] for cell in row))

def validate_moves_sequence(moves):
    """Validate that a move sequence contains only legal moves.
    
    Args:
        moves: String of moves separated by spaces
        
    Returns:
        bool: True if all moves are valid, False otherwise
    """
    valid_moves = [
        "U", "U'", "U2", "D", "D'", "D2", 
        "R", "R'", "R2", "L", "L'", "L2", 
        "F", "F'", "F2", "B", "B'", "B2",
        "M", "M'", "M2", "E", "E'", "E2", 
        "S", "S'", "S2"
    ]
    
    move_list = moves.strip().split()
    
    return all(move in valid_moves for move in move_list)

if __name__ == "__main__":
    print("Running cube utilities tests...")
    
    test_solve_simple()
    benchmark_solver()
    
    # Test move reversal
    moves = "R U R' F D2"
    reversed_moves = reverse_moves(moves)
    print(f"\nOriginal moves: {moves}")
    print(f"Reversed moves: {reversed_moves}")
    
    # Test if reversing works
    cube = RubiksCube()
    cube.execute_moves(moves)
    print("\nAfter original moves:")
    cube.display()
    
    cube.execute_moves(reversed_moves)
    print("\nAfter reversed moves (should be solved):")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
