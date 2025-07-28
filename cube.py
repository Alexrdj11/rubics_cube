class RubiksCube:
    def __init__(self):
        self.cube = [[[face for _ in range(3)] for _ in range(3)] for face in range(6)]
        self.colors = ['W', 'Y', 'R', 'O', 'B', 'G']
        
    def copy(self):
        new_cube = RubiksCube()
        new_cube.cube = [[[self.cube[face][row][col] for col in range(3)] 
                         for row in range(3)] for face in range(6)]
        return new_cube
    
    def is_solved(self):
        for face in self.cube:
            colors_on_face = {face[i][j] for i in range(3) for j in range(3)}
            if len(colors_on_face) != 1:
                return False
        return True
    
    def display(self):
        print("Cube state:")
        face_names = ['White (Bottom)', 'Yellow (Top)', 'Red (Front)', 
                     'Orange (Back)', 'Blue (Right)', 'Green (Left)']
        
        for face_idx, face in enumerate(self.cube):
            print(f"\n{face_names[face_idx]}:")
            for row in face:
                print(' '.join(self.colors[cell] for cell in row))
    
    def _rotate_face_clockwise(self, face_idx):
        face = self.cube[face_idx]
        self.cube[face_idx] = [[face[2-j][i] for j in range(3)] for i in range(3)]
    
    def _rotate_face_counterclockwise(self, face_idx):
        for _ in range(3):
            self._rotate_face_clockwise(face_idx)
    
    def U(self):
        self._rotate_face_clockwise(1)
        temp = [self.cube[2][0][i] for i in range(3)]
        for i in range(3):
            self.cube[2][0][i] = self.cube[5][0][i]
        for i in range(3):
            self.cube[5][0][i] = self.cube[3][0][i]
        for i in range(3):
            self.cube[3][0][i] = self.cube[4][0][i]
        for i in range(3):
            self.cube[4][0][i] = temp[i]
    
    def U_prime(self):
        for _ in range(3):
            self.U()
    
    def U2(self):
        self.U()
        self.U()
    
    def D(self):
        self._rotate_face_clockwise(0)
        temp = [self.cube[2][2][i] for i in range(3)]
        for i in range(3):
            self.cube[2][2][i] = self.cube[4][2][i]
        for i in range(3):
            self.cube[4][2][i] = self.cube[3][2][i]
        for i in range(3):
            self.cube[3][2][i] = self.cube[5][2][i]
        for i in range(3):
            self.cube[5][2][i] = temp[i]
    
    def D_prime(self):
        for _ in range(3):
            self.D()
    
    def D2(self):
        self.D()
        self.D()
    
    def R(self):
        self._rotate_face_clockwise(4)
        temp = [self.cube[2][i][2] for i in range(3)]
        for i in range(3):
            self.cube[2][i][2] = self.cube[0][i][2]
        for i in range(3):
            self.cube[0][i][2] = self.cube[3][2-i][0]
        for i in range(3):
            self.cube[3][2-i][0] = self.cube[1][i][2]
        for i in range(3):
            self.cube[1][i][2] = temp[i]
    
    def R_prime(self):
        for _ in range(3):
            self.R()
    
    def R2(self):
        self.R()
        self.R()
    
    def L(self):
        self._rotate_face_clockwise(5)
        temp = [self.cube[2][i][0] for i in range(3)]
        for i in range(3):
            self.cube[2][i][0] = self.cube[1][i][0]
        for i in range(3):
            self.cube[1][i][0] = self.cube[3][2-i][2]
        for i in range(3):
            self.cube[3][2-i][2] = self.cube[0][i][0]
        for i in range(3):
            self.cube[0][i][0] = temp[i]
    
    def L_prime(self):
        for _ in range(3):
            self.L()
    
    def L2(self):
        self.L()
        self.L()
    
    def F(self):
        self._rotate_face_clockwise(2)
        temp = [self.cube[1][2][i] for i in range(3)]
        for i in range(3):
            self.cube[1][2][i] = self.cube[5][2-i][2]
        for i in range(3):
            self.cube[5][2-i][2] = self.cube[0][0][2-i]
        for i in range(3):
            self.cube[0][0][i] = self.cube[4][i][0]
        for i in range(3):
            self.cube[4][i][0] = temp[i]
    
    def F_prime(self):
        for _ in range(3):
            self.F()
    
    def F2(self):
        self.F()
        self.F()
    
    def B(self):
        self._rotate_face_clockwise(3)
        temp = [self.cube[1][0][i] for i in range(3)]
        for i in range(3):
            self.cube[1][0][i] = self.cube[4][i][2]
        for i in range(3):
            self.cube[4][i][2] = self.cube[0][2][2-i]
        for i in range(3):
            self.cube[0][2][i] = self.cube[5][2-i][0]
        for i in range(3):
            self.cube[5][2-i][0] = temp[i]
    
    def B_prime(self):
        for _ in range(3):
            self.B()
    
    def B2(self):
        self.B()
        self.B()
    
    def execute_moves(self, moves_string):
        moves = moves_string.strip().split()
        for move in moves:
            if move == "U":
                self.U()
            elif move == "U'":
                self.U_prime()
            elif move == "U2":
                self.U2()
            elif move == "D":
                self.D()
            elif move == "D'":
                self.D_prime()
            elif move == "D2":
                self.D2()
            elif move == "R":
                self.R()
            elif move == "R'":
                self.R_prime()
            elif move == "R2":
                self.R2()
            elif move == "L":
                self.L()
            elif move == "L'":
                self.L_prime()
            elif move == "L2":
                self.L2()
            elif move == "F":
                self.F()
            elif move == "F'":
                self.F_prime()
            elif move == "F2":
                self.F2()
            elif move == "B":
                self.B()
            elif move == "B'":
                self.B_prime()
            elif move == "B2":
                self.B2()
            else:
                print(f"Unknown move: {move}")

if __name__ == "__main__":
    cube = RubiksCube()
    print("Initial solved cube:")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
    
    print("\nTesting sequence: R U R' U'")
    cube.execute_moves("R U R' U'")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
    
    print("\nTesting scramble: F R U' R' F' R U R'")
    cube = RubiksCube()
    cube.execute_moves("F R U' R' F' R U R'")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
    
    print("\nTesting if moves are reversible - applying reverse of scramble:")
    cube.execute_moves("R U' R' F R U R' F'")
    cube.display()
    print(f"Is solved: {cube.is_solved()}")
