from cube import RubiksCube
import random

def create_solved_cube():
    return RubiksCube()

def create_scrambled_cube(num_moves=20):
    cube = RubiksCube()
    moves = ["U", "U'", "U2", "D", "D'", "D2", 
            "R", "R'", "R2", "L", "L'", "L2",
            "F", "F'", "F2", "B", "B'", "B2"]
    
    scramble_sequence = []
    for _ in range(num_moves):
        move = random.choice(moves)
        scramble_sequence.append(move)
        cube.execute_moves(move)
    
    print(f"Scramble applied: {' '.join(scramble_sequence)}")
    return cube, scramble_sequence

def print_cube_simple(cube):
    print("\n    " + " ".join(cube.colors[cube.cube[1][0][i]] for i in range(3)))
    print("    " + " ".join(cube.colors[cube.cube[1][1][i]] for i in range(3)))
    print("    " + " ".join(cube.colors[cube.cube[1][2][i]] for i in range(3)))
    print()
    
    for row in range(3):
        line = ""
        for face in [5, 2, 4, 3]:
            line += " ".join(cube.colors[cube.cube[face][row][i]] for i in range(3)) + " "
        print(line)
    
    print()
    print("    " + " ".join(cube.colors[cube.cube[0][0][i]] for i in range(3)))
    print("    " + " ".join(cube.colors[cube.cube[0][1][i]] for i in range(3)))
    print("    " + " ".join(cube.colors[cube.cube[0][2][i]] for i in range(3)))

def validate_moves_sequence(moves_string):
    valid_moves = {"U", "U'", "U2", "D", "D'", "D2", 
                  "R", "R'", "R2", "L", "L'", "L2",
                  "F", "F'", "F2", "B", "B'", "B2"}
    
    moves = moves_string.strip().split()
    for move in moves:
        if move not in valid_moves:
            print(f"Invalid move: {move}")
            return False
    return True

def test_move_reversibility():
    print("Testing move reversibility...")
    cube = RubiksCube()
    
    moves_to_test = ["U", "D", "R", "L", "F", "B"]
    
    for move in moves_to_test:
        original_state = cube.copy()
        
        cube.execute_moves(f"{move} {move}'")
        
        if cube.cube == original_state.cube:
            print(f"✓ {move} and {move}' are properly reversible")
        else:
            print(f"✗ {move} and {move}' are NOT properly reversible")
    
    print("Move reversibility test completed.")

def benchmark_moves(num_iterations=1000):
    import time
    
    cube = RubiksCube()
    moves = "R U R' U' R U R' U' R U R' U'"
    
    start_time = time.time()
    for _ in range(num_iterations):
        cube.execute_moves(moves)
    end_time = time.time()
    
    total_moves = len(moves.split()) * num_iterations
    moves_per_second = total_moves / (end_time - start_time)
    
    print(f"Executed {total_moves} moves in {end_time - start_time:.4f} seconds")
    print(f"Speed: {moves_per_second:.0f} moves per second")

if __name__ == "__main__":
    print("=== RUBIK'S CUBE UTILITIES DEMO ===")
    
    print("\n1. Creating solved cube:")
    cube = create_solved_cube()
    print_cube_simple(cube)
    
    print("\n2. Creating scrambled cube:")
    scrambled_cube, scramble = create_scrambled_cube(8)
    print_cube_simple(scrambled_cube)
    
    print("\n3. Testing move validation:")
    valid_sequence = "R U R U'"
    print(f"Valid sequence '{valid_sequence}': {validate_moves_sequence(valid_sequence)}")
    print(f"Invalid sequence 'R X U': {validate_moves_sequence('R X U')}")
    
    print("\n4. Testing move reversibility:")
    test_move_reversibility()
    
    print("\n5. Benchmarking moves:")
    benchmark_moves(100)
