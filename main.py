from cube import RubiksCube
from solver import RubiksSolver
from utils import create_scrambled_cube, print_cube_simple, validate_moves_sequence
import sys

def main_menu():
    print("\n" + "="*50)
    print("       RUBIK'S CUBE SOLVER")
    print("="*50)
    print("1. Solve a scrambled cube")
    print("2. Apply custom moves to cube")
    print("3. Test cube moves")
    print("4. Generate random scramble")
    print("5. Exit")
    print("="*50)
    
    choice = input("Enter your choice (1-5): ").strip()
    return choice

def solve_scrambled_cube():
    print("\n--- SOLVE A SCRAMBLED CUBE ---")
    
    print("1. Generate random scramble")
    print("2. Enter custom scramble sequence")
    
    scramble_choice = input("Choose scramble method (1-2): ").strip()
    
    if scramble_choice == "1":
        num_moves = input("Number of scramble moves (default 15): ").strip()
        num_moves = int(num_moves) if num_moves.isdigit() else 15
        
        cube, scramble_sequence = create_scrambled_cube(num_moves)
        print(f"\nGenerated scramble: {' '.join(scramble_sequence)}")
        
    elif scramble_choice == "2":
        scramble = input("Enter scramble sequence (e.g., 'R U R' U' F R F'): ").strip()
        
        if not validate_moves_sequence(scramble):
            print("Invalid scramble sequence!")
            return
        
        cube = RubiksCube()
        cube.execute_moves(scramble)
        print(f"\nApplied scramble: {scramble}")
    
    else:
        print("Invalid choice!")
        return
    
    print("\nScrambled cube state:")
    print_cube_simple(cube)
    
    solver = RubiksSolver()
    print("\nAttempting to solve...")
    
    solution = solver.solve(cube)
    
    if cube.is_solved():
        print(f"\n🎉 CUBE SOLVED! 🎉")
        print(f"Solution: {' '.join(solution)}")
    else:
        print("\n⚠️  Solver is not yet fully implemented.")
        print("This is a placeholder - the actual solving algorithms need to be completed.")

def apply_custom_moves():
    print("\n--- APPLY CUSTOM MOVES ---")
    
    cube = RubiksCube()
    print("Starting with solved cube:")
    print_cube_simple(cube)
    
    while True:
        moves = input("\nEnter moves (or 'quit' to exit, 'reset' for solved cube): ").strip()
        
        if moves.lower() == 'quit':
            break
        elif moves.lower() == 'reset':
            cube = RubiksCube()
            print("Cube reset to solved state.")
            print_cube_simple(cube)
            continue
        
        if not validate_moves_sequence(moves):
            print("Invalid move sequence! Use moves like: U, R, F, L, B, D (with ', 2 variants)")
            continue
        
        cube.execute_moves(moves)
        print(f"\nApplied moves: {moves}")
        print_cube_simple(cube)
        print(f"Is solved: {cube.is_solved()}")

def test_cube_moves():
    print("\n--- TEST CUBE MOVES ---")
    
    cube = RubiksCube()
    
    test_sequences = [
        "R U R' U'",
        "F R U' R' F'",
        "R U R' F' R U R' U' R' F R2 U' R'",
        "M U M' U2 M U M'"
    ]
    
    print("Testing common move sequences:")
    
    for i, sequence in enumerate(test_sequences[:3], 1):
        print(f"\n{i}. Testing: {sequence}")
        test_cube = cube.copy()
        test_cube.execute_moves(sequence)
        print_cube_simple(test_cube)
        print(f"Is solved: {test_cube.is_solved()}")

def generate_scramble():
    print("\n--- GENERATE RANDOM SCRAMBLE ---")
    
    num_moves = input("Number of moves (default 20): ").strip()
    num_moves = int(num_moves) if num_moves.isdigit() else 20
    
    cube, scramble_sequence = create_scrambled_cube(num_moves)
    
    print(f"\nGenerated scramble: {' '.join(scramble_sequence)}")
    print("\nScrambled cube state:")
    print_cube_simple(cube)

def main():
    print("Welcome to the Rubik's Cube Solver!")
    print("This implementation follows the step-by-step guide.")
    
    while True:
        choice = main_menu()
        
        if choice == "1":
            solve_scrambled_cube()
        elif choice == "2":
            apply_custom_moves()
        elif choice == "3":
            test_cube_moves()
        elif choice == "4":
            generate_scramble()
        elif choice == "5":
            print("\nThanks for using the Rubik's Cube Solver!")
            print("The solving algorithms are placeholders - implement them to complete the solver!")
            sys.exit(0)
        else:
            print("Invalid choice! Please enter 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
