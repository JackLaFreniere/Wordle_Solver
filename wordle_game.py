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

    @classmethod
    def get_letter_distribution(self, word:str) -> dict:
        dist = {}

        for w in word:
            if w in dist:
                dist[w] = dist[w] + 1
                continue

            dist[w] = 1
        
        return dist

    @classmethod
    def get_byg(self, answer:str, guess:str) -> str:
        dist = self.get_letter_distribution(answer)
        response = "b" * max_word_size
        
        for i in range(max_word_size):
            letter = guess[i]
            if letter == answer[i]: #Green
                response = response[:i] + "g" + response[i + 1:]
                dist[letter] = dist[letter] - 1
        
        for i in range(max_word_size):
            if response[i] == "g":
                continue

            letter = guess[i]
            if letter in dist and dist[letter]: #Yellow
                dist[letter] = dist[letter] - 1
                response = response[:i] + "y" + response[i + 1:]
        
        return response
