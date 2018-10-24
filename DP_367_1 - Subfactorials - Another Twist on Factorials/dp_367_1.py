#!/usr/bin/env python3

'''
TITLE:
[2018-09-04] Challenge #367 [Easy] Subfactorials - Another Twist on Factorials

LINK:
https://www.reddit.com/r/dailyprogrammer/comments/9cvo0f/20180904_challenge_367_easy_subfactorials_another/

DERIVATION:
Start with n numbers 1...n, and n slots #1...#n. Take the number 1 and place it
in some slot #x, there are (n-1) possible choices for this. Now x can be placed
in any of the remaining free slots, including #1, since its own slot is already
occupied by the 1. There are !(n-1) possibilities where x never appears in slot
#1, and !(n-2) possibilities, where x is always in slot #1.
'''

def subfactorial(n):
    if n <= 0 or n != int(n):
        raise ValueError(f"n must be a positive integer! (input: n = {n})")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return (n-1) * (subfactorial(n-1) + subfactorial(n-2))


# Test cases
assert(subfactorial(1) == 0)
assert(subfactorial(2) == 1)
assert(subfactorial(3) == 2)
assert(subfactorial(4) == 9)
assert(subfactorial(5) == 44)

# Challenge
assert(subfactorial(6) == 265)
assert(subfactorial(9) == 133496)
assert(subfactorial(14) == 32071101049)

# Final output
print("All tests passed!")
print(f"subfactorial(15) = {subfactorial(15)}")
print()
