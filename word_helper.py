import copy

possible_answers = []
accepted_guesses = []

def get_possible_answers() -> list:
    global possible_answers

    if possible_answers:
        return copy.deepcopy(possible_answers)
    else:
        possible_answers = get_files("data/text_files/possible_answers.txt")
        return possible_answers

def get_accepted_guesses() -> list:
    global accepted_guesses

    if accepted_guesses:
        return copy.deepcopy(accepted_guesses)
    else:
        accepted_guesses = get_files("data/text_files/accepted_guesses.txt")
        return accepted_guesses

def get_files(name:str) -> list:
    lines = []
    with open(name) as file:
        lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i][:5]
    
    return lines