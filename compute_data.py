import word_helper, sys, copy
from itertools import product
from collections import Counter
from wordle_game import max_word_size
import numpy as np

DATA_DIRECTORY = "data/computed_data/"

GUESS_BYG_TABLE_NAME = "pattern_table.npy"
GUESS_PRECOMPUTED_TABLE_NAME = "best_guesses.npy"
BEST_GUESS_NAME = "best_guess.txt"

GUESS_BYG_TABLE_DIRECTORY_NAME = DATA_DIRECTORY + GUESS_BYG_TABLE_NAME
GUESS_PRECOMPUTED_TABLE_DIRECTORY_NAME = DATA_DIRECTORY + GUESS_PRECOMPUTED_TABLE_NAME
GUESS_PRECOMPUTED_GUESS_DIRECTORY_NAME = DATA_DIRECTORY + BEST_GUESS_NAME

byg_to_int_dict, int_to_byd_dict = {}, {}

total_byg_combinations = 3 ** max_word_size

pattern_table = None
best_guess = None
best_guesses = None

def initialize_data():
    global byg_to_int_dict, int_to_byd_dict

    byg_to_int_dict, int_to_byd_dict = get_byg_and_int_dict()

def get_byg_and_int_dict() -> tuple[dict[str, int], dict[int, str]]:
    byg_to_int, int_to_byg = {}, {}

    byg_combinations = list(product("byg", repeat=max_word_size))
    for i in range(len(byg_combinations)):
        byg_to_int["".join(byg_combinations[i])] = i
        int_to_byg[i] = "".join(byg_combinations[i])
    
    return byg_to_int, int_to_byg

def get_byg_to_int(byg:str) -> int:
    global byg_to_int_dict

    return byg_to_int_dict[byg]

def get_int_to_byg(num:int) -> str:
    global int_to_byd_dict

    return int_to_byd_dict[num]

def get_pattern_table() -> np.ndarray:
    """ 
    Gets the Pattern Table from a precomputed .npy file.
    If the .npy does not exist or there is an error in accesing it, the table is recomputed.\n
    Usage of pattern table goes like this:\n
        pattern_table[answer_index, guess_index] = byg_index
    """

    try:
        return np.load(GUESS_BYG_TABLE_DIRECTORY_NAME, mmap_mode="r")
    except:
        return create_pattern_table()
    
def get_best_guesses() -> tuple[str, np.ndarray]:
    """ 
    The best **first** guess is obtained from a .txt file.
    If the .txt does not exist or there is an error in acacessing it, the file is recomputed.\n
    Gets the best **second** guesses from a precomputed .npy file.
    If the .npy does not exist or there is an error in accesing it, the table is recomputed.\n
    Usage of best guesses goes like this:\n
        (best_guess, best_guesses)
        best_guess = guess_index
        best_guesses[fbyg_index] = guess_index
    """

    try:
        best_guess = ""
        with open(GUESS_PRECOMPUTED_GUESS_DIRECTORY_NAME, "r") as file:
            best_guess = int(file.readline())
              
        return (best_guess, np.load(GUESS_PRECOMPUTED_TABLE_DIRECTORY_NAME, mmap_mode="r"))
    except:
        return create_best_guesses()

def create_pattern_table() -> np.ndarray:
    """
    Calculates and saves the newly computed Pattern Table as well as returning it.
    """
    
    pattern_table = calculate_pattern_table()
    np.save(GUESS_BYG_TABLE_DIRECTORY_NAME, pattern_table)
    
    return pattern_table

def calculate_pattern_table() -> np.ndarray:
    """
    Calculates the Pattern Table and returns it.
    """

    answers_indexes = word_helper.get_possible_answers_indexes()
    guesses_indexes = word_helper.get_accepted_guesses_indexes()

    len_a = len(answers_indexes)
    len_g = len(guesses_indexes)

    pattern_table = np.zeros((len_a, len_g), dtype=np.uint8)    

    print("Creating Pattern Table")
    for a in answers_indexes:
        print(f"Pattern Table: {a + 1:,} out of {len_a:,} ({(a + 1)/len_a:.2%})")
        for g in guesses_indexes:
            pattern_table[a, g] = get_byg(a, g)
    
    print("Done!\n")

    return pattern_table

def create_best_guesses() -> tuple[str, np.ndarray]:
    """
    Calculates and saves the newly computed best **first** guess and best **second** guesses as well as returning both.
    """
    global pattern_table
    pattern_table = get_pattern_table()
        
    best_first_guess, best_guesses_table = calculate_best_guesses()
    np.save(GUESS_PRECOMPUTED_TABLE_DIRECTORY_NAME, best_guesses_table)

    with open(GUESS_PRECOMPUTED_GUESS_DIRECTORY_NAME, "w") as file:
        file.write(str(best_first_guess))
        
    return best_first_guess, best_guesses_table

def calculate_best_guesses() -> tuple[str, np.ndarray]:
    """
    Calculates the best **first** guess and best **second** guesses and returns it.
    """
        
    best_guesses_table = np.zeros((total_byg_combinations), dtype=np.uint16)    
    
    answers_indexes = np.array(word_helper.get_possible_answers_indexes())
    guesses_indexes = np.array(word_helper.get_accepted_guesses_indexes())

    print("Getting the best first word")
    best_first_guess = get_word(guesses_indexes, answers_indexes)
    print("Done!\n")

    for i in range(total_byg_combinations):
        print(f"Best guess: {i + 1} out of {total_byg_combinations} ({(i + 1)/total_byg_combinations:.2%})")

        remaining_guesses, remaining_answers = shorten_words(guesses_indexes, answers_indexes, best_first_guess, i)
        best_second_word = get_word(remaining_guesses, remaining_answers)
        
        best_guesses_table[i] = best_second_word

    return (best_first_guess, best_guesses_table)

def get_byg(answer:int, guess:int) -> str:
    """
    Calculates the expected pattern of byg for a given answer and guess.
    Example input and output:\n
        get_byg(2213, 1883) -> "vocal", "cache" -> bygbb -> 45

    """
    
    answer_str = word_helper.get_index_to_answer(answer)
    guess_str = word_helper.get_index_to_guess(guess)

    dist = Counter(answer_str)
    response = "b" * max_word_size
    
    for i in range(max_word_size):
        letter = guess_str[i]
        if letter == answer_str[i]: #Green
            response = response[:i] + "g" + response[i + 1:]
            dist[letter] = dist[letter] - 1
    
    for i in range(max_word_size):
        if response[i] == "g":
            continue

        letter = guess_str[i]
        if letter in dist and dist[letter]: #Yellow
            dist[letter] = dist[letter] - 1
            response = response[:i] + "y" + response[i + 1:]
    
    return get_byg_to_int(response)

def get_score(buckets:np.ndarray) -> float:
    return np.sum(buckets * buckets) / np.sum(buckets)

def get_word(accepted_guesses_indexes:list, remaining_words_indexes:list) -> int:
    counts = np.zeros((243, len(accepted_guesses_indexes)), dtype=np.uint32)
    patterns = pattern_table[np.ix_(remaining_words_indexes, accepted_guesses_indexes)]

    for pattern in range(243):
        counts[pattern] = np.sum(patterns == pattern, axis=0)

    scores = np.sum(counts * counts, axis=0)
    best_guess = accepted_guesses_indexes[np.argmin(scores)]
    
    return best_guess

def shorten_words(remaining_guess_indexes:np.ndarray, remaining_answer_indexes:np.ndarray, guess:str, response:str) -> tuple[list, list]:
    global pattern_table
    
    if guess in remaining_guess_indexes:
        remaining_guess_indexes = remaining_guess_indexes[remaining_guess_indexes != guess]

    # remaining_answer_indexes = np.array(remaining_answer_indexes)
    mask = pattern_table[remaining_answer_indexes, guess] == response
    remaining_answer_indexes = remaining_answer_indexes[mask]

    return remaining_guess_indexes, remaining_answer_indexes

if __name__ == "__main__":
    initialize_data()
    if len(sys.argv) > 1:
        if any(flag in sys.argv for flag in ("--pt", "--all")):
            create_pattern_table()
        if any(flag in sys.argv for flag in ("--bg", "--all")):
            create_best_guesses()
else:
    pattern_table = get_pattern_table()
    best_guess, best_guesses = get_best_guesses()
