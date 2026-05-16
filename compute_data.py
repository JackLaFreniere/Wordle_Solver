import word_helper, game
from itertools import product
import numpy as np

def get_pattern_table() -> np.ndarray:
    try:
        return np.load("computed_data/numpy_data.npy", mmap_mode="r")
    except:
        return create_pattern_table()
                
def create_pattern_table() -> np.ndarray:
    pattern_table = calculate_pattern_table()
    np.save("computed_data/numpy_data.npy", pattern_table)
    
    return pattern_table

def get_byd_int() -> dict:
    breakdown = {}
    combs = list(product("byg", repeat=5))
    for i in range(len(combs)):
        breakdown["".join(combs[i])] = i

    return breakdown

def calculate_pattern_table() -> np.ndarray:
    pattern_table = np.zeros((len(word_helper.get_possible_answers()), len(word_helper.get_accepted_guesses())), dtype=np.uint8)    
    breakdown = get_byd_int()

    answers = word_helper.get_possible_answers()
    guesses = word_helper.get_accepted_guesses()
    for a in range(len(answers)):
        for g in range(len(guesses)):
            byg = game.Wordle.get_byg(answers[a], guesses[g])
            pattern_table[a][g] = breakdown[byg]
            
    return pattern_table

if __name__ == "__main__":
    create_pattern_table()
