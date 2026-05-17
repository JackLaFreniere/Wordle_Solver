import game, word_helper, copy, sys, compute_data
import numpy as np
from typing import Union

class Jarvis:
    def __init__(self, pattern_table:Union[np.ndarray, None], best_guesses:Union[tuple[str, np.ndarray], None]):
        self.wordle = None
        self.possible_answers = word_helper.get_possible_answers()
        self.accepted_guesses = word_helper.get_accepted_guesses()
        
        self.possible_answers_dict = dict(zip(self.possible_answers, range(len(self.possible_answers))))
        self.accepted_guesses_dict = dict(zip(self.accepted_guesses, range(len(self.accepted_guesses))))

        if isinstance(pattern_table, np.ndarray):
            self.pattern_table = pattern_table
        if isinstance(best_guesses, tuple):
            self.best_guess, self.best_guesses_table = best_guesses[0], best_guesses[1]

    def play_game(self, word:str) -> tuple[list, bool]:
        self.__init__(None, None)
        self.wordle = game.Wordle(word)
        
        attempts = []
        results = []

        remaining_words = copy.deepcopy(self.possible_answers)
        previous_response = ""

        while not self.wordle.is_game_over():
            if self.wordle.get_number_of_words_attempted() == 0:
                guess = self.best_guess
            elif self.wordle.get_number_of_words_attempted() == 1:
                guess = str(self.best_guesses_table[compute_data.get_byg_to_int(previous_response)])
            else:
                guess = self.get_word(remaining_words)
            
            response = self.wordle.guess(guess)
            previous_response = response
            remaining_words = self.shorten_words(remaining_words, guess, response)

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
