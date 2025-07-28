
from cube import RubiksCube
import random

class AdvancedRubiksSolver:
    
    def __init__(self):
        self.solution_moves = []
    
    def solve(self, cube):
        if cube.is_solved():
            print("Cube is already solved!")
            return []
        
        print("Starting advanced solve...")
        all_moves = []
        
        max_attempts = 50
        attempts = 0
        
        common_algorithms = [
            "R U R' U'",
            "F R U R' U' F'",
            "R U R' F' R U R' U' R' F R2 U' R'",
            "R U R' U R U2 R'",
            "F' R U R' U' R' F R",
            "R U2 R' U' R U' R'",
        ]
        
        while not cube.is_solved() and attempts < max_attempts:
            algorithm = random.choice(common_algorithms)
            cube.execute_moves(algorithm)
            all_moves.extend(algorithm.split())
            attempts += 1
            
            if attempts % 10 == 0:
                print(f"Attempt {attempts}/50...")
        
        if cube.is_solved():
            print(f"🎉 Cube solved in {attempts} algorithm applications!")
            print(f"Total moves: {len(all_moves)}")
        else:
            print("⚠️ Could not solve with simple algorithm approach")
            print("This demonstrates the need for more sophisticated algorithms")
        
        return all_moves
    
    def scramble_and_solve_demo(self, scramble_moves=10):
        print("=== ADVANCED SOLVER DEMO ===")
        
        cube = RubiksCube()
        print("Initial solved cube:")
        cube.display()
        
        moves = ["U", "R", "F", "L", "B", "D"]
        scramble = []
        for _ in range(scramble_moves):
            move = random.choice(moves)
            if random.random() < 0.3:
                move += "'"
            elif random.random() < 0.2:
                move += "2"
            scramble.append(move)
        
        scramble_sequence = " ".join(scramble)
        print(f"\nApplying scramble: {scramble_sequence}")
        cube.execute_moves(scramble_sequence)
        
        print("Scrambled cube:")
        cube.display()
        print(f"Is solved: {cube.is_solved()}")
        
        print("\n--- Starting solve attempt ---")
        solution = self.solve(cube)
        
        print(f"\nFinal state:")
        cube.display()
        print(f"Is solved: {cube.is_solved()}")
        
        return solution

if __name__ == "__main__":
    solver = AdvancedRubiksSolver()
    solver.scramble_and_solve_demo(8)
