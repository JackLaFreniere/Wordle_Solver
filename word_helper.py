def get_possible_answers() -> list:
    return get_files("text_files/possible_answers.txt")

def get_accepted_guesses() -> list:
    return get_files("text_files/accepted_guesses.txt")

def get_files(name:str) -> list:
    lines = []
    with open(name) as file:
        lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i][:5]
    
    return lines