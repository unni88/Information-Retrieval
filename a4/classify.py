"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

from collections import defaultdict
from collections import Counter

import math
import glob


class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
    prior = defaultdict(float)
    condProb = defaultdict(defaultdict)
    uniqueTerms = set()
    classLabels = ['ham', 'spam']

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        """
        
        #[START]
        
        #2
        noOfTotalDocs = len(documents)
        
        #1
        for docID in range(0, noOfTotalDocs):
            for term in documents[docID].tokens:
                self.uniqueTerms.add(term)
        self.uniqueTerms = list(self.uniqueTerms)
    
        #3
        for classOfDoc in self.classLabels:
            
            listOfClassTerms = []
            Tct = Counter()
            prob = defaultdict(float)
            total = 0
            
            #4
            noOfClassDocs = len([1 for docID in range(0, noOfTotalDocs) if documents[docID].label is classOfDoc])
            
            #5
            self.prior[classOfDoc] = float(noOfClassDocs) / float(noOfTotalDocs)
        
            #6
            for docID in range(0, noOfTotalDocs):
                if documents[docID].label is classOfDoc:
                    for term in documents[docID].tokens:
                        listOfClassTerms.append(term);
        
            #7
            for term in listOfClassTerms:
                
                #8
                Tct[term] += 1
        
            for term in self.uniqueTerms:
                total += (Tct[term] + 1)
            
            #9
            for term in self.uniqueTerms:
            
                #10
                prob[term] = float(Tct[term] + 1) / float(total)
            
            self.condProb[classOfDoc] = prob
                
        #11
        #Instead of return,
        #prior, uniqueTerms, condProb
        #are stored as instance variables.
        
        #[END]
        return
        
        pass

    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
        
        testDocScore = defaultdict(defaultdict)
        listOfTestDocsClass = []
        
        #[START]
        
        #2
        for classOfDoc in self.classLabels:
            
            score = defaultdict(float)
            
            for docID in range(0, len(documents)):
            
                #3
                score[docID] = math.log10(self.prior[classOfDoc])
            
                #4
                for term in documents[docID].tokens:
                
                    if self.condProb[classOfDoc][term] > 0:
                        
                        #5
                        score[docID] += math.log10(self.condProb[classOfDoc][term])
    
            testDocScore[classOfDoc] = score
    
        for docID in range(0, len(documents)):
            tempList = []
            for classOfDoc in self.classLabels:
                tempList.append(testDocScore[classOfDoc][docID])
            listOfTestDocsClass.append(self.classLabels[tempList.index(max(tempList))])
        
        #6
        return listOfTestDocsClass
        
        #[END]
        
        pass


def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.

    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham

    See the provided log file for the expected output.

    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """

    falseSpam = 0
    missedSpam = 0

    for docID in range(0, len(documents)):
        if documents[docID].label is not 'spam' and predictions[docID] is 'spam':
            falseSpam += 1
        elif documents[docID].label is 'spam' and predictions[docID] is not 'spam':
            missedSpam += 1

    accuracy = float((len(documents) - (falseSpam + missedSpam))) / float(len(documents))

    print 'accuracy={0}, {1} false spam, {2} missed spam'.format(accuracy, falseSpam, missedSpam)

    return


def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'

    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)


if __name__ == '__main__':
    main()
