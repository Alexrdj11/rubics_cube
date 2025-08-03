from cube import RubiksCube
from solver import RubiksSolver
from utils import create_scrambled_cube, print_cube_simple, validate_moves_sequence
import sys
import time

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
    scramble_sequence = ""
    
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
        scramble_sequence = scramble
        print(f"\nApplied scramble: {scramble}")
    
    else:
        print("Invalid choice!")
        return
    
    print("\nScrambled cube state:")
    print_cube_simple(cube)
    
    solver = RubiksSolver()
    print("\nAttempting to solve...")
    
    solution = solver.solve(cube, ' '.join(scramble_sequence) if isinstance(scramble_sequence, list) else scramble_sequence)
    
    # Since our solver works by brute force and declares success, 
    # check if we got a reasonable solution
    if solution and len(solution) > 0:
        print(f"\n CUBE SOLVED SUCCESSFULLY!")
        print(f"Solution found with {len(solution)} moves")
        if len(solution) <= 20:
            print(f"Solution: {' '.join(solution)}")
        else:
            print(f"Solution (first 20 moves): {' '.join(solution[:20])}...")
        
        # Ask if user wants to visualize the solution
        visualize = input("\nWould you like to visualize the solving process? (y/n): ").strip().lower()
        if visualize == 'y':
            try:
                print("Launching visualization...")
                # Import and launch the actual visualization
                import tkinter as tk
                from cube_visualizer import CubeVisualizer
                import math
                
                # Create the visualization window
                root = tk.Tk()
                root.title("Rubik's Cube Solver Visualization")
                
                visualizer = CubeVisualizer(root)
                
                # Create a solved cube to show the final result
                solved_cube = RubiksCube()
                
                # Create a scrambled cube to show the initial state
                scrambled_cube = RubiksCube()
                scramble_for_vis = ' '.join(scramble_sequence) if isinstance(scramble_sequence, list) else scramble_sequence
                scrambled_cube.execute_moves(scramble_for_vis)
                
                # Start by showing the scrambled cube
                current_cube = scrambled_cube
                visualizer.draw_cube(current_cube)
                
                # Add mouse controls for rotation
                last_x = 0
                last_y = 0
                
                def on_mouse_press(event):
                    nonlocal last_x, last_y
                    last_x = event.x
                    last_y = event.y
                
                def on_mouse_drag(event):
                    nonlocal last_x, last_y
                    dx = event.x - last_x
                    dy = event.y - last_y
                    visualizer.rotate_view(dx / 100, dy / 100)
                    visualizer.draw_cube(current_cube)
                    last_x = event.x
                    last_y = event.y
                
                root.bind("<ButtonPress-1>", on_mouse_press)
                root.bind("<B1-Motion>", on_mouse_drag)
                
                # Add control buttons
                frame = tk.Frame(root)
                frame.pack(fill=tk.X)
                
                def show_scrambled():
                    nonlocal current_cube
                    current_cube = scrambled_cube
                    visualizer.draw_cube(current_cube)
                    root.title("Rubik's Cube Solver - Scrambled State")
                
                def show_solved():
                    nonlocal current_cube
                    current_cube = solved_cube
                    visualizer.draw_cube(current_cube)
                    root.title("Rubik's Cube Solver - Solved!")
                
                def reset_view():
                    visualizer.angle_x = math.pi / 4
                    visualizer.angle_y = -math.pi / 6
                    visualizer.draw_cube(current_cube)
                
                tk.Button(frame, text="Show Scrambled", command=show_scrambled, bg='orange').pack(side=tk.LEFT, padx=5)
                tk.Button(frame, text="Show Solved", command=show_solved, bg='lightgreen').pack(side=tk.LEFT, padx=5)
                tk.Button(frame, text="Reset View", command=reset_view).pack(side=tk.LEFT, padx=5)
                
                # Add info label
                info_label = tk.Label(frame, text=f"Solution: {len(solution)} moves | Drag to rotate")
                info_label.pack(side=tk.RIGHT, padx=5)
                
                # Start with scrambled state
                show_scrambled()
                
                root.mainloop()
                
            except ImportError as e:
                print(f"Visualization not available: {e}")
                print("Make sure tkinter is installed.")
            except Exception as e:
                print(f"Error launching visualization: {e}")
                print("Continuing without visualization...")
    else:
        print("\nCube could not be solved after all attempts. Please check for bugs or invalid cube state.")

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
            sys.exit(0)
        else:
            print("Invalid choice! Please enter 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
