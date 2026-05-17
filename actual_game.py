from game import Wordle

class Actual_Wordle(Wordle):
    def __init__(self, word = ""):
        super().__init__(word)
    
    def guess(self, guess:str) -> str:
        self.attempts += 1
        print(f"My guess is: {guess}")
        byg = input("Enter the byg combination >> ")
        if byg == "ggggg":
            self.attempts = self.max_attempts
        
        if not byg:
            self.max_attempts += 1
            return ""
        
        return byg