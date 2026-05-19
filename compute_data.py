import word_helper, wordle_game, sys, wordle_solver_bot, copy
from itertools import product
import numpy as np

DATA_DIRECTORY = "data/computed_data/"

GUESS_BYG_TABLE_NAME = "pattern_table.npy"
GUESS_PRECOMPUTED_TABLE_NAME = "best_guesses.npy"
BEST_GUESS_NAME = "best_guess.txt"

byg_to_int_dict = {}
int_to_byd_dict = {}

total_byg_combinations = 3 ** wordle_game.max_word_size

def create_byg_and_int_dict():
    global byg_to_int_dict, int_to_byd_dict

    if byg_to_int_dict and int_to_byd_dict:
        pass

    byg_combinations = list(product("byg", repeat=wordle_game.max_word_size))
    for i in range(len(byg_combinations)):
        byg_to_int_dict["".join(byg_combinations[i])] = i
        int_to_byd_dict[i] = "".join(byg_combinations[i])

def get_byg_to_int(byg:str) -> int:
    global byg_to_int_dict

    return byg_to_int_dict[byg]

def get_int_to_byg(num:int) -> str:
    global int_to_byd_dict

    return int_to_byd_dict[num]

def get_pattern_table() -> np.ndarray:
    return get_np_array(GUESS_BYG_TABLE_NAME, create_pattern_table)
    
def get_best_guesses() -> tuple[str, np.ndarray]:
    try:
        best_guess = ""
        with open(f"{DATA_DIRECTORY}{BEST_GUESS_NAME}", "r") as file:
            best_guess = file.readline()    
              
        return (best_guess, np.load(f"data/computed_data/{GUESS_PRECOMPUTED_TABLE_NAME}", mmap_mode="r"))
    except:
        return create_best_guesses()

def get_np_array(name:str, get_func:function) -> np.ndarray:
    try:
        return np.load(f"data/computed_data/{name}", mmap_mode="r")
    except:
        create_byg_and_int_dict()
        return get_func()
                
def create_pattern_table() -> np.ndarray:
    pattern_table = calculate_pattern_table()
    np.save(f"{DATA_DIRECTORY}{GUESS_BYG_TABLE_NAME}", pattern_table)
    
    return pattern_table

def calculate_pattern_table() -> np.ndarray:
    global byg_to_int_dict
    
    answers = word_helper.get_possible_answers()
    guesses = word_helper.get_accepted_guesses()

    pattern_table = np.zeros((len(answers), len(guesses)), dtype=np.uint8)    

    print("Creating Pattern Table")
    len_a = len(answers)
    len_g = len(guesses)
    for a in range(len(answers)):
        print(f"Pattern Table: {a:,} out of {len_a:,} ({a/len_a:.2%})")
        for g in range(len(guesses)):

            byg = wordle_game.Wordle.get_byg(answers[a], guesses[g])
            pattern_table[a][g] = byg_to_int_dict[byg]
    
    print("Done!\n")

    return pattern_table

def create_best_guesses() -> tuple[str, np.ndarray]:
    best_first_guess, best_guesses_table = calculate_best_guesses()
    np.save(f"{DATA_DIRECTORY}{GUESS_PRECOMPUTED_TABLE_NAME}", best_guesses_table)

    with open(f"{DATA_DIRECTORY}{BEST_GUESS_NAME}", "w") as file:
        file.write(best_first_guess)
        
    return (best_first_guess, best_guesses_table)

def calculate_best_guesses() -> tuple[str, np.ndarray]:
    best_guesses_table = np.zeros((total_byg_combinations), dtype=f"U{wordle_game.max_word_size}")    
    jarvis = wordle_solver_bot.Jarvis(get_pattern_table(), None) 
    
    answers = word_helper.get_possible_answers()

    print("Getting the best first word")
    best_first_guess = jarvis.get_word(answers)
    print("Done!\n")

    num_second_guesses = total_byg_combinations
    for i in range(num_second_guesses):
        print(f"Best guess: {i} out of {num_second_guesses} ({i/num_second_guesses:.2%})")

        remaining_words = jarvis.shorten_words(copy.deepcopy(answers), best_first_guess, int_to_byd_dict[i])
        best_second_word = jarvis.get_word(remaining_words)
        
        best_guesses_table[i] = best_second_word

    return (best_first_guess, best_guesses_table)

if __name__ == "__main__":
    create_byg_and_int_dict()
    if len(sys.argv) > 1:
        if any(flag in sys.argv for flag in ("--pt", "--all")):
            create_pattern_table()
        if any(flag in sys.argv for flag in ("--bg", "--all")):
            print(create_best_guesses())
