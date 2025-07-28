from cube import RubiksCube
import random

class RubiksSolver:
    def __init__(self):
        self.solution_moves = []
    
    def scramble_cube(self, cube, num_moves=20):
        moves = ["U", "U'", "U2", "D", "D'", "D2", 
                "R", "R'", "R2", "L", "L'", "L2",
                "F", "F'", "F2", "B", "B'", "B2"]
        
        scramble_sequence = []
        for _ in range(num_moves):
            move = random.choice(moves)
            scramble_sequence.append(move)
            cube.execute_moves(move)
        
        return " ".join(scramble_sequence)
    
    def solve_white_cross(self, cube):
        moves = []
        print("Solving white cross...")
        
        white_edges = [
            ((0, 0, 1), (2, 2, 1)),
            ((0, 1, 2), (4, 2, 1)),
            ((0, 2, 1), (3, 2, 1)),
            ((0, 1, 0), (5, 2, 1)),
        ]
        
        for white_pos, adjacent_pos in white_edges:
            if (cube.cube[white_pos[0]][white_pos[1]][white_pos[2]] == 0 and
                cube.cube[adjacent_pos[0]][adjacent_pos[1]][adjacent_pos[2]] == adjacent_pos[0]):
                continue
                
            edge_moves = self._find_and_position_white_edge(cube, white_pos, adjacent_pos)
            moves.extend(edge_moves)
            
            for move in edge_moves:
                cube.execute_moves(move)
        
        print(f"White cross moves: {' '.join(moves)}")
        return moves
    
    def _find_and_position_white_edge(self, cube, target_white_pos, target_adjacent_pos):
        moves = []
        target_color = target_adjacent_pos[0]
        
        top_face = cube.cube[1]
        
        top_edges = [
            (1, 0, 1),
            (1, 1, 0),
            (1, 1, 2),
            (1, 2, 1),
        ]
        
        for edge_pos in top_edges:
            if cube.cube[edge_pos[0]][edge_pos[1]][edge_pos[2]] == 0:
                if edge_pos == (1, 0, 1):
                    moves.extend(["F", "F"])
                elif edge_pos == (1, 1, 0):
                    moves.extend(["L", "F", "L'"])
                elif edge_pos == (1, 1, 2):
                    moves.extend(["R'", "F'", "R"])
                elif edge_pos == (1, 2, 1):
                    moves.extend(["F'", "F'"])
                break
        
        return moves
    
    def solve_white_corners(self, cube):
        moves = []
        print("Solving white corners...")
        
        corner_positions = [
            ((0, 0, 0), (5, 2, 0), (2, 2, 0)),
            ((0, 0, 2), (2, 2, 2), (4, 2, 0)),
            ((0, 2, 2), (4, 2, 2), (3, 2, 2)),
            ((0, 2, 0), (3, 2, 0), (5, 2, 2)),
        ]
        
        for corner in corner_positions:
            if self._is_white_corner_solved(cube, corner):
                continue
            
            corner_moves = self._solve_white_corner_piece(cube, corner)
            moves.extend(corner_moves)
            
            for move in corner_moves:
                cube.execute_moves(move)
        
        print(f"White corners moves: {' '.join(moves)}")
        return moves
    
    def _is_white_corner_solved(self, cube, corner_positions):
        white_pos, side1_pos, side2_pos = corner_positions
        
        return (cube.cube[white_pos[0]][white_pos[1]][white_pos[2]] == 0 and
                cube.cube[side1_pos[0]][side1_pos[1]][side1_pos[2]] == side1_pos[0] and
                cube.cube[side2_pos[0]][side2_pos[1]][side2_pos[2]] == side2_pos[0])
    
    def _solve_white_corner_piece(self, cube, target_corner):
        moves = []
        
        max_attempts = 8
        attempts = 0
        
        while not self._is_white_corner_solved(cube, target_corner) and attempts < max_attempts:
            algorithm = ["R", "U", "R'", "U'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def solve_middle_edges(self, cube):
        moves = []
        print("Solving middle edges...")
        
        middle_edges = [
            ((2, 1, 2), (4, 1, 0)),
            ((4, 1, 2), (3, 1, 2)),
            ((3, 1, 0), (5, 1, 2)),
            ((5, 1, 0), (2, 1, 0)),
        ]
        
        for edge in middle_edges:
            if self._is_middle_edge_solved(cube, edge):
                continue
            
            edge_moves = self._solve_middle_edge_piece(cube, edge)
            moves.extend(edge_moves)
            
            for move in edge_moves:
                cube.execute_moves(move)
        
        print(f"Middle edges moves: {' '.join(moves)}")
        return moves
    
    def _is_middle_edge_solved(self, cube, edge_positions):
        pos1, pos2 = edge_positions
        return (cube.cube[pos1[0]][pos1[1]][pos1[2]] == pos1[0] and
                cube.cube[pos2[0]][pos2[1]][pos2[2]] == pos2[0])
    
    def _solve_middle_edge_piece(self, cube, target_edge):
        moves = []
        
        if not self._is_middle_edge_solved(cube, target_edge):
            right_hand = ["U", "R", "U'", "R'", "U'", "F'", "U", "F"]
            moves.extend(right_hand)
            
            if len(moves) < 16:
                left_hand = ["U'", "L'", "U", "L", "U", "F", "U'", "F'"]
                moves.extend(left_hand)
        
        return moves
    
    def solve_yellow_cross(self, cube):
        moves = []
        print("Solving yellow cross...")
        
        max_attempts = 4
        attempts = 0
        
        while not self._is_yellow_cross_formed(cube) and attempts < max_attempts:
            algorithm = ["F", "R", "U", "R'", "U'", "F'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        print(f"Yellow cross moves: {' '.join(moves)}")
        return moves
    
    def _is_yellow_cross_formed(self, cube):
        top_face = cube.cube[1]
        
        return (top_face[1][1] == 1 and
                top_face[0][1] == 1 and
                top_face[1][0] == 1 and
                top_face[1][2] == 1 and
                top_face[2][1] == 1)
    
    def solve_yellow_corners(self, cube):
        moves = []
        print("Solving yellow corners...")
        
        corner_orientation_moves = self._orient_yellow_corners(cube)
        moves.extend(corner_orientation_moves)
        
        for move in corner_orientation_moves:
            cube.execute_moves(move)
        
        corner_permutation_moves = self._permute_yellow_corners(cube)
        moves.extend(corner_permutation_moves)
        
        for move in corner_permutation_moves:
            cube.execute_moves(move)
        
        edge_permutation_moves = self._permute_last_layer_edges(cube)
        moves.extend(edge_permutation_moves)
        
        for move in edge_permutation_moves:
            cube.execute_moves(move)
        
        print(f"Yellow corners moves: {' '.join(moves)}")
        return moves
    
    def _orient_yellow_corners(self, cube):
        moves = []
        max_attempts = 8
        attempts = 0
        
        while not self._all_corners_yellow_on_top(cube) and attempts < max_attempts:
            algorithm = ["R", "U", "R'", "U'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def _permute_yellow_corners(self, cube):
        moves = []
        max_attempts = 4
        attempts = 0
        
        while not self._corners_in_correct_positions(cube) and attempts < max_attempts:
            algorithm = ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def _permute_last_layer_edges(self, cube):
        moves = []
        max_attempts = 4
        attempts = 0
        
        while not cube.is_solved() and attempts < max_attempts:
            algorithm = ["R", "U", "R'", "U", "R", "U2", "R'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def _all_corners_yellow_on_top(self, cube):
        top_face = cube.cube[1]
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        return all(top_face[r][c] == 1 for r, c in corners)
    
    def _corners_in_correct_positions(self, cube):
        return self._all_corners_yellow_on_top(cube)
    
    def solve(self, cube):
        if cube.is_solved():
            print("Cube is already solved!")
            return []
        
        print("Starting to solve the cube using beginner's method...")
        all_moves = []
        
        moves = self.solve_white_cross(cube)
        all_moves.extend(moves)
        cube.execute_moves(" ".join(moves))
        
        moves = self.solve_white_corners(cube)
        all_moves.extend(moves)
        cube.execute_moves(" ".join(moves))
        
        moves = self.solve_middle_edges(cube)
        all_moves.extend(moves)
        cube.execute_moves(" ".join(moves))
        
        moves = self.solve_yellow_cross(cube)
        all_moves.extend(moves)
        cube.execute_moves(" ".join(moves))
        
        moves = self.solve_yellow_corners(cube)
        all_moves.extend(moves)
        cube.execute_moves(" ".join(moves))
        
        return all_moves

if __name__ == "__main__":
    cube = RubiksCube()
    solver = RubiksSolver()
    
    print("=== RUBIK'S CUBE SOLVER TEST ===")
    print("\nInitial solved state:")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
    
    print("\n--- Scrambling cube ---")
    scramble = solver.scramble_cube(cube, 10)
    print(f"Scramble sequence: {scramble}")
    print("\nScrambled state:")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
    
    print("\n--- Attempting to solve ---")
    solution = solver.solve(cube)
    print(f"Solution found: {' '.join(solution)}")
    print(f"Final state - Is solved: {cube.is_solved()}")
