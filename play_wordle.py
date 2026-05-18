import compute_data
from wordle_solver_bot import Jarvis

jarvis = Jarvis(compute_data.get_pattern_table(), compute_data.get_best_guesses())
jarvis.play_game("", True)
