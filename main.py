import word_helper, compute_data, time
from wordle_solver_bot import Jarvis
from statistics import mean

def print_result(result:list, file=None):
    guesses, responses, word, passed = result[0], result[1], result[2], result[3]
    print(f"{str(guesses):<54} {str(responses):<54} {word} {passed}")
    print(f"{str(guesses):<54} {str(responses):<54} {word} {passed}", file=file)

def play_all_games(bot:Jarvis, all_possible_answers:list, file=None) -> tuple[list, int, int]:
    start_time = time.time()

    scores = []
    for wordle_answer in all_possible_answers:
        result = bot.play_game(wordle_answer)
        scores.append(result)
        print_result(result, file=file)

    end_time = time.time()
    mins, secs = divmod(end_time - start_time, 60)
    
    return (scores, int(mins), secs)

def get_guess_distribution(guesses_list:list) -> dict:
    guess_distribution = [0] * 6
    for guess in guesses_list:
        guess_distribution[guess - 1] += 1

    return guess_distribution

def print_information_breakdown(scores:list, mins:int, secs:float, file=None):
    #Prints analysis
    fails_list = []
    guesses_list = []
    results_list = []
    successes_list = []
    for score in scores:
        guesses_list.append(len(score[0]))
        results_list.append(len(score[1]))
        successes_list.append(score[3])

        if not score[3]:
            fails_list.append(score)

    total_attempts = len(guesses_list)
    total_successes = successes_list.count(True)
    success_rate = float(total_successes)/total_attempts

    guess_distribution = get_guess_distribution(guesses_list)

    print(f"\nTotal time taken: {mins}m:{secs:.2f}s", file=file)
    print(f"Total attempts: {total_attempts}", file=file)
    print(f"Number of successes: {total_successes}", file=file)
    print(f"Success rate: {success_rate * 100:.5f}%", file=file)
    print(f"Average number of attempts: {mean(guesses_list):.5f}\n", file=file)
    
    print(f"Guess distrubition:", file=file)
    for i in range(len(guess_distribution)):
        print(f"{i + 1} guesses: {guess_distribution[i]:,} ({float(guess_distribution[i])/total_attempts * 100:.2f})%", file=file)

    print(f"Total fails: {len(fails_list)}", file=file)
    for fail in fails_list:
        print(fail)

bot = Jarvis()
all_possible_answers = word_helper.get_possible_answers_indexes()

with open("results.txt", "w") as file:
    data = play_all_games(bot, all_possible_answers, file=file)
    results, mins, secs = data[0], data[1], data[2]

    print_information_breakdown(results, mins, secs)
    print_information_breakdown(results, mins, secs, file=file)
