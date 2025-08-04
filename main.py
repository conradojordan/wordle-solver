import re
from collections import Counter

ALL_WORDS: list[str] = [word.strip() for word in open("words")]


def letter_frequency(words: list[str]) -> list[tuple[str, int]]:
    return Counter("".join(words)).most_common(26)


def rank_word_by_letter_frequency(word: str, frequency: list[tuple[str, int]]):
    freq = [letter[0] for letter in frequency]
    total = 0
    for letter in word:
        total += 26 - freq.index(letter)
    return total


def find_next_best_word(words: list[str], *, remove_duplicate_letters: bool = False):
    freq = letter_frequency(words)
    found_words: list[str] = list()

    for i in range(5, 26):
        current_letters = freq[:i]
        current_letters = "".join([l[0] for l in current_letters])
        regex = r"^[" + current_letters + r"]{5}$"
        regex = re.compile(regex)
        found_words = [word for word in words if regex.search(word)]
        if remove_duplicate_letters:
            found_words = [word for word in found_words if len(set(word)) == len(word)]
        if len(found_words) > 5:
            break
    sorted_words = sorted(
        found_words, key=lambda x: rank_word_by_letter_frequency(x, freq), reverse=True
    )
    return sorted_words[:5]


def update_words_with_new_information(
    words: list[str], known_letters: dict[str, list[str]]
) -> tuple[list[str], dict[str, list[str]]]:
    # Positional letters
    regex = "^"
    for letter in known_letters["positional"]:
        regex += letter if letter else "."
    regex += "$"
    regex = re.compile(regex)
    words = [word for word in words if regex.search(word)]

    # Regular letters
    for letter in known_letters["regular"]:
        regex = re.compile(letter)
        words = [word for word in words if regex.search(word)]
    known_letters["regular"] = list()

    # Positional not found letters
    regex = "^"
    for letters in known_letters["positional_not_found"]:
        regex += ("[^" + letters + "]") if letters else "."
    regex += "$"
    regex = re.compile(regex)
    words = [word for word in words if regex.search(word)]

    # Not found letters
    if known_letters["not_found"]:
        regex = re.compile("[" + "".join(known_letters["not_found"]) + "]")
        words = [word for word in words if not regex.search(word)]
        known_letters["not_found"] = list()

    return words, known_letters


def is_valid_result(result: str) -> bool:
    if not set(result).issubset({"x", "g", "y"}):
        return False

    if len(result) != 5:
        return False

    return True


def get_guess_result(known_letters: dict[str, list[str]], guess: str):
    print("Enter the result of the guess.", end=" ")
    print("Use 'x' for wrong, 'g' for green and 'y' for yellow (example 'xxgxy')")
    result = input("Enter guess result: ").lower()

    while not is_valid_result(result):
        print(
            "The given guess result is invalid, please enter 5 characters comprised of the letters 'x', 'g' and 'y'."
        )
        print(
            "For example, enter 'gxgxy' if the first and third letters are green, the last one is yellow and the others are gray."
        )
        result = input("Enter guess result: ").lower()

    for index, result_letter in enumerate(result):
        guess_letter = guess[index]
        match result_letter:
            case "g":
                known_letters["positional"][index] = guess_letter
            case "y":
                if guess_letter not in known_letters["regular"]:
                    known_letters["regular"].append(guess_letter)

                if guess_letter not in known_letters["positional_not_found"][index]:
                    known_letters["positional_not_found"][index] += guess_letter
            case "x":
                known_letters["not_found"].append(guess_letter)
            case _:
                continue

    return known_letters


if __name__ == "__main__":
    words = ALL_WORDS.copy()
    known_letters: dict[str, list[str]] = {
        "positional": ["" for _ in range(5)],
        "regular": [],
        "positional_not_found": ["" for _ in range(5)],
        "not_found": [],
    }
    previous_guesses: list[str] = list()

    print(
        f"Suggested first guesses: {', '.join(find_next_best_word(ALL_WORDS, remove_duplicate_letters=True))}"
    )

    while True:
        print("\n" + "Next round!".center(30, "-"))
        guess = input(
            "Enter this round's guess (or press enter if game is finished): "
        ).lower()
        if not guess:
            break
        previous_guesses.append(guess)

        known_letters: dict[str, list[str]] = get_guess_result(known_letters, guess)

        words, known_letters = update_words_with_new_information(words, known_letters)

        # Do not suggest already guessed words
        next_guesses = find_next_best_word(words)
        for next_guess in next_guesses:
            if next_guess in previous_guesses:
                next_guesses.remove(next_guess)

        print(f"\nSuggested next guesses: {', '.join(next_guesses)}")
    print("---- Congratulations on winning the game!!!! ----")
