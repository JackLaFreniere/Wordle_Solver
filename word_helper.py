import copy
import numpy as np

possible_answers = []
accepted_guesses = []

possible_answers_indexes = []
accepted_guesses_indexes = []

def get_possible_answers() -> list:
    """
    Returns a list of all of the words that could be the possible answer
    """
    global possible_answers

    if not possible_answers:
        possible_answers = get_files("data/text_files/possible_answers.txt")

    return copy.deepcopy(possible_answers)

def get_accepted_guesses() -> list:
    """
    Returns a list of all of the words that are an accepted guess
    """
    global accepted_guesses

    if not accepted_guesses:
        accepted_guesses = get_files("data/text_files/accepted_guesses.txt")
    
    return copy.deepcopy(accepted_guesses)
    
def get_possible_answers_indexes() -> list:
    """
    Returns a list of indexes that correspond to the indexes of the possible_answers list
    """
    global possible_answers_indexes, possible_answers

    if not possible_answers_indexes:
        if not possible_answers:
            possible_answers = get_possible_answers()
        
        possible_answers_indexes = list(range(len(possible_answers)))

    return possible_answers_indexes

def get_accepted_guesses_indexes() -> list:
    """
    Returns a list of indexes that correspond to the indexes of the accepted_guesses list
    """
    global accepted_guesses_indexes, accepted_guesses

    if not accepted_guesses_indexes:
        if not accepted_guesses:
            accepted_guesses = get_accepted_guesses()
        
        accepted_guesses_indexes = list(range(len(accepted_guesses)))
    
    return accepted_guesses_indexes

def get_index_to_answer(index:int) -> str:
    """
    Gets the word as a string that is associated with the index of the answer.
    """
    global possible_answers

    return possible_answers[index]

def get_index_to_guess(index:int) -> str:
    """
    Gets the word as a string that is assocated with the idnex of the guess.
    """
    global accepted_guesses

    return accepted_guesses[index]

def get_files(name:str) -> list:
    """
    Returns a list that contains all of the lines of a text file with the \\n ommited from each line.
    """

    lines = []
    with open(name) as file:
        lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i][:5]
    
    return lines