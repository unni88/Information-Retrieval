Edit this file in your private repository to provide answers to the following questions.

1. Consider merging the following two lists, where the first list has skip pointers.
![skips](skips.png)
  1. How often is a skip pointer followed (i.e., p1 is advanced to skip(p1))?

    ANS:
        Only once from 24 to 75

  2. How many postings comparisons will be made by this algorithm while intersecting the two lists?

    ANS:
    According to the algorithm given in figure 2.10


    | # of Comparasion |       Comparasion        |                         |
    |------------------|--------------------------|-------------------------|
    |       **1**      |         3 == 3           | Two comparasions(3, 24) |
    |       **2**      |         5 == 5           |                         |
    |       **3**      |         9 < 89           |                         |
    |       **4**      |        15 < 89           |                         |
    |       **5**      |   24 < 89  OR 75 < 89    |          SKIP           |
    |       **6**      |        81 < 89           |                         |
    |       **7**      |        84 < 89           |                         |
    |       **8**      |        89 == 89          |                         |
    |       **9**      |        92 < 95           |Two comparasions(92, 115)|
    |       **10**     |        96 > 95           |                         |
    |       **11**     |        96 < 97           |                         |
    |       **12**     |        97 == 97          |                         |
    |       **13**     |        100 > 99          |                         |
    |       **14**     |        100 == 100        |                         |
    |       **15**     |        115 > 101         |                         |                         

    So total comparasions are 15 plus 4 skips which is 19.
    
  
  3. How many postings comparisons would be made if the postings lists are intersected without the use of skip pointers?

    ANS:

    | # of Comparasion |       Comparasion        |                           |
    |------------------|--------------------------|---------------------------|
    |       **1**      |         3 == 3           |           match           |
    |       **2**      |         5 == 5           |           match           |
    |       **3**      |         9 < 89           | list1 pointer incremented |
    |       **4**      |        15 < 89           | list1 pointer incremented |
    |       **5**      |        24 < 89           | list1 pointer incremented |
    |       **6**      |        39 < 89           | list1 pointer incremented |
    |       **7**      |        60 < 89           | list1 pointer incremented |
    |       **8**      |        68 < 89           | list1 pointer incremented |
    |       **9**      |        75 < 89           | list1 pointer incremented |
    |       **10**     |        81 < 89           | list1 pointer incremented |
    |       **11**     |        84 < 89           | list1 pointer incremented |
    |       **12**     |        89 == 89          |           match           |
    |       **13**     |        92 < 95           | list1 pointer incremented |
    |       **14**     |        96 > 95           | list2 pointer incremented |
    |       **15**     |        96 < 97           | list1 pointer incremented |
    |       **16**     |        97 == 97          |           match           |
    |       **17**     |        96 < 97           | list1 pointer incremented |
    |       **18**     |        100 > 99          | list2 pointer incremented |
    |       **19**     |        100 == 100        |           match           |
    |       **20**     |        115 > 101         |     END OF BOTH LISTS     |

    So total number of comparasions is 20.


2. Compute the Levenshtein edit distance between *paris* and *alice*. Fill in the 5 × 5 table below of
distances between all preﬁxes as computed by the algorithm in Figure 3.5 in [MRS](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf). Cell (*i*, *j*) should store the minimum edit distance between the first *i* characters of *alice* and the first *j* characters of *paris* (as in the bottom right number of each cell in Figure 3.6).

    ANS: Edit Distance = 4

  |       |   | p | a | r | i | s |
  |-------|---|---|---|---|---|---|
  |       | 0 | 1 | 2 | 3 | 4 | 5 |
  | **a** | 1 | 1 | 1 | 2 | 3 | 4 |
  | **l** | 2 | 2 | 2 | 2 | 3 | 4 |
  | **i** | 3 | 3 | 3 | 3 | 2 | 3 |
  | **c** | 4 | 4 | 4 | 4 | 3 | 3 |
  | **e** | 5 | 5 | 5 | 5 | 4 | 4 |


3. (Inspired by [H Schütze](http://www.cis.uni-muenchen.de/~hs/teach/13s/ir/).)We define a *hapax legomenon* as a term that occurs exactly once in a collection. We want to estimate the number of hapax legomena using Heaps’ law and Zipf’s law.
    1. How many unique terms does a web collection of 400,000,000 web pages containing 400 tokens on average have? Use the Heaps parameters k = 100 and b = 0.5.
    2. Use Zipf’s law to estimate the proportion of the term vocabulary of the collection that consists of hapax legomena. You may want to use the approximation 1/1 + 1/2 + ... + 1/*n* = ln *n*
    3. Do you think that the estimate you get is correct? Why or why not?

    ANS:

    1) 2.56 * 10^18
    
    2) According to zipf's law, frequency of a term is inversely proportional to its rank. Consider the example below:

    |     Term     | Rank | Frequency |
    |--------------|------|-----------|
    |   **the**    |  1   |    189    |
    |   **to**     |  3   |     69    |
    |   **a**      |  5   |     50    |
    |   **is**     |  9   |     29    |
    |   **that**   |  13  |     22    |
    |   **yes**    |  31  |      8    |
    |   **.**      |   .  |      .    |
    |   **.**      |   .  |      .    |
    |   **.**      |   .  |      .    |
    |   **zebra**  |  200 |      1    |

    So now *zebra* is a term in our collection which occurs only once. The constant for this is somewhere between 150 to 300.

    
    3) The estimate we get is not always correct. It depends on various factors. Like the frequency of other terms in the collection, the length of the document, total number of unique terms etc.
