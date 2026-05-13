import bot, word_helper
from statistics import mean, median, mode

lines = word_helper.get_words()

jarvis = bot.Jarvis()
scores = []
for line in lines:
    result = jarvis.play_game(line)
    scores.append(result)

#Prints analysis
guesses = []
results = []
successes = []
for score in scores:
    guesses.append(len(score[0]))
    results.append(len(score[1]))
    successes.append(score[2])

total_attempts = len(guesses)
total_successes = successes.count(True)
success_rate = float(total_successes)/total_attempts

print(f"Total attempts: {total_attempts}")
print(f"Number of successes: {total_successes}")
print(f"Success rate: {success_rate * 100:.5f}%")
print(f"Average number of attempts: {mean(guesses):.5f}")