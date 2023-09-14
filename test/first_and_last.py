from heapq import nlargest as _nlargest
from collections import namedtuple as _namedtuple
from types import GenericAlias
from difflib import SequenceMatcher
#from difflib import get_close_matches

lista = ['PapF', 'AtpF']
palabra = 'AtpF'


def get_close_matches(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return list of the best "good enough" matches.

    word is a sequence for which close matches are desired (typically a
    string).

    possibilities is a list of sequences against which to match word
    (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to
    return.  n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
    that don't score at least that similar to word are ignored.

    The best (no more than n) matches among the possibilities are returned
    in a list, sorted by similarity score, most similar first.

    >>> get_close_matches("appel", ["ape", "apple", "peach", "puppy"])
    ['apple', 'ape']
    >>> import keyword as _keyword
    >>> get_close_matches("wheel", _keyword.kwlist)
    ['while']
    >>> get_close_matches("Apple", _keyword.kwlist)
    []
    >>> get_close_matches("accept", _keyword.kwlist)
    ['except']
    """

    if not n > 0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), x))

    print(result)

    # Move the best scorers to head of list
    result = _nlargest(n, result)
    # Strip scores for the best n matches
    return [x for score, x in result]


print(get_close_matches(palabra, lista, cutoff=0.4))


def first_and_last(word):
    letters = list(word)
    letters[0] = letters[0].capitalize()
    print(f'First: {letters[0]}\tLast: {letters[-1]}')
    return "".join(letters)


# print(first_and_last('araC'))
