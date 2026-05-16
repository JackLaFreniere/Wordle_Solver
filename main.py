
import bot, word_helper, threading
from statistics import mean, median, mode

lines = word_helper.get_possible_answers()

jarvis1 = bot.Jarvis()
jarvis2 = bot.Jarvis()
jarvis3 = bot.Jarvis()
jarvis4 = bot.Jarvis()

scores = []
# print(jarvis.play_game("creed"))
for line in lines:
    result = jarvis1.play_game(line)
    scores.append(result)
    print(result)

#Prints analysis
guesses = []
results = []
successes = []
for score in scores:
    guesses.append(len(score[0]))
    results.append(len(score[1]))
    successes.append(score[3])

total_attempts = len(guesses)
total_successes = successes.count(True)
success_rate = float(total_successes)/total_attempts

print(f"Total attempts: {total_attempts}")
print(f"Number of successes: {total_successes}")
print(f"Success rate: {success_rate * 100:.5f}%")
print(f"Average number of attempts: {mean(guesses):.5f}")
