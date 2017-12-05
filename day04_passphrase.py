"""
http://adventofcode.com/2017/day/4
"""

def is_valid(passphrase: str) -> bool:
    """
    A passphrase is valid if it has no repeated words
    """
    words = passphrase.split()
    num_words = len(words)
    num_distinct_words = len(set(words))
    return num_words == num_distinct_words

assert is_valid("aa bb cc dd ee")
assert not is_valid("aa bb cc dd aa")
assert is_valid("aa bb cc dd aaa")

def is_valid2(passphrase: str) -> bool:
    words = passphrase.split()
    num_words = len(words)
    non_anagrams = {tuple(sorted(word)) for word in words}
    num_non_anagrams = len(non_anagrams)
    return num_words == num_non_anagrams

assert is_valid2("abcde fghij")
assert not is_valid2("abcde xyz ecdab")
assert is_valid2("a ab abc abd abf abj")
assert is_valid2("iiii oiii ooii oooi oooo")
assert not is_valid2("oiii ioii iioi iiio")

if __name__ == "__main__":
    with open("day04_input.txt", "r") as f:
        passphrases = [line.strip() for line in f]
    valid_passphrases = [pp for pp in passphrases if is_valid(pp)]
    print(len(valid_passphrases))

    valid_passphrases2 = [pp for pp in passphrases if is_valid2(pp)]
    print(len(valid_passphrases2))
