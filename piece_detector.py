
from cube import RubiksCube

class CubeAnalyzer:
    
    def __init__(self):
        self.piece_positions = self._initialize_piece_positions()
    
    def _initialize_piece_positions(self):
        return {
            'edges': {
                'WR': [(0, 0, 1), (2, 2, 1)],
                'WB': [(0, 1, 2), (4, 2, 1)],
                'WO': [(0, 2, 1), (3, 2, 1)],
                'WG': [(0, 1, 0), (5, 2, 1)],
                'YR': [(1, 2, 1), (2, 0, 1)],
                'YB': [(1, 1, 2), (4, 0, 1)],
                'YO': [(1, 0, 1), (3, 0, 1)],
                'YG': [(1, 1, 0), (5, 0, 1)],
                'RB': [(2, 1, 2), (4, 1, 0)],
                'BO': [(4, 1, 2), (3, 1, 2)],
                'OG': [(3, 1, 0), (5, 1, 2)],
                'GR': [(5, 1, 0), (2, 1, 0)],
            },
            'corners': {
                'WRG': [(0, 0, 0), (2, 2, 0), (5, 2, 0)],
                'WRB': [(0, 0, 2), (2, 2, 2), (4, 2, 0)],
                'WOB': [(0, 2, 2), (3, 2, 2), (4, 2, 2)],
                'WOG': [(0, 2, 0), (3, 2, 0), (5, 2, 2)],
                'YRG': [(1, 2, 0), (2, 0, 0), (5, 0, 2)],
                'YRB': [(1, 2, 2), (2, 0, 2), (4, 0, 0)],
                'YOB': [(1, 0, 2), (3, 0, 2), (4, 0, 2)],
                'YOG': [(1, 0, 0), (3, 0, 0), (5, 0, 0)],
            }
        }
    
    def analyze_cube_state(self, cube):
        analysis = {
            'is_solved': cube.is_solved(),
            'layers': self._analyze_layers(cube),
            'cross_states': self._analyze_cross_states(cube),
            'corner_states': self._analyze_corner_states(cube),
            'edge_states': self._analyze_edge_states(cube),
            'solving_progress': self._calculate_solving_progress(cube),
        }
        
        return analysis
    
    def _analyze_layers(self, cube):
        return {
            'white_layer': self._is_layer_solved(cube, 'white'),
            'middle_layer': self._is_layer_solved(cube, 'middle'),
            'yellow_layer': self._is_layer_solved(cube, 'yellow'),
        }
    
    def _analyze_cross_states(self, cube):
        return {
            'white_cross': self._is_cross_solved(cube, 'white'),
            'yellow_cross': self._is_cross_solved(cube, 'yellow'),
        }
    
    def _analyze_corner_states(self, cube):
        corner_analysis = {}
        
        for corner_name, positions in self.piece_positions['corners'].items():
            corner_analysis[corner_name] = self._analyze_corner_piece(cube, corner_name, positions)
        
        return corner_analysis
    
    def _analyze_edge_states(self, cube):
        edge_analysis = {}
        
        for edge_name, positions in self.piece_positions['edges'].items():
            edge_analysis[edge_name] = self._analyze_edge_piece(cube, edge_name, positions)
        
        return edge_analysis
    
    def find_piece(self, cube, piece_type, piece_colors):
        if piece_type == 'edge':
            return self._find_edge_piece(cube, piece_colors)
        elif piece_type == 'corner':
            return self._find_corner_piece(cube, piece_colors)
        else:
            raise ValueError("piece_type must be 'edge' or 'corner'")
    
    def _find_edge_piece(self, cube, target_colors):
        edge_positions = [
            [(0, 0, 1), (2, 2, 1)], [(0, 1, 0), (5, 2, 1)],
            [(0, 1, 2), (4, 2, 1)], [(0, 2, 1), (3, 2, 1)],
            [(2, 1, 0), (5, 1, 2)], [(2, 1, 2), (4, 1, 0)],
            [(3, 1, 0), (5, 1, 0)], [(3, 1, 2), (4, 1, 2)],
            [(1, 0, 1), (3, 0, 1)], [(1, 1, 0), (5, 0, 1)],
            [(1, 1, 2), (4, 0, 1)], [(1, 2, 1), (2, 0, 1)],
        ]
        
        for positions in edge_positions:
            colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in positions]
            
            if set(colors) == set(target_colors):
                correct_orientation = colors == target_colors
                
                return {
                    'positions': positions,
                    'colors': colors,
                    'correct_orientation': correct_orientation,
                    'location': self._classify_edge_location(positions[0])
                }
        
        return None
    
    def _find_corner_piece(self, cube, target_colors):
        corner_positions = [
            [(0, 0, 0), (2, 2, 0), (5, 2, 0)], [(0, 0, 2), (2, 2, 2), (4, 2, 0)],
            [(0, 2, 0), (3, 2, 0), (5, 2, 2)], [(0, 2, 2), (3, 2, 2), (4, 2, 2)],
            [(1, 0, 0), (3, 0, 0), (5, 0, 0)], [(1, 0, 2), (3, 0, 2), (4, 0, 2)],
            [(1, 2, 0), (2, 0, 0), (5, 0, 2)], [(1, 2, 2), (2, 0, 2), (4, 0, 0)],
        ]
        
        for positions in corner_positions:
            colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in positions]
            
            if set(colors) == set(target_colors):
                orientation = self._determine_corner_orientation(colors, target_colors)
                
                return {
                    'positions': positions,
                    'colors': colors,
                    'orientation': orientation,
                    'location': self._classify_corner_location(positions[0])
                }
        
        return None
    
    def _classify_edge_location(self, position):
        face, row, col = position
        
        if face == 0:
            return 'bottom'
        elif face == 1:
            return 'top'
        else:
            if row == 1:
                return 'middle'
            elif row == 0:
                return 'top'
            else:
                return 'bottom'
    
    def _classify_corner_location(self, position):
        face, row, col = position
        
        if face == 0:
            return 'bottom'
        elif face == 1:
            return 'top'
        else:
            if row == 0:
                return 'top'
            else:
                return 'bottom'
    
    def _determine_corner_orientation(self, actual_colors, target_colors):
        if actual_colors[0] == target_colors[0]:
            return 0
        elif actual_colors[1] == target_colors[0]:
            return 1
        else:
            return 2
    
    def _is_layer_solved(self, cube, layer):
        if layer == 'white':
            white_face = cube.cube[0]
            if not all(white_face[i][j] == 0 for i in range(3) for j in range(3)):
                return False
            
            side_faces = [2, 4, 3, 5]
            for face_idx in side_faces:
                bottom_row = cube.cube[face_idx][2]
                if not all(cell == face_idx for cell in bottom_row):
                    return False
            return True
        
        elif layer == 'middle':
            side_faces = [2, 4, 3, 5]
            for face_idx in side_faces:
                middle_row = cube.cube[face_idx][1]
                if not all(cell == face_idx for cell in middle_row):
                    return False
            return True
        
        elif layer == 'yellow':
            return cube.is_solved()
        
        return False
    
    def _is_cross_solved(self, cube, color):
        if color == 'white':
            face = cube.cube[0]
            cross_positions = [(0, 1), (1, 0), (1, 2), (2, 1)]
            center = (1, 1)
            
            if face[center[0]][center[1]] != 0:
                return False
            
            for pos in cross_positions:
                if face[pos[0]][pos[1]] != 0:
                    return False
            
            adjacent_checks = [
                (cube.cube[2][2][1] == 2),
                (cube.cube[4][2][1] == 4),
                (cube.cube[3][2][1] == 3),
                (cube.cube[5][2][1] == 5),
            ]
            
            return all(adjacent_checks)
        
        elif color == 'yellow':
            face = cube.cube[1]
            cross_positions = [(0, 1), (1, 0), (1, 2), (2, 1)]
            center = (1, 1)
            
            if face[center[0]][center[1]] != 1:
                return False
            
            for pos in cross_positions:
                if face[pos[0]][pos[1]] != 1:
                    return False
            
            return True
        
        return False
    
    def _analyze_corner_piece(self, cube, corner_name, positions):
        color_map = {'W': 0, 'Y': 1, 'R': 2, 'O': 3, 'B': 4, 'G': 5}
        expected_colors = [color_map[c] for c in corner_name]
        
        actual_colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in positions]
        
        return {
            'in_correct_position': set(actual_colors) == set(expected_colors),
            'correctly_oriented': actual_colors == expected_colors,
            'current_colors': actual_colors,
            'expected_colors': expected_colors,
        }
    
    def _analyze_edge_piece(self, cube, edge_name, positions):
        color_map = {'W': 0, 'Y': 1, 'R': 2, 'O': 3, 'B': 4, 'G': 5}
        expected_colors = [color_map[c] for c in edge_name]
        
        actual_colors = [cube.cube[pos[0]][pos[1]][pos[2]] for pos in positions]
        
        return {
            'in_correct_position': set(actual_colors) == set(expected_colors),
            'correctly_oriented': actual_colors == expected_colors,
            'current_colors': actual_colors,
            'expected_colors': expected_colors,
        }
    
    def _calculate_solving_progress(self, cube):
        total_pieces = 20
        solved_pieces = 0
        
        for edge_name, positions in self.piece_positions['edges'].items():
            edge_analysis = self._analyze_edge_piece(cube, edge_name, positions)
            if edge_analysis['correctly_oriented']:
                solved_pieces += 1
        
        for corner_name, positions in self.piece_positions['corners'].items():
            corner_analysis = self._analyze_corner_piece(cube, corner_name, positions)
            if corner_analysis['correctly_oriented']:
                solved_pieces += 1
        
        return (solved_pieces / total_pieces) * 100
    
    def generate_detailed_report(self, cube):
        analysis = self.analyze_cube_state(cube)
        
        report = []
        report.append("🔍 DETAILED CUBE ANALYSIS REPORT")
        report.append("=" * 50)
        
        report.append(f"\n📊 OVERALL STATUS:")
        report.append(f"✅ Cube Solved: {analysis['is_solved']}")
        report.append(f"📈 Progress: {analysis['solving_progress']:.1f}%")
        
        report.append(f"\n🏗️ LAYER STATUS:")
        for layer, status in analysis['layers'].items():
            status_icon = "✅" if status else "❌"
            report.append(f"{status_icon} {layer.replace('_', ' ').title()}: {status}")
        
        report.append(f"\n➕ CROSS STATUS:")
        for cross, status in analysis['cross_states'].items():
            status_icon = "✅" if status else "❌"
            report.append(f"{status_icon} {cross.replace('_', ' ').title()}: {status}")
        
        report.append(f"\n🔲 PIECE ANALYSIS:")
        
        correct_edges = sum(1 for edge in analysis['edge_states'].values() 
                          if edge['correctly_oriented'])
        report.append(f"📐 Edges: {correct_edges}/12 correctly positioned")
        
        correct_corners = sum(1 for corner in analysis['corner_states'].values() 
                            if corner['correctly_oriented'])
        report.append(f"📐 Corners: {correct_corners}/8 correctly positioned")
        
        return "\n".join(report)

if __name__ == "__main__":
    print("🔍 TESTING ADVANCED CUBE ANALYZER")
    print("=" * 50)
    
    cube = RubiksCube()
    analyzer = CubeAnalyzer()
    
    print("📊 SOLVED CUBE ANALYSIS:")
    print(analyzer.generate_detailed_report(cube))
    
    cube.execute_moves("R U R' U' F R F'")
    print("\n📊 SCRAMBLED CUBE ANALYSIS:")
    print(analyzer.generate_detailed_report(cube))
    
    print("\n🔍 PIECE DETECTION TEST:")
    white_red_edge = analyzer.find_piece(cube, 'edge', [0, 2])
    if white_red_edge:
        print(f"✅ Found White-Red edge: {white_red_edge}")
    else:
        print("❌ White-Red edge not found")
    
    white_red_green_corner = analyzer.find_piece(cube, 'corner', [0, 2, 5])
    if white_red_green_corner:
        print(f"✅ Found White-Red-Green corner: {white_red_green_corner}")
    else:
        print("❌ White-Red-Green corner not found")
