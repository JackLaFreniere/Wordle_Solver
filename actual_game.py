import word_helper
from wordle_game import Wordle, max_word_size
import numpy as np
from compute_data import get_byg_to_int

class Actual_Wordle(Wordle):
    def __init__(self, pattern_table:np.ndarray):
        super().__init__(-1, pattern_table)
    
    def guess(self, guess:str) -> str:
        self.attempts += 1

        print(f"My guess is: {word_helper.get_index_to_guess(guess)}")
        byg = input("Enter the byg combination >> ")
        
        if byg == "ggggg":
            self.attempts = self.max_attempts
        
        if not byg:
            self.max_attempts += 1
            return ""
        
        return get_byg_to_int(byg)