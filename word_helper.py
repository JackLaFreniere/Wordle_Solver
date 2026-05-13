def get_words() -> list:
    lines = []
    with open("answers.txt") as file:
        lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i][:5]
    
    return lines