from compute_data import get_pattern_table, get_best_guesses, get_best_guesses
from wordle_solver_bot import Jarvis

bot = Jarvis(get_pattern_table(), get_best_guesses())
bot.play_game("", True)
