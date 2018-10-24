#!/usr/bin/env python3


test_words = [
    ["mistranslate", "mis-trans-late"],
    ["alphabetical", "al-pha-bet-i-cal"],
    ["bewildering", "be-wil-der-ing"],
    ["buttons", "but-ton-s"],
    ["ceremony", "cer-e-mo-ny"],
    ["hovercraft", "hov-er-craft"],
    ["lexicographically", "lex-i-co-graph-i-cal-ly"],
    ["programmer", "pro-gram-mer"],
    ["recursion",  "re-cur-sion"],
]


def process_rule(rule):
    '''
    Transforms a raw rule of the form "e4f3ere" into
    a pure string "efere" and a list of weights for
    the hyphenation "[0, 4, 3, 0, 0, 0]" so that the
    the hyphenation rule is given by intertwining the two to
    0 e 4 f 3 e 0 r 0 e 0
    '''
    rule_original = rule  # save for the error message
    rule_text = ""
    rule_weights = []
    result = []

    # we will process each letter together with the weight for the
    # space following it so that the first weight needs to be handled
    # separately
    if rule[0].isdigit():
        rule_weights += [int(rule[0])]
        rule = rule[1:]
    else:
        rule_weights += [0]

    n_text = 0
    n_weights = 0
    for c in rule:
        if c.isdigit():
            rule_weights += [int(c)]
            n_weights += 1
            # now we should have n_weights == n_text
        else:
            # if a letter was not followed by a digit it's an implicit 0
            if n_text == n_weights + 1:
                rule_weights += [0]
                n_weights += 1
            if n_text != n_weights:
                # this can only happen if there were two consecutive digits,
                # which is not allowed
                print(f"Bad input for process_rule: {rule_original}")
                return None
            rule_text += c
            n_text += 1
    if len(rule_weights) == len(rule_text):
        rule_weights += [0]
    result += [rule_text, rule_weights]
    return result


# Read and process the rules
rules_dict = {}
max_rule_len = 0
for rule in open("tex-hyphenation-patterns.txt", 'r'):
    rule = rule.strip()
    wrd, patt = process_rule(rule)
    # if the dots are kept then each pattern without the numbers is unique
    # so each rules_dict[wrd] can only have one entry
    rules_dict[wrd] = (wrd, patt)
    max_rule_len = max(len(wrd) + 1 if '.' in rule else len(wrd), max_rule_len)


def hyphenate(word):
    '''
    returns the word together with its hyphenation weights, e.g.
    'hello' => ['hello', [0, 2, 3, 4]]
    so that the hyphenation has to be performed according to
    h   e   l   l   o
      0   2   3   4
    and gives 'hel-lo'
    '''

    # add dots at the beginning and the end of the word
    # in order to automatically match the corresponding patterns
    xword = "." + word + "."
    weights = [0] * (len(xword) + 1)

    xword_subs = [xword[i:i + l] for l in range(2, max_rule_len + 1) for i in range(len(xword) - l + 1) if xword[i:i + l] in rules_dict]

    for sub in xword_subs:
        [rule_text, rule_weights] = rules_dict[sub]
        # if rule_text is found in word then apply rule_weights to weights
        pos = xword.find(rule_text)
        while pos >= 0:
            for n in range(len(rule_text) + 1):
                weights[pos + n] = max(weights[pos + n], rule_weights[n])
            # print(rule_text + " " + str(rule_weights))
            # print(apply_hypenation(word, weights[2:-2]))
            # print()
            pos = xword.find(rule_text, pos + 1)

    # we don't need the weights around the dots at the beginning
    # and the end of the word so we trim them
    return [word, weights[2:-2]]


def apply_hypenation(word, hyph):
    '''
    word: word to hyphenate
    hyph: hyphenaton rules; hyph[n] describes the space after word[n]

    the word has to be hyphenated at all odd values of weights in hyph
    '''

    if len(word) - 1 != len(hyph):
        return f"Wrong input: word = {word} ({len(word)}), hyph = {hyph} ({len(hyph)})"

    out = ""
    i = 0
    for n in range(len(word) - 1):
        if hyph[n] % 2 == 1:  # so there's a hyphen after word[n]
            out += word[i:n+1] + "-"
            i = n + 1
    out += word[i:]

    return out


# Do the test cases
print("> Test cases:")
for [word, solution] in test_words:
    word_res = apply_hypenation(*hyphenate(word))
    print(
        f"{word} => {word_res} "
        f"({'correct' if solution == word_res else 'INCORRECT'})"
    )
print("> Test cases finished. Check output above.")
print()


# Hyphenate words in file
fout = open("enable1_hypenated.txt", 'w')
counts = dict.fromkeys(range(10), 0)
print("> Hyphenating words in file...")
for line in open("enable1.txt", 'r'):
    res = apply_hypenation(*hyphenate(line.strip()))
    counts[res.count('-')] += 1
    fout.write(f"{line.strip()} => {res}\n")
fout.close()
print("> Done hyphenating.")
print(counts)


# print(apply_hypenation(*hyphenate("lexicographically")))
# print(hyphenate("hello"))
