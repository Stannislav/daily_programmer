# Solution from here: https://www.reddit.com/r/dailyprogrammer/comments/8qxpqd/20180613_challenge_363_intermediate_word/e0ppcu4/


import string, urllib.request


# Generator of all positions of 'substr' in 'wrd'
# 'patt' is necessary only to detect if there is a '.'
# at the beginning or the end of 'wrd'
def findAll(wrd, substr, patt):
    if patt[0] == '.':
        yield wrd.index(substr)
    elif patt[-1] == '.':
        yield wrd.rindex(substr)
    else:
        index = wrd.find(substr)
        while index != -1:
            yield index
            index = wrd.find(substr, index + 1)


bonus = False  # set to False if you want to input your own words


# Transform the raw rules into a dictionary called 'patterns'.
# 'patterns' has entries of the form
# 'scie': (('scie', '.sci3e', (4,)), ('scie', '3s4cie', (0, 2)))
patterns = {}
for line in open("tex-hyphenation-patterns.txt"):
    line = line.strip()
    substring = line.translate({ord(k): None for k in string.digits + string.punctuation})
    if substring in patterns:
        patterns[substring] += ((substring, line,) + (tuple(pos for pos in range(len(line)) if line[pos].isdigit()),),)
    else:
        patterns[substring] = ((substring, line,) + (tuple(pos for pos in range(len(line)) if line[pos].isdigit()),),)

# Get words from either a file or the user in put in hyphenate them
word_hyphen_count = dict.fromkeys(range(10), 0)
file_words = open("enable1.txt", 'r')
word = file_words.readline().rstrip() if bonus else input('Enter your word >>> ').rstrip()
while word:
    # generate all substrings of 'word' of at most 8 characters long
    substrings = list(dict.fromkeys([substring
        for length in range(2, min(len(word), 8) + 1)
            for substring in (word[i:i + length]
                for i in range(len(word)) if i + length <= len(word))
    ]))

    # extract all patterns that match any of the substrings just generated
    pattern_subs = [elem
        for sub in substrings if sub in patterns
            for elem in patterns[sub] if
            (
                (elem[1][0] == '.' and word[:len(elem[0])] == elem[0]) or
                (elem[1][-1] == '.' and word[-len(elem[0]):] == elem[0]) or
                ('.' not in elem[1])
            )
    ]

    # apply all patterns found to 'word' and
    # save hyphenation value in 'value_list'
    value_list = [0] * (len(word) + 1)
    for pattern in pattern_subs:
        for word_position in findAll(word, pattern[0], pattern[1]):
            for pattern_value_position, value_position in enumerate(pattern[2]):
                idx = word_position + value_position - pattern_value_position
                if pattern[1][0] == '.':
                    idx -= 1
                value_list[idx] = max(value_list[idx], int(pattern[1][value_position]))
    word_list = list(word)

    for position in range(1, len(value_list) - 1)[::-1]:
        if value_list[position] % 2 != 0:
            word_list.insert(position, '-')

    if bonus:
        word_hyphen_count[word_list.count('-')] += 1
    else:
        print(''.join(word_list))

    word = file_words.readline().rstrip() if bonus else input('Enter your word >>> ').rstrip()
print(word_hyphen_count)
