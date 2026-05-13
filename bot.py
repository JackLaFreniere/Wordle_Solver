import game, word_helper, copy
from itertools import combinations_with_replacement

class Jarvis:
    def __init__(self):
        pass
    
    def play_game(self, word:str) -> tuple[list, bool]:
        wordle = game.Wordle(word)
        attempts = []
        results = []

        word_list = word_helper.get_words()
        remaining_words = copy.deepcopy(word_list)

        while not wordle.is_game_over():
            guess = self.get_word(word_list, remaining_words)

            response = wordle.guess(guess)
            attempts.append(guess)
            results.append(response)

        return (attempts, results, results[-1] == "ggggg")
    
    def get_word(self, word_list:list, remaining_words:list) -> str:
        return "hello"
        # sample_vals = ["b", "y", "g"]
        # combs = list(combinations_with_replacement(sample_vals, 5))
        # for word in word_list:
        #     total = 0
        #     test_list = copy.deepcopy(remaining_words)
        #     for comb in combs:
        #         if
