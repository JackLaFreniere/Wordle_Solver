import numpy as np

max_word_size = 5
max_attempts = 6

class Wordle:    
    def __init__(self, word:int, pattern_table:np.ndarray):
        self.max_attempts = max_attempts
        self.pattern_table = pattern_table
        self.reset(word)
    
    def reset(self, word:int):
        self.answer = word
        self.attempts = 0

    def is_game_over(self) -> bool:
        return self.attempts >= self.max_attempts
    
    def get_number_of_words_attempted(self) -> int:
        return self.attempts

    def guess(self, word:int) -> int:
        self.attempts += 1

        if word == self.answer: #Player got it right
            self.attempts = self.max_attempts
            return 3 ** max_word_size - 1
        
        return self.pattern_table[self.answer, word]
