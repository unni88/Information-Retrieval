"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter, defaultdict
import io
import math

import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        Each iteration consists of calls to compute_means and compute_clusters.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector)
        See Log.txt for expected output.
        """
        
        self.meanDocuments = documents[0:self.k]
        self.documents = documents
        
        self.meanVector = []
        
        for doc in self.meanDocuments:
            self.meanVector.append(float(np.dot(doc.values(), doc.values())))


        for i in range(0, iters):
            self.clusters = defaultdict(list)
            print self.compute_clusters(documents)
            self.meanDocuments = self.compute_means()
            print self.error(documents)
        
        self.clusters = defaultdict(list)
        self.compute_clusters(documents)

        return
        pass

    def compute_means(self):
        """ Compute the mean vectors for each cluster (storing the results in an
        instance variable)."""

        self.meanVector = []
        
        for doc in self.meanDocuments:
            self.meanVector.append(float(np.dot(doc.values(), doc.values())))
        
        for clusterID, list in self.clusters.items():
            tempCounter = Counter()
            for docID, dist in list:
                tempCounter.update(self.documents[docID])
            for key, value in tempCounter.items():
                tempCounter[key] = float(value) / float(len(list))
            self.meanDocuments[clusterID] = tempCounter
        return self.meanDocuments
        pass

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable). """
        
        for docID in range(0, len(documents)):
            distance = []
            for clusterID in range(0, self.k):
                distance.append((docID, self.distance(documents[docID], self.meanDocuments[clusterID], self.meanVector[clusterID])))
            minDistance = min(distance, key = lambda t: t[1])
            self.clusters[distance.index(minDistance)].append(minDistance)

        result = []
        for clusterID in self.clusters.keys():
            result.append(len(self.clusters[clusterID]))

        return result
        pass


    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
    
        A = mean_norm
        B = float(sum([doc.values()[i]**2 for i in range(0, len(doc.values()))]))
        AB = 0.0
        for key in doc.keys():
            if key in mean:
                AB += mean[key] * doc[key]

        return float(math.sqrt(A + B - 2.0 * AB))

    def error(self, documents):
        """ Return the error of the current clustering, defined as the sum of the
        Euclidean distances between each document and its assigned mean vector."""
        
        error = 0.0
        
        self.meanVector = []
        
        for doc in self.meanDocuments:
            self.meanVector.append(float(np.dot(doc.values(), doc.values())))

        for clusterID, list in self.clusters.items():
            for docID, dist in list:
                error += self.distance(documents[docID], self.meanDocuments[clusterID], self.meanVector[clusterID])

        return error
        pass

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster, sorted by distance to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (which will be out of order from the original
        document).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        
        for clusterID, list in self.clusters.items():
            list =  sorted(list, key=lambda x: x[1], reverse=False)
            print 'CLUSTER ' + str(clusterID)
            if len(list) > n:
                iter = n
            else:
                iter = len(list)
            i = 0
            while i < iter:
                if len(self.documents[list[i][0]]) > 3:
                    print ' '.join([k for k in self.documents[list[i][0]]])     #[unicode(k).encode('utf8') for k in self.documents[list[i][0]]]
                else:
                    iter += 1
                i += 1

        return
        pass


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    
    result = []
    countTerm = Counter()
    
    for doc in docs:
        for term, value in doc.items():
            countTerm[term] += 1
    
    for doc in docs:
        for key in doc.keys():
            if countTerm[key] < min_df:
                del doc[key]
        if len(doc) > 0:
            result.append(Counter(doc))

    return result
    pass


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with io.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles

def main():
    """ DO NOT MODIFY. """
    profiles = read_profiles('profiles.txt')
    print 'read', len(profiles), 'profiles.'
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
