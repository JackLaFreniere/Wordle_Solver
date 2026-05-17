import game, actual_game, word_helper, copy, compute_data
import numpy as np
from typing import Union

class Jarvis:
    def __init__(self, pattern_table:Union[np.ndarray, None], best_guesses:Union[tuple[str, np.ndarray], None]):
        self.wordle = None
        self.possible_answers = word_helper.get_possible_answers()
        self.accepted_guesses = word_helper.get_accepted_guesses()
        
        self.possible_answers_dict = dict(zip(self.possible_answers, range(len(self.possible_answers))))
        self.accepted_guesses_dict = dict(zip(self.accepted_guesses, range(len(self.accepted_guesses))))

        compute_data.main()

        if isinstance(pattern_table, np.ndarray):
            self.pattern_table = pattern_table
        if isinstance(best_guesses, tuple):
            self.best_guess, self.best_guesses_table = best_guesses[0], best_guesses[1]

    def play_game(self, word:str, is_actual_game:bool = False) -> tuple[list, bool]:
        self.__init__(None, None)
        if is_actual_game:
            self.wordle = actual_game.Actual_Wordle("")
        else:
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
            elif len(remaining_words) <= 2:
                guess = remaining_words[0]
            else:
                guess = self.get_word(remaining_words)
            
            response = self.wordle.guess(guess)
            if not response:
                self.accepted_guesses.remove(guess)
                if guess in self.possible_answers:
                    self.possible_answers.remove(guess)
                continue
            
            previous_response = response
            self.shorten_words(remaining_words, guess, response)

            attempts.append(guess)
            results.append(response)

        return (attempts, results, word, results[-1] == "ggggg")
    
    def get_word(self, remaining_words:list) -> str:
        best_guess = self.accepted_guesses[0]
        best_guess_score = float("inf")

        for i in range(len(self.accepted_guesses)):
            buckets = {}
            for j in range(len(remaining_words)):
                p = self.pattern_table[self.possible_answers_dict[remaining_words[j]]][i]
                buckets[p] = buckets.get(p, 0) + 1
                
            score = self.get_score(buckets)
            if score < best_guess_score:
                best_guess = self.accepted_guesses[i]
                best_guess_score = score
        
        return best_guess
    
    def get_score(self, buckets:dict) -> float:
        weighted_total = sum(x ** 2 for x in list(buckets.values()))
        total = sum(list(buckets.values()))

        if total != 0:
            return weighted_total / total
        else:
            return 0

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
