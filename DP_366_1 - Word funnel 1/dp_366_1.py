#!/usr/bin/env python3


def funnel(word1, word2):
    '''
    Test if  word2 can be obtained by removing one letter from word1.

    Here we will not make use of the tree structure introduced below,
    but just compare both words letter by letter.
    '''
    if len(word2) != len(word1) - 1:
        return False

    removed = 0
    for i in range(len(word2)):
        if word1[i+removed] != word2[i]:
            if removed:
                return False
            else:
                removed = 1

    return True


def insert_word(word, tree):
    '''
    We want to save all our words in a tree where nodes are the
    letters in the words and one can recover all words by following
    the branches.

    This function inserts one given word into the tree.

    We optimized the tail recursion into a while loop.
    '''
    while len(word) > 0:
        # Insert the first letter and recurse to insert the rest of the word
        if word[0] not in tree:
            tree[word[0]] = dict()
        word, tree = word[1:], tree[word[0]]
    tree[0] = True  # Indicate the end of word by a zero


def in_tree(word, tree):
    '''
    Check if a given word is in the tree. This is easily done
    by recursively following the branches in the tree.

    We optimized the tail recursion into a while loop.
    '''

    while len(word) > 0:
        if word[0] not in tree:
            return False
        word, tree = word[1:], tree[word[0]]

    return 0 in tree


def bonus(word):
    newwords = [word[:i] + word[i+1:] for i in range(len(word))]
    return set([w for w in newwords if in_tree(w, word_tree)])


# Read words from file
word_cache = [word.strip() for word in open('enable1.txt', 'r')]

# Build letter tree
print("Building the letter tree ... ", end='', flush=True)
word_tree = dict()
for i in range(len(word_cache)):
        insert_word(word_cache[i], word_tree)
print("done")

# Test Cases
assert funnel("leave", "eave") == True
assert funnel("reset", "rest") == True
assert funnel("dragoon", "dragon") == True
assert funnel("eave", "leave") == False
assert funnel("sleet", "lets") == False
assert funnel("skiff", "ski") == False

# Test Cases Bonus 1
assert bonus("dragoon") == set(["dragon"])
assert bonus("boats") == set(["oats", "bats", "bots", "boas", "boat"])
assert bonus("affidavit") == set([])

# Test Cases Bonus 2
cnt = 0
for i in range(len(word_cache)):
    result = bonus(word_cache[i])
    if len(result) == 5:
        cnt += 1
        print("{:2d}. {:12s}: {}".format(cnt, word_cache[i], ', '.join(result)))


assert cnt == 28
