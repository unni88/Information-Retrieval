1. Extend the postings merge algorithm to arbitrary Boolean query formulas. What is
its time complexity? For instance, consider:

`(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)`

Can we always merge in linear time? Linear in what? Can we do better than this?

ANS:    Boolean query formula:      LIST(SET(p1) AND SET(p2))
The time complexity is O(x+y) where x is length of p1 and y is length of p2

(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)



2. If the query is:

`friends AND romans AND (NOT countrymen)`

How could we use the frequency of countrymen in evaluating the best query evaluation order? In particular, propose a way of handling negation in determining the order of query processing.

ANS:    If the frequency of countrymen is less, we can check the documents with friends and romans and then discard the one with countrymen. And if the frequency is more than we can           discard countrymen first and later look for documents with friends and romans in it.


Instead of checking 'friends' and 'romans' in all documents and then discarding those containing 'countrymen', we can first discard the documents that contains 'countrymen' and later check for the documents which contains 'friend' and 'document'.

1. Locate 'countrymen' in the dictionary and discard it.
2. Locate 'friend' in the dictionary.
3. Retrieve its postings.
4. Locate 'romans' in the dictionary.
5. Retrieve its postings.
6. Intersect the two postings.


3. For a conjunctive query, is processing postings lists in order of size guaranteed to be
optimal? Explain why it is, or give an example where it isn’t.

ANS:    YES, It is optimal.
Consider a example of 'friends AND romans AND countrymen' and postings of them are 5, 7, 4 respectively.
Since the frequency of countrymen is 4 (i.e less than the other two), we can take a intersection of it with either friends or romans. And the result will contain less than 4 items in the list, which we can use to intersect with the left one.

