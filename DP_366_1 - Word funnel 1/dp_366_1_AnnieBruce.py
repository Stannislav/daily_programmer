#!/usr/bin/env python3

'''
Solution by AnnieBruce:

https://www.reddit.com/r/dailyprogrammer/comments/98ufvz/20180820_challenge_366_easy_word_funnel_1/e576cqn/

The speed-up of this solution is due to the use of sets instead of lists,
which have access time O(1)
'''

import doctest
import string


def remove_character_at(str, idx):
    """Removes the character from str at index idx, returning the remaining string
    str, int -> str

    >>> remove_character_at("boats", 2)
    'bots'
    """
    return str[:idx] + str[idx+1:]


def get_shortened_string_list(str):
    """Returns all strings which can be formed by removing a single character
    from str
    str -> str list

    >>> sorted(get_shortened_string_list("bat"))
    ['at', 'ba', 'bt']
    """

    result = set()

    for idx in range(len(str)):
        result.add(remove_character_at(str, idx))

    return result


def funnel(base, test):
    """Tests string against the base string to determine if it can be constructed
    by removing one character from the base string
    str, str -> bool

    >>> funnel("leave", "eave")
    True
    >>> funnel("eave", "leave")
    False
    """
    return test in get_shortened_string_list(base)


def build_word_list(in_file):
    """Processes a list of words stored in file, placing them in a list of lists
    where the outer list index is the number of characters in each word of the
    corresponding inner list
    file -> str set list
    """
    word_list = list()
    for word in in_file:
        word = word.strip()
        # word list hasn't gotten here yet
        if len(word_list) <= len(word):
            # extend the list
            for n in range(len(word_list), len(word) + 1):
                word_list.insert(n, set())
        # insert into appropriate sublist
        word_list[len(word)].add(word)
    return word_list


def bonus(word, word_list):
    """tests word and returns all words from the provided word list which can be
    constructed by removing one letter from word
    str, str set list -> str list

    """
    candidate_words = get_shortened_string_list(word)
    return candidate_words.intersection(word_list[len(word) - 1])


def bonus2(word_list):
    """Finds all potential input words which result in 5 words returned via the
    function bonus
    str set list -> str list"""

    results = list()
    # All words with 5 result words must necessarily have at least five letters
    for idx in range(5, len(word_list)):
        for word in word_list[idx]:
            if len(bonus(word, word_list)) == 5:
                results.append(word)
    return results


if __name__ == "__main__":
    print("Hello, how are you?")
    # load enable1 and generate list
    word_list = build_word_list(open("enable1.txt"))
    print(bonus("dragoon", word_list))
    print(len(bonus2(word_list)))
    doctest.testmod()
