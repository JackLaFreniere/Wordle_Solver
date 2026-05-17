import word_helper, game, sys, bot, copy
from itertools import product
import numpy as np

GUESS_BYG_TABLE_NAME = "pattern_table.npy"
GUESS_PRECOMPUTED_TABLE_NAME = "best_guesses.npy"
BEST_GUESS_NAME = "best_guess.txt"

byg_to_int_dict = {}
int_to_byd_dict = {}

def main():
    global byg_to_int_dict, int_to_byd_dict

    byg_combinations = list(product("byg", repeat=5))
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
    best_guess = ""
    with open(f"computed_data/{BEST_GUESS_NAME}", "r") as file:
        best_guess = file.readline()

    return (best_guess, get_np_array(GUESS_PRECOMPUTED_TABLE_NAME, create_best_guesses))

def get_np_array(name:str, get_func:function) -> np.ndarray:
    try:
        return np.load(f"computed_data/{name}", mmap_mode="r")
    except:
        return get_func()
                
def create_pattern_table() -> np.ndarray:
    pattern_table = calculate_pattern_table()
    np.save(f"computed_data/{GUESS_BYG_TABLE_NAME}", pattern_table)
    
    return pattern_table

def calculate_pattern_table() -> np.ndarray:
    global byg_to_int_dict
    
    answers = word_helper.get_possible_answers()
    guesses = word_helper.get_accepted_guesses()

    pattern_table = np.zeros((len(answers), len(guesses)), dtype=np.uint8)    

    len_a = len(answers)
    len_g = len(guesses)
    for a in range(len(answers)):
        print(f"Pattern Table: {a:,} out of {len_a:,} ({a/len_a:.2%})")
        for g in range(len(guesses)):

            byg = game.Wordle.get_byg(answers[a], guesses[g])
            pattern_table[a][g] = byg_to_int_dict[byg]
    
    print("Done!\n")

    return pattern_table

def create_best_guesses() -> tuple[str, np.ndarray]:
    best_first_guess, best_guesses_table = calculate_best_guesses()
    np.save(f"computed_data/{GUESS_PRECOMPUTED_TABLE_NAME}", best_guesses_table)

    return (best_first_guess, best_guesses_table)

def calculate_best_guesses() -> tuple[str, np.ndarray]:
    best_guesses_table = np.zeros((3**5), dtype="U5")    
    jarvis = bot.Jarvis(get_pattern_table(), None) 
    
    answers = word_helper.get_possible_answers()

    print("Getting the best first word")
    best_first_guess = 'roate'#jarvis.get_word(answers)
    print("Done!\n")

    with open(f"computed_data/{BEST_GUESS_NAME}", "w") as file:
        file.write(best_first_guess)

    num_second_guesses = 3**5
    for i in range(num_second_guesses):
        print(f"Best guess: {i} out of {num_second_guesses} ({i/num_second_guesses:.2%})")

        remaining_words = jarvis.shorten_words(copy.deepcopy(answers), best_first_guess, int_to_byd_dict[i])
        best_second_word = jarvis.get_word(remaining_words)
        
        best_guesses_table[i] = best_second_word
        # print(i, best_second_word, len(answers), len(remaining_words))

    return (best_first_guess, best_guesses_table)

if __name__ == "__main__":
    main()
    if len(sys.argv) > 1:
        if any(flag in sys.argv for flag in ("--pt", "--all")):
            create_pattern_table()
        if any(flag in sys.argv for flag in ("--bg", "--all")):
            print(create_best_guesses())
