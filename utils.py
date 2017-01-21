from itertools import islice, repeat, starmap, takewhile

def chunker(iterable, n):
    return takewhile(bool,
                     map(tuple,
                         starmap(islice,
                                 repeat((iter(iterable),
                                         n)))))
