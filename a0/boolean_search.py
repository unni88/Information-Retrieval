""" Assignment 0
    CS 429      -->         Spring 15
    
    Aditya Shirodkar
    
    Python 2.7 on OS X Yosemite
    
    Started:        22:35, Jan 19, 15
    Completed:      03:00, Jan 22, 15
    Last Modified:  03:00, Jan 22, 15
"""


""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""

# Some imports you may want to use.
from collections import defaultdict
import re


def read_lines(filename):
    """ Read a file to a list of strings. You should not need to modify
    this. """
    return [l.strip() for l in open(filename, 'rt').readlines()]


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    >>> tokenize("Hi there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    temp = re.split('\W+', document)
    
    while '' in temp:
        temp.remove('')
    
    return [x.lower() for x in temp]
    pass


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    >>> index['c']
    [1]
    """
    
    uniqueWords = set(sum(tokens, []))
    
    while '' in uniqueWords:
        uniqueWords.remove('')

    invertedIndex = {word:list(i
                              for i in range(0, len(tokens)) if word in tokens[i])
            for word in uniqueWords}

#invertedIndex = sorted(invertedIndex.keys())

    return invertedIndex
    pass


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    
    return list(set(list1) & set(list2))
    pass


def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index.
    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    
    dict = {}
    temp = {}
    
    for word in words:
        for key in index.keys():
            if word == key:
                temp = {word:index[key]}
                dict.update(temp)

    tempDict = {}
    for key in dict:
        temp = {key:len(dict[key])}
        tempDict.update(temp)

    return sorted(tempDict, key=tempDict.__getitem__)


    """dict = {word:(index[key]
                               for key in index.keys() if word in key)
                    for word in words}
"""

    pass


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that query is a single string, possible containing multiple words. The steps are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.
    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """

    #1
    queryTokens = tokenize(query)

    #2
    sort = sort_by_num_postings(queryTokens, index)
    
    #3
    if len(sort) is 1:
        return index[sort[0]]
    else:
        temp = index[sort[0]]
        for i in range(1, len(sort)):
            return (intersect(temp, index[sort[i]]))

    pass



def main():
    """ Main method. You should not modify this. """
    documents = read_lines('documents.txt')
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = read_lines('queries.txt')
    for query in queries:
        results = search(index, query)
        print '\n\nQUERY:', query, '\nRESULTS:\n', '\n'.join(documents[r] for r in results)


if __name__ == '__main__':
    main()
