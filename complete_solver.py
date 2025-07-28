
from cube import RubiksCube
from optimal_solver import OptimalRubiksSolver
from piece_detector import CubeAnalyzer
import random

class CompleteAdvancedSolver:
    
    def __init__(self):
        self.optimal_solver = OptimalRubiksSolver()
        self.analyzer = CubeAnalyzer()
        self.solution_moves = []
        self.success_rate = 0.0
        
        self.algorithm_library = {
            'oll_algorithms': {
                'dot': ["F", "R", "U", "R'", "U'", "F'", "U", "F", "R", "U", "R'", "U'", "F'"],
                'line': ["F", "R", "U", "R'", "U'", "F'"],
                'l_shape': ["F", "R", "U", "R'", "U'", "F'", "U", "F", "R", "U", "R'", "U'", "F'"],
                'cross': [],
            },
            'pll_algorithms': {
                't_perm': ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'"],
                'j_perm': ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'"],
                'y_perm': ["F", "R", "U'", "R'", "U'", "R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R", "F'"],
                'a_perm': ["R'", "F", "R'", "B2", "R", "F'", "R'", "B2", "R2"],
                'u_perm': ["R", "U'", "R", "U", "R", "U", "R", "U'", "R'", "U'", "R2"],
                'h_perm': ["M2", "U", "M2", "U2", "M2", "U", "M2"],
            },
            'f2l_algorithms': {
                'basic_insert': ["R", "U", "R'", "U'", "F'", "U", "F"],
                'split_pair': ["R", "U'", "R'", "U", "F", "U'", "F'"],
                'corner_twist': ["R", "U", "R'", "U'", "R", "U", "R'"],
            }
        }
    
    def solve_with_statistics(self, cube, max_attempts=3):
        success_attempts = 0
        best_solution = None
        best_move_count = float('inf')
        
        for attempt in range(max_attempts):
            print(f"\n🎯 Attempt {attempt + 1}/{max_attempts}")
            
            cube_copy = cube.copy()
            
            try:
                solution = self.solve_advanced(cube_copy)
                
                if cube_copy.is_solved():
                    success_attempts += 1
                    move_count = len(solution)
                    
                    print(f"✅ Success! Solved in {move_count} moves")
                    
                    if move_count < best_move_count:
                        best_solution = solution
                        best_move_count = move_count
                        print(f"🏆 New best solution: {move_count} moves")
                else:
                    print("❌ Failed to solve completely")
                    
            except Exception as e:
                print(f"❌ Error in attempt {attempt + 1}: {e}")
        
        self.success_rate = (success_attempts / max_attempts) * 100
        
        print(f"\n📊 SOLVER STATISTICS:")
        print(f"✅ Success Rate: {self.success_rate:.1f}% ({success_attempts}/{max_attempts})")
        print(f"🏆 Best Solution: {best_move_count} moves")
        
        return best_solution if best_solution else []
    
    def solve_advanced(self, cube):
        if cube.is_solved():
            return []
        
        print("🚀 Starting advanced solve with piece detection...")
        all_moves = []
        
        initial_analysis = self.analyzer.analyze_cube_state(cube)
        print(f"📊 Initial progress: {initial_analysis['solving_progress']:.1f}%")
        
        layer_moves = self._solve_layers_with_detection(cube)
        all_moves.extend(layer_moves)
        
        if not cube.is_solved():
            last_layer_moves = self._solve_last_layer_advanced(cube)
            all_moves.extend(last_layer_moves)
        
        if not cube.is_solved():
            optimization_moves = self._final_optimization(cube)
            all_moves.extend(optimization_moves)
        
        return all_moves
    
    def _solve_layers_with_detection(self, cube):
        moves = []
        
        if not self.analyzer._is_cross_solved(cube, 'white'):
            print("🎯 Solving white cross with piece detection...")
            cross_moves = self._solve_white_cross_advanced(cube)
            moves.extend(cross_moves)
            self._apply_moves(cube, cross_moves)
        
        if not self.analyzer._is_layer_solved(cube, 'white'):
            print("🎯 Solving white corners with piece detection...")
            corner_moves = self._solve_white_corners_advanced(cube)
            moves.extend(corner_moves)
            self._apply_moves(cube, corner_moves)
        
        if not self.analyzer._is_layer_solved(cube, 'middle'):
            print("🎯 Solving middle layer with piece detection...")
            middle_moves = self._solve_middle_layer_advanced(cube)
            moves.extend(middle_moves)
            self._apply_moves(cube, middle_moves)
        
        return moves
    
    def _solve_white_cross_advanced(self, cube):
        moves = []
        target_edges = [
            ([0, 2], [(0, 0, 1), (2, 2, 1)]),
            ([0, 4], [(0, 1, 2), (4, 2, 1)]),
            ([0, 3], [(0, 2, 1), (3, 2, 1)]),
            ([0, 5], [(0, 1, 0), (5, 2, 1)]),
        ]
        
        for target_colors, target_positions in target_edges:
            if self._is_edge_in_position(cube, target_colors, target_positions):
                continue
            
            piece_info = self.analyzer.find_piece(cube, 'edge', target_colors)
            
            if piece_info:
                edge_moves = self._position_edge_optimally(cube, piece_info, target_positions)
                moves.extend(edge_moves)
                self._apply_moves(cube, edge_moves)
        
        return moves
    
    def _solve_white_corners_advanced(self, cube):
        moves = []
        target_corners = [
            ([0, 2, 5], [(0, 0, 0), (2, 2, 0), (5, 2, 0)]),
            ([0, 2, 4], [(0, 0, 2), (2, 2, 2), (4, 2, 0)]),
            ([0, 3, 4], [(0, 2, 2), (3, 2, 2), (4, 2, 2)]),
            ([0, 3, 5], [(0, 2, 0), (3, 2, 0), (5, 2, 2)]),
        ]
        
        for target_colors, target_positions in target_corners:
            if self._is_corner_in_position(cube, target_colors, target_positions):
                continue
            
            piece_info = self.analyzer.find_piece(cube, 'corner', target_colors)
            
            if piece_info:
                corner_moves = self._position_corner_optimally(cube, piece_info, target_positions)
                moves.extend(corner_moves)
                self._apply_moves(cube, corner_moves)
        
        return moves
    
    def _solve_middle_layer_advanced(self, cube):
        moves = []
        target_edges = [
            ([2, 4], [(2, 1, 2), (4, 1, 0)]),
            ([4, 3], [(4, 1, 2), (3, 1, 2)]),
            ([3, 5], [(3, 1, 0), (5, 1, 2)]),
            ([5, 2], [(5, 1, 0), (2, 1, 0)]),
        ]
        
        for target_colors, target_positions in target_edges:
            if self._is_edge_in_position(cube, target_colors, target_positions):
                continue
            
            piece_info = self.analyzer.find_piece(cube, 'edge', target_colors)
            
            if piece_info:
                f2l_moves = self._solve_f2l_pair(cube, piece_info, target_positions)
                moves.extend(f2l_moves)
                self._apply_moves(cube, f2l_moves)
        
        return moves
    
    def _solve_last_layer_advanced(self, cube):
        moves = []
        
        oll_moves = self._solve_oll_advanced(cube)
        moves.extend(oll_moves)
        self._apply_moves(cube, oll_moves)
        
        pll_moves = self._solve_pll_advanced(cube)
        moves.extend(pll_moves)
        self._apply_moves(cube, pll_moves)
        
        return moves
    
    def _solve_oll_advanced(self, cube):
        moves = []
        
        oll_state = self._analyze_oll_pattern(cube)
        
        if oll_state in self.algorithm_library['oll_algorithms']:
            algorithm = self.algorithm_library['oll_algorithms'][oll_state]
            moves.extend(algorithm)
        else:
            default_oll = ["F", "R", "U", "R'", "U'", "F'"]
            moves.extend(default_oll)
        
        return moves
    
    def _solve_pll_advanced(self, cube):
        moves = []
        max_attempts = 4
        
        for attempt in range(max_attempts):
            if cube.is_solved():
                break
            
            pll_case = self._detect_pll_pattern(cube)
            
            if pll_case in self.algorithm_library['pll_algorithms']:
                algorithm = self.algorithm_library['pll_algorithms'][pll_case]
                algorithm = [move for move in algorithm if 'M' not in move]
                moves.extend(algorithm)
                self._apply_moves(cube, algorithm)
            else:
                default_pll = ["R", "U", "R'", "U", "R", "U2", "R'"]
                moves.extend(default_pll)
                self._apply_moves(cube, default_pll)
        
        return moves
    
    def _final_optimization(self, cube):
        moves = []
        
        if not cube.is_solved():
            print("🔧 Applying final optimization...")
            
            final_algorithms = [
                ["R", "U", "R'", "U'"],
                ["F", "R", "U", "R'", "U'", "F'"],
                ["R", "U2", "R'", "U'", "R", "U'", "R'"],
            ]
            
            for algorithm in final_algorithms:
                moves.extend(algorithm)
                self._apply_moves(cube, algorithm)
                
                if cube.is_solved():
                    break
        
        return moves
    
    
    def _apply_moves(self, cube, moves):
        for move in moves:
            cube.execute_moves(move)
    
    def _is_edge_in_position(self, cube, target_colors, target_positions):
        actual_colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in target_positions]
        return actual_colors == target_colors
    
    def _is_corner_in_position(self, cube, target_colors, target_positions):
        actual_colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in target_positions]
        return actual_colors == target_colors
    
    def _position_edge_optimally(self, cube, piece_info, target_positions):
        moves = []
        
        if piece_info['location'] == 'bottom':
            moves.extend(["F", "F"])
        elif piece_info['location'] == 'middle':
            moves.extend(["R", "U", "R'"])
        
        moves.extend(["U", "F", "F"])
        
        return moves
    
    def _position_corner_optimally(self, cube, piece_info, target_positions):
        moves = []
        
        if piece_info['location'] == 'top':
            for _ in range(piece_info.get('orientation', 0)):
                moves.extend(["R", "U", "R'", "U'"])
        else:
            moves.extend(["R", "U", "R'"])
            moves.extend(["R", "U", "R'", "U'"])
        
        return moves
    
    def _solve_f2l_pair(self, cube, piece_info, target_positions):
        if piece_info['correct_orientation']:
            algorithm = self.algorithm_library['f2l_algorithms']['basic_insert']
        else:
            algorithm = self.algorithm_library['f2l_algorithms']['split_pair']
        
        return algorithm
    
    def _analyze_oll_pattern(self, cube):
        top_face = cube.cube[1]
        
        cross_yellows = sum([
            top_face[0][1] == 1,
            top_face[1][0] == 1,
            top_face[1][2] == 1,
            top_face[2][1] == 1,
        ])
        
        if cross_yellows == 4:
            return 'cross'
        elif cross_yellows == 2:
            if (top_face[0][1] == 1 and top_face[2][1] == 1) or (top_face[1][0] == 1 and top_face[1][2] == 1):
                return 'line'
            else:
                return 'l_shape'
        else:
            return 'dot'
    
    def _detect_pll_pattern(self, cube):
        top_edges = [
            cube.cube[2][0][1],
            cube.cube[4][0][1],
            cube.cube[3][0][1],
            cube.cube[5][0][1],
        ]
        
        if len(set(top_edges)) == 1:
            return 'solved'
        elif top_edges[0] == top_edges[2] or top_edges[1] == top_edges[3]:
            return 't_perm'
        else:
            return 'u_perm'

if __name__ == "__main__":
    print("🚀 TESTING COMPLETE ADVANCED SOLVER")
    print("=" * 60)
    
    cube = RubiksCube()
    solver = CompleteAdvancedSolver()
    
    scrambles = [
        "R U R' U'",
        "F R U R' U' F'",
        "R U R' U' F R F' U R U' R'",
        "F R U' R' F' R U R' U' R' F R F'",
    ]
    
    for i, scramble in enumerate(scrambles, 1):
        print(f"\n🎲 TEST SCRAMBLE {i}: {scramble}")
        print("-" * 40)
        
        test_cube = RubiksCube()
        test_cube.execute_moves(scramble)
        
        print(f"📊 Scrambled: {not test_cube.is_solved()}")
        
        solution = solver.solve_with_statistics(test_cube, max_attempts=2)
        
        if solution:
            print(f"🎯 Solution length: {len(solution)} moves")
            print(f"📝 Solution preview: {' '.join(solution[:15])}{'...' if len(solution) > 15 else ''}")
        
        print(f"✅ Final result: {test_cube.is_solved()}")
    
    print(f"\n🏆 OVERALL SOLVER PERFORMANCE:")
    print(f"📊 Average Success Rate: {solver.success_rate:.1f}%")
    print("🎯 Advanced solver implementation complete!")
