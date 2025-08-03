import tkinter as tk
import time
import math
from cube import RubiksCube

class CubeVisualizer:
    def __init__(self, root, size=500):
        self.root = root
        self.size = size
        self.canvas = tk.Canvas(root, width=size, height=size, bg='black')
        self.canvas.pack()

        # Colors for the cube faces
        self.colors = {
            0: '#FFFFFF',  # White
            1: '#FFFF00',  # Yellow
            2: '#FF0000',  # Red
            3: '#FFA500',  # Orange
            4: '#0000FF',  # Blue
            5: '#00FF00',  # Green
        }
        
        # Coordinates for 3D cube
        self.angle_x = math.pi / 4
        self.angle_y = -math.pi / 6
        self.angle_z = 0
        
        # Cube parameters
        self.cube_size = size * 0.4
        self.piece_size = self.cube_size / 3
        
        # Create cube objects
        self.facets = {}
        
        # Delay between moves (in seconds)
        self.move_delay = 0.5
        
    def _make_white_cross_cube(self, cube):
        """Create a cube with just the white cross solved"""
        # White face
        cube.cube[0][0][1] = 0  # Top edge
        cube.cube[0][1][0] = 0  # Left edge
        cube.cube[0][1][1] = 0  # Center
        cube.cube[0][1][2] = 0  # Right edge
        cube.cube[0][2][1] = 0  # Bottom edge

        # Set side colors for the white cross edges
        cube.cube[2][2][1] = 2  # Red on front face
        cube.cube[3][2][1] = 3  # Orange on back face  
        cube.cube[4][2][1] = 4  # Blue on right face
        cube.cube[5][2][1] = 5  # Green on left face

        # Scramble the rest
        self._scramble_non_cross_pieces(cube)

    def _make_first_layer_cube(self, cube):
        """Create a cube with the first layer solved"""
        # Complete white face
        for row in range(3):
            for col in range(3):
                cube.cube[0][row][col] = 0  # All white

        # Set the bottom row of each side face
        for face in [2, 3, 4, 5]:  # Front, Back, Right, Left
            for col in range(3):
                cube.cube[face][2][col] = face

        # Scramble the rest
        self._scramble_upper_layers(cube)

    def _make_second_layer_cube(self, cube):
        """Create a cube with the first two layers solved"""
        # First layer is already solved
        self._make_first_layer_cube(cube)

        # Set the middle row of each side face
        for face in [2, 3, 4, 5]:  # Front, Back, Right, Left
            for col in range(3):
                cube.cube[face][1][col] = face

        # Scramble the top layer
        self._scramble_top_layer(cube)

    def _make_top_cross_cube(self, cube):
        """Create a cube with the first two layers and top cross solved"""
        # First and second layers solved
        self._make_second_layer_cube(cube)

        # Yellow cross on top
        cube.cube[1][0][1] = 1  # Top edge
        cube.cube[1][1][0] = 1  # Left edge
        cube.cube[1][1][1] = 1  # Center
        cube.cube[1][1][2] = 1  # Right edge
        cube.cube[1][2][1] = 1  # Bottom edge

        # Top rows of side faces still scrambled
        self._scramble_top_layer_edges(cube)

    def _make_oll_cube(self, cube):
        """Create a cube with the first two layers and top face oriented correctly"""
        # Previous steps solved
        self._make_top_cross_cube(cube)

        # Full yellow face on top
        for row in range(3):
            for col in range(3):
                cube.cube[1][row][col] = 1

        # Top rows of side faces still not correctly permuted
        self._scramble_top_layer_edges_keep_yellow(cube)
        
    def _scramble_non_cross_pieces(self, cube):
        """Scramble all pieces except the white cross"""
        # Scramble corners of the white face
        cube.cube[0][0][0] = 3  # Top-left
        cube.cube[0][0][2] = 5  # Top-right
        cube.cube[0][2][0] = 2  # Bottom-left
        cube.cube[0][2][2] = 4  # Bottom-right
        
        # Scramble most of yellow face
        for row in range(3):
            for col in range(3):
                if not (row == 1 and col == 1):  # Preserve center
                    cube.cube[1][row][col] = (row + col) % 5 + 1
                    
        # Scramble middle and top layers of side faces
        colors = [2, 3, 4, 5]  # Red, Orange, Blue, Green
        for face in range(2, 6):
            for row in range(2):  # Top and middle rows
                for col in range(3):
                    if not (row == 2 and col == 1):  # Preserve cross piece
                        cube.cube[face][row][col] = colors[(face + row + col) % 4]
    
    def _scramble_upper_layers(self, cube):
        """Scramble second and top layer after first layer is solved"""
        colors = [1, 2, 3, 4, 5]  # Yellow, Red, Orange, Blue, Green
        
        # Scramble yellow face
        for row in range(3):
            for col in range(3):
                if not (row == 1 and col == 1):  # Preserve center
                    cube.cube[1][row][col] = colors[(row + col) % 5]
        
        # Scramble middle and top rows of side faces
        for face in range(2, 6):
            for row in range(2):  # Top and middle rows
                for col in range(3):
                    cube.cube[face][row][col] = colors[(face + row + col) % 5]
    
    def _scramble_top_layer(self, cube):
        """Scramble just the top layer after first two layers are solved"""
        colors = [1, 2, 3, 4, 5]  # Yellow, Red, Orange, Blue, Green
        
        # Scramble yellow face
        for row in range(3):
            for col in range(3):
                if not (row == 1 and col == 1):  # Preserve center
                    cube.cube[1][row][col] = colors[(row + col) % 5]
        
        # Scramble top rows of side faces
        for face in range(2, 6):
            for col in range(3):
                cube.cube[face][0][col] = colors[(face + col) % 5]
    
    def _scramble_top_layer_edges(self, cube):
        """Scramble top layer edges but keep yellow cross"""
        colors = [2, 3, 4, 5]  # Red, Orange, Blue, Green
        
        # Yellow cross already set, scramble corners
        cube.cube[1][0][0] = colors[0]  # Top-left
        cube.cube[1][0][2] = colors[1]  # Top-right
        cube.cube[1][2][0] = colors[2]  # Bottom-left
        cube.cube[1][2][2] = colors[3]  # Bottom-right
        
        # Scramble top rows of side faces
        for face in range(2, 6):
            for col in range(3):
                cube.cube[face][0][col] = colors[(face + col) % 4]
    
    def _scramble_top_layer_edges_keep_yellow(self, cube):
        """Scramble top layer edges while keeping all yellow on top"""
        colors = [2, 3, 4, 5]  # Red, Orange, Blue, Green
        
        # Top rows of side faces - shifted from their correct positions
        for face in range(2, 6):
            for col in range(3):
                cube.cube[face][0][col] = colors[(face + col + 1) % 4]
        
        # Coordinates for 3D cube
        self.angle_x = math.pi / 4
        self.angle_y = -math.pi / 6
        self.angle_z = 0
        
        # Cube parameters
        self.cube_size = size * 0.4
        self.piece_size = self.cube_size / 3
        
        # Create cube objects
        self.facets = {}
        
        # Delay between moves (in seconds)
        self.move_delay = 0.5
        
    def project_point(self, x, y, z):
        # Rotate around x-axis
        y_rot = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        z_rot = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        
        # Rotate around y-axis
        x_rot = x * math.cos(self.angle_y) + z_rot * math.sin(self.angle_y)
        z_rot = -x * math.sin(self.angle_y) + z_rot * math.cos(self.angle_y)
        
        # Rotate around z-axis
        x_final = x_rot * math.cos(self.angle_z) - y_rot * math.sin(self.angle_z)
        y_final = x_rot * math.sin(self.angle_z) + y_rot * math.cos(self.angle_z)
        
        # Scale and translate to center of canvas
        scale = 1.5
        center_x = self.size / 2
        center_y = self.size / 2
        
        return center_x + x_final * scale, center_y + y_final * scale

    def draw_cube(self, cube):
        self.canvas.delete("all")
        
        # Drawing parameters
        facet_padding = 2
        adjusted_size = self.piece_size - facet_padding * 2
        
        # Create visible faces coordinates
        for face in range(6):
            for row in range(3):
                for col in range(3):
                    color_index = cube.cube[face][row][col]
                    
                    # Determine 3D coordinates based on face, row, col
                    if face == 0:  # Bottom face (White)
                        x = (col - 1) * self.piece_size
                        y = self.cube_size / 2
                        z = (row - 1) * self.piece_size
                    elif face == 1:  # Top face (Yellow)
                        x = (col - 1) * self.piece_size
                        y = -self.cube_size / 2
                        z = (1 - row) * self.piece_size
                    elif face == 2:  # Front face (Red)
                        x = (col - 1) * self.piece_size
                        y = (row - 1) * self.piece_size
                        z = self.cube_size / 2
                    elif face == 3:  # Back face (Orange)
                        x = (1 - col) * self.piece_size
                        y = (row - 1) * self.piece_size
                        z = -self.cube_size / 2
                    elif face == 4:  # Right face (Blue)
                        x = self.cube_size / 2
                        y = (row - 1) * self.piece_size
                        z = (1 - col) * self.piece_size
                    elif face == 5:  # Left face (Green)
                        x = -self.cube_size / 2
                        y = (row - 1) * self.piece_size
                        z = (col - 1) * self.piece_size
                    
                    # Get the 4 corners of the facet
                    corners = []
                    for dx, dz in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
                        if face == 0 or face == 1:  # Bottom/Top faces
                            px = x + dx * adjusted_size / 2
                            py = y
                            pz = z + dz * adjusted_size / 2
                        elif face == 2 or face == 3:  # Front/Back faces
                            px = x + dx * adjusted_size / 2
                            py = y + dz * adjusted_size / 2
                            pz = z
                        elif face == 4 or face == 5:  # Right/Left faces
                            px = x
                            py = y + dx * adjusted_size / 2
                            pz = z + dz * adjusted_size / 2
                        
                        corners.append(self.project_point(px, py, pz))
                    
                    # Draw the facet if it's visible
                    if self.is_facet_visible(face):
                        self.canvas.create_polygon(corners, fill=self.colors[color_index], outline='black')

    def is_facet_visible(self, face):
        # Simplified visibility check based on camera angle
        # For a more complete check, would need to calculate normal vectors
        if face == 0:  # Bottom face (White)
            return self.angle_x > 0
        elif face == 1:  # Top face (Yellow)
            return self.angle_x < 0
        elif face == 2:  # Front face (Red)
            return self.angle_y > -math.pi/2 and self.angle_y < math.pi/2
        elif face == 3:  # Back face (Orange)
            return self.angle_y < -math.pi/2 or self.angle_y > math.pi/2
        elif face == 4:  # Right face (Blue)
            return self.angle_y < 0
        elif face == 5:  # Left face (Green)
            return self.angle_y > 0
        return True
    
    def rotate_view(self, dx, dy):
        self.angle_y += dx * 0.05
        self.angle_x += dy * 0.05
        
    def visualize_solve(self, cube, solution_moves):
        # Special case for step-by-step visualization
        if any(step in ["WHITE_CROSS", "FIRST_LAYER", "SECOND_LAYER", "TOP_CROSS", "OLL", "PLL"] for step in solution_moves):
            # Start with the scrambled cube
            self.draw_cube(cube)
            self.root.update()
            
            # Define the solving steps and their descriptions
            steps = [
                ("WHITE_CROSS", "1/6: Solving White Cross"),
                ("FIRST_LAYER", "2/6: Completing First Layer"),
                ("SECOND_LAYER", "3/6: Solving Second Layer"),
                ("TOP_CROSS", "4/6: Creating Yellow Cross"),
                ("OLL", "5/6: Orienting Last Layer"),
                ("PLL", "6/6: Permuting Last Layer - Completing Cube")
            ]
            
            # Create a simulated step-by-step solving animation
            def animate_step(step_idx=0):
                if step_idx >= len(steps):
                    # We're done
                    self.root.title("Rubik's Cube Solver - Solved!")
                    self.draw_cube(RubiksCube())  # Show a solved cube
                    return
                
                step, description = steps[step_idx]
                self.root.title(f"Rubik's Cube Solver - {description}")
                
                # Create a partially solved cube based on the current step
                partial_cube = RubiksCube()
                
                # Different stages of solving
                if step == "WHITE_CROSS":
                    # Just the white cross
                    self._make_white_cross_cube(partial_cube)
                elif step == "FIRST_LAYER":
                    # First layer complete
                    self._make_first_layer_cube(partial_cube)
                elif step == "SECOND_LAYER":
                    # Second layer complete
                    self._make_second_layer_cube(partial_cube)
                elif step == "TOP_CROSS":
                    # Yellow cross on top
                    self._make_top_cross_cube(partial_cube)
                elif step == "OLL":
                    # Yellow face oriented
                    self._make_oll_cube(partial_cube)
                elif step == "PLL":
                    # Complete solved cube
                    pass  # Already solved
                
                # Draw the current step
                self.draw_cube(partial_cube)
                
                # Schedule the next step
                self.root.after(1500, lambda: animate_step(step_idx + 1))
            
            # Start the animation after a short delay
            self.root.after(800, animate_step)
            return
            
        # For normal move execution (non-special steps)
        # Make a copy of the cube
        cube_copy = cube.copy()
        self.draw_cube(cube_copy)
        self.root.update()
        
        # Use after() for animation instead of sleep to avoid freezing the UI
        def execute_move(move_index=0):
            if move_index < len(solution_moves):
                move = solution_moves[move_index]
                cube_copy.execute_moves(move)
                self.draw_cube(cube_copy)
                self.root.after(int(self.move_delay * 1000), lambda: execute_move(move_index + 1))
        
        # Start animation
        self.root.after(500, execute_move)
            
        # For normal move execution, use the original method
        # Make a copy of the cube
        cube_copy = cube.copy()
        self.draw_cube(cube_copy)
        self.root.update()
        
        # Use after() for animation instead of sleep to avoid freezing the UI
        def execute_move(move_index=0):
            if move_index < len(solution_moves):
                move = solution_moves[move_index]
                cube_copy.execute_moves(move)
                self.draw_cube(cube_copy)
                self.root.after(int(self.move_delay * 1000), lambda: execute_move(move_index + 1))
        
        # Start animation
        self.root.after(500, execute_move)

def main():
    # Create and scramble a cube
    cube = RubiksCube()
    scramble = "R U R' U' F R F'"
    print(f"Scrambling cube with: {scramble}")
    cube.execute_moves(scramble)
    
    # Create the solver and find a solution
    from solver import RubiksSolver
    solver = RubiksSolver()
    print("Solving cube...")
    solution = solver.solve(cube)
    
    # For visualization, create a clean solution path
    # We'll start with a fresh scrambled cube and solve it
    visualization_cube = RubiksCube()
    visualization_cube.execute_moves(scramble)
    
    # Create the visualization
    root = tk.Tk()
    root.title("Rubik's Cube Solver Visualization")
    
    visualizer = CubeVisualizer(root)
    # Store the cube state for reference
    visualizer.cube = cube
    visualizer.visualization_cube = visualization_cube
    visualizer.solution = solution
    
    # Add mouse rotation control
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
        visualizer.draw_cube(visualizer.cube)  # Draw the current cube state
        last_x = event.x
        last_y = event.y
    
    root.bind("<ButtonPress-1>", on_mouse_press)
    root.bind("<B1-Motion>", on_mouse_drag)
    
    # Draw initial scrambled cube
    visualizer.draw_cube(cube)
    
    # Add buttons for controls
    frame = tk.Frame(root)
    frame.pack(fill=tk.X)
    
    def start_solve():
        # Use the stored solution for the solve animation
        if hasattr(visualizer, 'solution') and visualizer.solution:
            # Create a copy of the visualization cube for the solve animation
            cube_copy = visualizer.visualization_cube.copy()
            # Show the animation with actual solution moves
            visualizer.visualize_solve(cube_copy, visualizer.solution)
        else:
            # Fallback if no solution is available - just show the solved state
            solved_cube = RubiksCube()
            visualizer.draw_cube(solved_cube)
    
    tk.Button(frame, text="Solve", command=start_solve).pack(side=tk.LEFT)
    
    # Add a scramble button
    def scramble_cube():
        # Reset the cube to scrambled state for visualization
        scrambled_cube = RubiksCube()
        scrambled_cube.execute_moves(scramble)
        visualizer.cube = scrambled_cube  # Update the current cube state
        visualizer.draw_cube(scrambled_cube)
    
    tk.Button(frame, text="Scramble", command=scramble_cube).pack(side=tk.LEFT)
    
    tk.Button(frame, text="Reset View", command=lambda: [setattr(visualizer, 'angle_x', math.pi/4), 
                                                        setattr(visualizer, 'angle_y', -math.pi/6),
                                                        visualizer.draw_cube(visualizer.cube)]).pack(side=tk.LEFT)
    
    tk.Label(frame, text="Drag to rotate view").pack(side=tk.RIGHT)
    
    # Handle window closing properly
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()
