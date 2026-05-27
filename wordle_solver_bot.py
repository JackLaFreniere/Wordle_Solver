import wordle_game, actual_game, word_helper, copy
import numpy as np
from compute_data import initialize_data, get_pattern_table, get_best_guesses, get_word, shorten_words, get_int_to_byg, get_answer_index_to_guess_index_table

class Jarvis:
    def __init__(self):
        initialize_data()
        
        self.possible_answers_indexes = np.array(word_helper.get_possible_answers_indexes())
        self.accepted_guesses_indexes = np.array(word_helper.get_accepted_guesses_indexes())

        self.pattern_table = get_pattern_table()
        self.best_guess, self.best_guesses_table = get_best_guesses()
        self.answer_index_to_guess_index_table = get_answer_index_to_guess_index_table()
        
        self.wordle = wordle_game.Wordle(-1, self.pattern_table)
    
    def reset(self, word:str):
        self.wordle.reset(word)

    def play_game(self, word:str, is_actual_game:bool = False) -> tuple[list, bool]:
        self.reset(word)

        if is_actual_game:
            self.wordle = actual_game.Actual_Wordle(self.pattern_table)
        else:
            self.wordle = wordle_game.Wordle(word, self.pattern_table)
        
        attempts = []
        results = []

        remaining_answers_indexes = copy.deepcopy(self.possible_answers_indexes)
        remaining_guesses_indexes = copy.deepcopy(self.accepted_guesses_indexes)
        previous_response = -1

        while not self.wordle.is_game_over() and (len(results) == 0 or results[-1] != "ggggg"):
            if self.wordle.get_number_of_words_attempted() == 0: #Precomputed first guess
                guess = self.best_guess
            elif len(remaining_answers_indexes) <= 2: #Force a valid guess there is one or two words left
                guess = self.answer_index_to_guess_index_table[remaining_answers_indexes[0]]
            elif self.wordle.get_number_of_words_attempted() == 1: #Precomputed second guess
                guess = self.best_guesses_table[previous_response]
            else: #Compute the current best guess
                guess = get_word(remaining_guesses_indexes, remaining_answers_indexes)
            
            response = self.wordle.guess(guess)

            if response == "":
                remaining_guesses_indexes = remaining_guesses_indexes[remaining_guesses_indexes != guess]
                if guess in remaining_answers_indexes:
                    remaining_answers_indexes = remaining_answers_indexes[remaining_answers_indexes != guess]
                continue
            
            previous_response = response
            remaining_guesses_indexes, remaining_answers_indexes = shorten_words(remaining_guesses_indexes, remaining_answers_indexes, guess, response)

            attempts.append(word_helper.get_index_to_guess(guess))
            results.append(get_int_to_byg(response))

        if word == "":
            return

        return (attempts, results, word_helper.get_index_to_answer(word), results[-1] == "ggggg")
