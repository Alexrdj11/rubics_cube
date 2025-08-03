"""
Tracks the solving process of a Rubik's Cube with detailed step information
"""

import time
from typing import List, Dict, Any

class SolveTracker:
    def __init__(self):
        """Initialize a new solve tracking session"""
        self.start_time = None
        self.end_time = None
        self.total_moves = 0
        self.steps = []
        self.scramble = ""
        self.is_complete = False
    
    def start_solve(self, scramble=""):
        """Start tracking a new solve with the given scramble"""
        self.start_time = time.time()
        self.scramble = scramble
        self.steps = []
        self.total_moves = 0
        self.is_complete = False
        return self
    
    def add_step(self, name: str, moves: int, description: str = ""):
        """Add a solving step with the number of moves used"""
        self.steps.append({
            "name": name,
            "moves": moves,
            "description": description,
            "total_moves_so_far": self.total_moves + moves
        })
        self.total_moves += moves
        return self
    
    def finish_solve(self, success: bool = True):
        """Mark the solve as complete and record the end time"""
        self.end_time = time.time()
        self.is_complete = success
        return self
    
    def get_elapsed_time(self) -> float:
        """Get the elapsed time of the solve in seconds"""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the solve"""
        return {
            "scramble": self.scramble,
            "total_moves": self.total_moves,
            "elapsed_time": self.get_elapsed_time(),
            "is_complete": self.is_complete,
            "steps": self.steps
        }
    
    def print_solve_progress(self) -> None:
        """Print the solve progress in a formatted way"""
        print(f"> Initializing cube state...")
        print(f"> Analyzing scramble: [{self.scramble}]")
        
        for step in self.steps:
            print(f"> {step['name']}: {step['description']} ({step['total_moves_so_far']} moves)")
        
        if self.is_complete:
            print(f"> Cube solved successfully!")
            print(f"> Total time: {self.get_elapsed_time():.2f} seconds")
            print(f"> Moves applied: {self.total_moves}")
        else:
            print(f"> Solve incomplete after {self.total_moves} moves")
            print(f"> Elapsed time: {self.get_elapsed_time():.2f} seconds")
