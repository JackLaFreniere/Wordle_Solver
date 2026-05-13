class Wordle:
    def __init__(self, word):
        self.answer = word
        self.attempts = 0
        self.max_attempts = 6
        self.max_word_size = 5
    
    def is_game_over(self) -> bool:
        return self.attempts >= self.max_attempts

    def get_letter_distribution(self, word:str) -> dict:
        dist = {}

        for w in word:
            if w in dist:
                dist[w] = dist[w] + 1
                continue

            dist[w] = 1
        
        return dist

    def guess(self, word:str) -> str:
        self.attempts += 1

        if word == self.answer: #Player got it right
            self.attempts = self.max_attempts
            return "g" * self.max_word_size
        
        dist = self.get_letter_distribution(self.answer)
        response = "b" * self.max_word_size
        
        for i in range(self.max_word_size):
            letter = word[i]
            if letter == self.answer[i]: #Green
                response = response[:i] + "g" + response[i + 1:]
                dist[letter] = dist[letter] - 1
        
        for i in range(self.max_word_size):
            if response[i] == "g":
                continue

            letter = word[i]
            if letter in dist and dist[letter]: #Yellow
                dist[letter] = dist[letter] - 1
                response = response[:i] + "y" + response[i + 1:]
        
        return response
