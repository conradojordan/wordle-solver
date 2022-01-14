import re
from collections import Counter

all_words = [word.strip() for word in open("words")]


def letter_frequency(words):
    return Counter("".join(words)).most_common(26)


def remove_words_with_duplicate_letters(words):
    return [word for word in words if len(set(word)) == len(word)]


def rank_word_by_letter_frequency(word, frequency):
    freq = [l[0] for l in frequency]
    total = 0
    for letter in word:
        total += 26 - freq.index(letter)
    return total


def find_next_best_word(words):
    freq = letter_frequency(words)
    for i in range(5, 26):
        current_letters = freq[:i]
        current_letters = "".join([l[0] for l in current_letters])
        regex = re.compile(r"^[" + current_letters + r"]{5}$")
        found_words = [word for word in words if regex.search(word)]
        found_words = remove_words_with_duplicate_letters(found_words)
        if found_words:
            break
    sorted_words = sorted(
        found_words, key=lambda x: rank_word_by_letter_frequency(x, freq)
    )
    return sorted_words[0]


def update_words_by_removing_last_guess(words, last_guess):
    regex = re.compile(r"[" + last_guess + r"]")
    return [word for word in words if not regex.search(word)]
