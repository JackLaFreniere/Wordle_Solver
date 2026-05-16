import game, word_helper, copy, compute_data, sys
import numpy as np

class Jarvis:
    def __init__(self):
        self.wordle = None

    def play_game(self, word:str) -> tuple[list, bool]:
        self.wordle = game.Wordle(word)
        self.possible_answers = word_helper.get_possible_answers()
        self.accepted_guesses = word_helper.get_accepted_guesses()
        self.possible_answers_dict = dict(zip(self.possible_answers, range(len(self.possible_answers))))
        self.accepted_guesses_dict = dict(zip(self.accepted_guesses, range(len(self.accepted_guesses))))
        self.pattern_table = compute_data.get_pattern_table()
        attempts = []
        results = []

        remaining_words = copy.deepcopy(self.possible_answers)

        while not self.wordle.is_game_over():
            guess = self.get_word(remaining_words)
            response = self.wordle.guess(guess)
            remaining_words = self.shorten_words(remaining_words, guess, response)
            # print(f"{guess}: {response}")

            attempts.append(guess)
            results.append(response)

        return (attempts, results, word, results[-1] == "ggggg")
    
    def get_word(self, remaining_words:list) -> str:
        best_guess = self.accepted_guesses[0]
        best_guess_score = sys.maxsize

        for i in range(len(self.accepted_guesses)):
            buckets = np.zeros(243, dtype=int)
            for j in range(len(remaining_words)):
                p = self.pattern_table[self.possible_answers_dict[remaining_words[j]]][i]
                buckets[p] += 1
                
            score = self.get_score(buckets)
            if score < best_guess_score:
                best_guess = self.accepted_guesses[i]
                best_guess_score = score
        
        return best_guess
    
    def get_score(self, buckets:np.ndarray) -> float:
        return np.sum(buckets * buckets) / np.sum(buckets)

    def shorten_words(self, remaining_words:list, guess:str, response:str):
        if guess in remaining_words:
            remaining_words.remove(guess)
        
        if guess in self.accepted_guesses:
            self.accepted_guesses.remove(guess)

        to_remove = []
        for i in range(len(remaining_words)):
            r = remaining_words[i]
            byg = game.Wordle.get_byg(remaining_words[i], guess)
            if  byg != response:
                to_remove.append(i)
        
        for i in range(len(to_remove) - 1, -1, -1):
            remaining_words.pop(to_remove[i])

        return remaining_words
