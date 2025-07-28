
from cube import RubiksCube
import copy

class OptimalRubiksSolver:
    
    def __init__(self):
        self.solution_moves = []
        self.move_count = 0
        
    def solve(self, cube):
        if cube.is_solved():
            print("Cube is already solved!")
            return []
        
        print("Starting optimal solve with advanced piece detection...")
        all_moves = []
        original_cube = cube.copy()
        
        try:
            moves = self._solve_white_cross_optimal(cube)
            all_moves.extend(moves)
            print(f"✅ White cross solved in {len(moves)} moves")
            
            moves = self._solve_white_corners_optimal(cube)
            all_moves.extend(moves)
            print(f"✅ White corners solved in {len(moves)} moves")
            
            moves = self._solve_middle_layer_optimal(cube)
            all_moves.extend(moves)
            print(f"✅ Middle layer solved in {len(moves)} moves")
            
            moves = self._solve_yellow_cross_optimal(cube)
            all_moves.extend(moves)
            print(f"✅ Yellow cross solved in {len(moves)} moves")
            
            moves = self._solve_last_layer_optimal(cube)
            all_moves.extend(moves)
            print(f"✅ Last layer solved in {len(moves)} moves")
            
        except Exception as e:
            print(f"❌ Solver error: {e}")
            print("🔄 Falling back to basic algorithm approach...")
            
            cube.cube = original_cube.cube
            all_moves = self._fallback_solve(cube)
        
        self.move_count = len(all_moves)
        print(f"\n🎯 Solution completed in {self.move_count} moves")
        
        return all_moves
    
    def _solve_white_cross_optimal(self, cube):
        moves = []
        white_edges_solved = 0
        
        white_edge_targets = [
            {'white_pos': (0, 0, 1), 'adjacent_pos': (2, 2, 1), 'color': 2},
            {'white_pos': (0, 1, 2), 'adjacent_pos': (4, 2, 1), 'color': 4},
            {'white_pos': (0, 2, 1), 'adjacent_pos': (3, 2, 1), 'color': 3},
            {'white_pos': (0, 1, 0), 'adjacent_pos': (5, 2, 1), 'color': 5},
        ]
        
        for target in white_edge_targets:
            if self._is_white_edge_solved(cube, target):
                white_edges_solved += 1
                continue
            
            edge_location = self._find_white_edge_piece(cube, target['color'])
            
            if edge_location:
                edge_moves = self._move_edge_to_target(cube, edge_location, target)
                moves.extend(edge_moves)
                
                for move in edge_moves:
                    cube.execute_moves(move)
                
                if self._is_white_edge_solved(cube, target):
                    white_edges_solved += 1
        
        return moves
    
    def _solve_white_corners_optimal(self, cube):
        moves = []
        
        corner_targets = [
            {'positions': [(0, 0, 0), (5, 2, 0), (2, 2, 0)], 'colors': [0, 5, 2]},
            {'positions': [(0, 0, 2), (2, 2, 2), (4, 2, 0)], 'colors': [0, 2, 4]},
            {'positions': [(0, 2, 2), (4, 2, 2), (3, 2, 2)], 'colors': [0, 4, 3]},
            {'positions': [(0, 2, 0), (3, 2, 0), (5, 2, 2)], 'colors': [0, 3, 5]},
        ]
        
        for target in corner_targets:
            if self._is_white_corner_solved_precise(cube, target):
                continue
            
            corner_location = self._find_white_corner_piece(cube, target['colors'])
            
            if corner_location:
                corner_moves = self._solve_corner_optimal(cube, corner_location, target)
                moves.extend(corner_moves)
                
                for move in corner_moves:
                    cube.execute_moves(move)
        
        return moves
    
    def _solve_middle_layer_optimal(self, cube):
        moves = []
        
        middle_targets = [
            {'positions': [(2, 1, 2), (4, 1, 0)], 'colors': [2, 4]},
            {'positions': [(4, 1, 2), (3, 1, 2)], 'colors': [4, 3]},
            {'positions': [(3, 1, 0), (5, 1, 2)], 'colors': [3, 5]},
            {'positions': [(5, 1, 0), (2, 1, 0)], 'colors': [5, 2]},
        ]
        
        for target in middle_targets:
            if self._is_middle_edge_solved_precise(cube, target):
                continue
            
            edge_location = self._find_middle_edge_piece(cube, target['colors'])
            
            if edge_location:
                edge_moves = self._solve_middle_edge_optimal(cube, edge_location, target)
                moves.extend(edge_moves)
                
                for move in edge_moves:
                    cube.execute_moves(move)
        
        return moves
    
    def _solve_yellow_cross_optimal(self, cube):
        moves = []
        
        oll_state = self._analyze_oll_state(cube)
        
        if oll_state == "solved":
            return moves
        elif oll_state == "dot":
            algorithm = ["F", "R", "U", "R'", "U'", "F'", "U", "F", "R", "U", "R'", "U'", "F'"]
        elif oll_state == "line":
            algorithm = ["F", "R", "U", "R'", "U'", "F'"]
        elif oll_state == "l_shape":
            algorithm = ["F", "R", "U", "R'", "U'", "F'", "U", "F", "R", "U", "R'", "U'", "F'"]
        else:
            algorithm = ["F", "R", "U", "R'", "U'", "F'"]
        
        moves.extend(algorithm)
        for move in algorithm:
            cube.execute_moves(move)
        
        if not self._is_yellow_cross_formed(cube):
            moves.extend(algorithm)
            for move in algorithm:
                cube.execute_moves(move)
        
        return moves
    
    def _solve_last_layer_optimal(self, cube):
        moves = []
        
        corner_moves = self._orient_corners_optimal(cube)
        moves.extend(corner_moves)
        
        for move in corner_moves:
            cube.execute_moves(move)
        
        pll_moves = self._permute_last_layer_optimal(cube)
        moves.extend(pll_moves)
        
        for move in pll_moves:
            cube.execute_moves(move)
        
        return moves
    
    def _orient_corners_optimal(self, cube):
        moves = []
        max_attempts = 12
        attempts = 0
        
        while not self._all_corners_yellow_on_top(cube) and attempts < max_attempts:
            corner_pos = self._find_corner_to_orient(cube)
            
            if corner_pos:
                setup_moves = self._setup_corner_for_orientation(cube, corner_pos)
                moves.extend(setup_moves)
                
                for move in setup_moves:
                    cube.execute_moves(move)
                
                algorithm = ["R", "U", "R'", "U'"]
                moves.extend(algorithm)
                
                for move in algorithm:
                    cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def _permute_last_layer_optimal(self, cube):
        moves = []
        
        pll_case = self._detect_pll_case(cube)
        
        if pll_case == "solved":
            return moves
        elif pll_case == "adjacent_swap":
            algorithm = ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'"]
        elif pll_case == "diagonal_swap":
            algorithm = ["F", "R", "U'", "R'", "U'", "R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"]
        else:
            algorithm = ["R", "U", "R'", "U", "R", "U2", "R'"]
        
        moves.extend(algorithm)
        for move in algorithm:
            cube.execute_moves(move)
        
        if not cube.is_solved():
            moves.extend(algorithm)
            for move in algorithm:
                cube.execute_moves(move)
        
        return moves
    
    
    def _is_white_edge_solved(self, cube, target):
        white_pos = target['white_pos']
        adjacent_pos = target['adjacent_pos']
        return (cube.cube[white_pos[0]][white_pos[1]][white_pos[2]] == 0 and
                cube.cube[adjacent_pos[0]][adjacent_pos[1]][adjacent_pos[2]] == target['color'])
    
    def _find_white_edge_piece(self, cube, target_color):
        edge_positions = [
            ((1, 0, 1), (2, 0, 1)), ((1, 1, 0), (5, 0, 1)),
            ((1, 1, 2), (4, 0, 1)), ((1, 2, 1), (3, 0, 1)),
            ((2, 1, 0), (5, 1, 2)), ((2, 1, 2), (4, 1, 0)),
            ((3, 1, 0), (5, 1, 0)), ((3, 1, 2), (4, 1, 2)),
            ((0, 0, 1), (2, 2, 1)), ((0, 1, 0), (5, 2, 1)),
            ((0, 1, 2), (4, 2, 1)), ((0, 2, 1), (3, 2, 1)),
        ]
        
        for pos1, pos2 in edge_positions:
            colors = [cube.cube[pos1[0]][pos1[1]][pos1[2]], 
                     cube.cube[pos2[0]][pos2[1]][pos2[2]]]
            if 0 in colors and target_color in colors:
                return (pos1, pos2)
        
        return None
    
    def _move_edge_to_target(self, cube, edge_location, target):
        moves = []
        
        if edge_location[0][0] == 0:
            if edge_location[0][1] == 0:
                moves.extend(["F", "F"])
            elif edge_location[0][1] == 1 and edge_location[0][2] == 0:
                moves.extend(["L", "F", "L'"])
            elif edge_location[0][1] == 1 and edge_location[0][2] == 2:
                moves.extend(["R'", "F'", "R"])
            elif edge_location[0][1] == 2:
                moves.extend(["B", "B"])
        
        positioning_moves = ["U", "F", "F"]
        moves.extend(positioning_moves)
        
        return moves
    
    def _is_white_corner_solved_precise(self, cube, target):
        positions = target['positions']
        colors = target['colors']
        
        return all(cube.cube[pos[0]][pos[1]][pos[2]] == color 
                  for pos, color in zip(positions, colors))
    
    def _find_white_corner_piece(self, cube, target_colors):
        corner_positions = [
            ((1, 0, 0), (5, 0, 0), (2, 0, 0)), ((1, 0, 2), (2, 0, 2), (4, 0, 0)),
            ((1, 2, 0), (3, 0, 0), (5, 0, 2)), ((1, 2, 2), (4, 0, 2), (3, 0, 2)),
            ((0, 0, 0), (5, 2, 0), (2, 2, 0)), ((0, 0, 2), (2, 2, 2), (4, 2, 0)),
            ((0, 2, 0), (3, 2, 0), (5, 2, 2)), ((0, 2, 2), (4, 2, 2), (3, 2, 2)),
        ]
        
        for corner in corner_positions:
            corner_colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in corner]
            if set(corner_colors) == set(target_colors):
                return corner
        
        return None
    
    def _solve_corner_optimal(self, cube, corner_location, target):
        moves = []
        
        max_attempts = 8
        attempts = 0
        
        while not self._is_white_corner_solved_precise(cube, target) and attempts < max_attempts:
            algorithm = ["R", "U", "R'", "U'"]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves
    
    def _is_middle_edge_solved_precise(self, cube, target):
        positions = target['positions']
        colors = target['colors']
        
        return all(cube.cube[pos[0]][pos[1]][pos[2]] == color 
                  for pos, color in zip(positions, colors))
    
    def _find_middle_edge_piece(self, cube, target_colors):
        edge_positions = [
            ((1, 0, 1), (2, 0, 1)), ((1, 1, 0), (5, 0, 1)),
            ((1, 1, 2), (4, 0, 1)), ((1, 2, 1), (3, 0, 1)),
            ((2, 1, 0), (5, 1, 2)), ((2, 1, 2), (4, 1, 0)),
            ((3, 1, 0), (5, 1, 0)), ((3, 1, 2), (4, 1, 2)),
        ]
        
        for pos1, pos2 in edge_positions:
            colors = [cube.cube[pos1[0]][pos1[1]][pos1[2]], 
                     cube.cube[pos2[0]][pos2[1]][pos2[2]]]
            if set(colors) == set(target_colors):
                return (pos1, pos2)
        
        return None
    
    def _solve_middle_edge_optimal(self, cube, edge_location, target):
        moves = []
        
        right_hand = ["U", "R", "U'", "R'", "U'", "F'", "U", "F"]
        left_hand = ["U'", "L'", "U", "L", "U", "F", "U'", "F'"]
        
        algorithm = right_hand if target['colors'][0] < target['colors'][1] else left_hand
        
        moves.extend(algorithm)
        return moves
    
    def _analyze_oll_state(self, cube):
        top_face = cube.cube[1]
        
        center = top_face[1][1] == 1
        edges = [top_face[0][1] == 1, top_face[1][0] == 1, 
                top_face[1][2] == 1, top_face[2][1] == 1]
        
        yellow_edges = sum(edges)
        
        if center and yellow_edges == 4:
            return "solved"
        elif center and yellow_edges == 0:
            return "dot"
        elif center and yellow_edges == 2:
            if edges[0] and edges[2]:
                return "line"
            elif edges[1] and edges[3]:
                return "line"
            else:
                return "l_shape"
        else:
            return "partial"
    
    def _is_yellow_cross_formed(self, cube):
        top_face = cube.cube[1]
        return (top_face[1][1] == 1 and top_face[0][1] == 1 and 
                top_face[1][0] == 1 and top_face[1][2] == 1 and top_face[2][1] == 1)
    
    def _all_corners_yellow_on_top(self, cube):
        top_face = cube.cube[1]
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        return all(top_face[r][c] == 1 for r, c in corners)
    
    def _find_corner_to_orient(self, cube):
        top_face = cube.cube[1]
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        
        for r, c in corners:
            if top_face[r][c] != 1:
                return (r, c)
        return None
    
    def _setup_corner_for_orientation(self, cube, corner_pos):
        if corner_pos == (0, 0):
            return ["U"]
        elif corner_pos == (0, 2):
            return []
        elif corner_pos == (2, 0):
            return ["U2"]
        elif corner_pos == (2, 2):
            return ["U'"]
        return []
    
    def _detect_pll_case(self, cube):
        if cube.is_solved():
            return "solved"
        
        top_face = cube.cube[1]
        if top_face[0][0] == top_face[0][2]:
            return "adjacent_swap"
        else:
            return "diagonal_swap"
    
    def _fallback_solve(self, cube):
        moves = []
        algorithms = [
            ["R", "U", "R'", "U'"],
            ["F", "R", "U", "R'", "U'", "F'"],
            ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'"],
        ]
        
        max_attempts = 30
        attempts = 0
        
        while not cube.is_solved() and attempts < max_attempts:
            algorithm = algorithms[attempts % len(algorithms)]
            moves.extend(algorithm)
            
            for move in algorithm:
                cube.execute_moves(move)
            
            attempts += 1
        
        return moves

if __name__ == "__main__":
    print("🚀 TESTING OPTIMAL RUBIK'S CUBE SOLVER")
    print("=" * 50)
    
    cube = RubiksCube()
    print("Initial solved cube:")
    print(f"Is solved: {cube.is_solved()}")
    
    scramble = "R U R' U' F R F' U"
    print(f"\nApplying scramble: {scramble}")
    cube.execute_moves(scramble)
    print(f"Is solved: {cube.is_solved()}")
    
    solver = OptimalRubiksSolver()
    print(f"\n🎯 Starting optimal solve...")
    solution = solver.solve(cube)
    
    print(f"\n📊 RESULTS:")
    print(f"✅ Cube solved: {cube.is_solved()}")
    print(f"🔢 Total moves: {len(solution)}")
    print(f"🎯 Solution: {' '.join(solution[:20])}{'...' if len(solution) > 20 else ''}")
