import re
from collections import Counter

all_words = [word.strip() for word in open("words")]


def letter_frequency(words):
    return Counter("".join(words)).most_common(26)


def rank_word_by_letter_frequency(word, frequency):
    freq = [l[0] for l in frequency]
    total = 0
    for letter in word:
        total += 26 - freq.index(letter)
    return total


def find_next_best_word(words, *, remove_duplicate_letters=False):
    freq = letter_frequency(words)
    found_words = list()

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


def update_words_with_new_information(words, known_letters):
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


def get_found_positional_letters(known_letters):
    if input("Did you find any positional letters (y/N)? ").lower() == "y":
        while True:
            letter = input(
                "Enter positional letter (or press enter to continue): "
            ).lower()
            if not letter:
                break
            letter_position = int(input("Enter the position of the letter (1-5): ")) - 1
            known_letters["positional"][letter_position] = letter
    return known_letters


def get_found_regular_letters(known_letters):
    if (
        input("Did you find any regular (non-positional) letters (y/N)? ").lower()
        == "y"
    ):
        while True:
            letter = input("Enter found letter (or press enter to continue): ").lower()
            if not letter:
                break
            known_letters["regular"].append(letter)
            letter_position = int(input("Enter the position of the letter (1-5): ")) - 1
            known_letters["positional_not_found"][letter_position] += letter
    known_letters["regular"] = list(set(known_letters["regular"]))
    return known_letters


if __name__ == "__main__":
    words = all_words.copy()
    known_letters = {
        "positional": ["" for i in range(5)],
        "regular": [],
        "positional_not_found": ["" for i in range(5)],
        "not_found": [],
    }
    previous_guesses = list()

    print(
        f"Suggested first guesses: {', '.join(find_next_best_word(all_words, remove_duplicate_letters=True))}"
    )

    while True:
        print("\n" + "Next round!".center(30, "-"))
        guess = input(
            "Enter this round's guess (or press enter if game is finished): "
        ).lower()
        if not guess:
            break
        previous_guesses.append(guess)

        known_letters = get_found_positional_letters(known_letters)
        known_letters = get_found_regular_letters(known_letters)
        known_letters["not_found"] += list(
            set(guess)
            - set(known_letters["positional"])
            - set(known_letters["regular"])
        )
        known_letters["not_found"] = list(set(known_letters["not_found"]))
        words, known_letters = update_words_with_new_information(words, known_letters)

        # Do not suggest already guessed words
        next_guesses = find_next_best_word(words)
        for next_guess in next_guesses:
            if next_guess in previous_guesses:
                next_guesses.remove(next_guess)

        print(f"\nSuggested next guesses: {', '.join(next_guesses)}")
    print("---- Congratulations on winning the game!!!! ----")
