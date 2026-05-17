import bot, word_helper, compute_data
from statistics import mean, median, mode

jarvis = bot.Jarvis(compute_data.get_pattern_table(), compute_data.get_best_guesses())
all_possible_answers = word_helper.get_possible_answers()

scores = []
# print(jarvis.play_game("creed"))
for wordle_answer in all_possible_answers:
    result = jarvis.play_game(wordle_answer)
    scores.append(result)
    print(result)

#Prints analysis
fails = []

guesses = []
results = []
successes = []
for score in scores:
    guesses.append(len(score[0]))
    results.append(len(score[1]))
    successes.append(score[3])
    if not score[3]:
        fails.append(score)

total_attempts = len(guesses)
total_successes = successes.count(True)
success_rate = float(total_successes)/total_attempts

print(f"\nTotal attempts: {total_attempts}")
print(f"Number of successes: {total_successes}")
print(f"Success rate: {success_rate * 100:.5f}%")
print(f"Average number of attempts: {mean(guesses):.5f}\n")

print(f"Total fails: {len(fails)}")
for fail in fails:
    print(fail)