import compute_data
from bot import Jarvis

jarvis = Jarvis(compute_data.get_pattern_table(), compute_data.get_best_guesses())
jarvis.play_game("", True)
