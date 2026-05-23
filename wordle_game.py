max_word_size = 5
max_attempts = 6

class Wordle:    
    def __init__(self, word):
        self.answer = word
        self.attempts = 0
        self.max_attempts = max_attempts

    def is_game_over(self) -> bool:
        return self.attempts >= self.max_attempts
    
    def get_number_of_words_attempted(self) -> int:
        return self.attempts

    def guess(self, word:str) -> str:
        self.attempts += 1

        if word == self.answer: #Player got it right
            self.attempts = self.max_attempts
            return "g" * max_word_size
        
        return self.get_byg(self.answer, word)
