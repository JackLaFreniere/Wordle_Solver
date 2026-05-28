import argparse
import re
from pathlib import Path

DATA_DIR = Path("data/text_files")
DEFAULT_INPUT = DATA_DIR / "wordle_js_words.txt"
ACCEPTED_GUESSES = DATA_DIR / "accepted_guesses.txt"
POSSIBLE_ANSWERS = DATA_DIR / "possible_answers.txt"

def extract_words(text: str) -> list[str]:
    words = re.findall(r"[a-z]{5}", text.lower())
    unique_words = []
    seen = set()

    for word in words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)

    return unique_words

def find_answer_start(words: list[str]) -> int:
    for i in range(1, len(words)):
        if words[i] < words[i - 1]:
            return i

    raise ValueError("Could not find where the alphabetized guess list ends.")

def write_words(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(words) + "\n")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import NYT Wordle JS words into accepted and possible answer text files."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Text file containing pasted JS/list content. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--answers-count",
        type=int,
        help="Use the final N words as possible answers instead of auto-detecting the split.",
    )
    args = parser.parse_args()

    text = args.input.read_text()
    accepted_words = extract_words(text)

    if args.answers_count is None:
        answer_start = find_answer_start(accepted_words)
    else:
        if args.answers_count <= 0 or args.answers_count > len(accepted_words):
            raise ValueError("--answers-count must be between 1 and the total word count.")
        answer_start = len(accepted_words) - args.answers_count

    possible_answers = accepted_words[answer_start:]

    write_words(ACCEPTED_GUESSES, accepted_words)
    write_words(POSSIBLE_ANSWERS, possible_answers)

    print(f"Imported {len(accepted_words):,} accepted guesses.")
    print(f"Imported {len(possible_answers):,} possible answers.")
    print(f"Answer list starts at accepted-guesses index {answer_start:,}.")
    print(f"Wrote {ACCEPTED_GUESSES}")
    print(f"Wrote {POSSIBLE_ANSWERS}")

if __name__ == "__main__":
    #https://www.nytimes.com/games-assets/v2/9201.d9fecfacd1fb666dd70b.js
    main()
