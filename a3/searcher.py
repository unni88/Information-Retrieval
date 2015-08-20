"""
    ASSIGNMENT 3
"""

from collections import defaultdict
import codecs
import math
import re

import numpy as np
from pylab import *
import matplotlib.pyplot as plt


class Index(object):

    def __init__(self, document_filename=None, query_filename=None, relevant_filename=None):
        self.documents = self.readDocuments(self.read_lines(document_filename))                                                           #   List of Documents
        self.querys = self.readQuery(self.read_lines(query_filename))                                                                     #   List of Querys
        self.relevant_documents = self.readRelevantDocuments(self.read_lines(relevant_filename))                                          #   List of Relevant Documents
        self.stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]                                                         #   Stemmed Documents
        self.relevant_documents_dict = self.makeRelevantDocumentDictionary([self.tokenize(d) for d in self.relevant_documents])           #   Dictionary of Relevant Documents
        self.doc_freqs = self.count_doc_frequencies(self.stemmed_docs)
        self.index = self.create_tfidf_index(self.stemmed_docs, self.doc_freqs)
        self.doc_lengths = self.compute_doc_lengths(self.index)
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.map = 0

    def compute_doc_lengths(self, index):
        tempDict = defaultdict(int)
        for listOfList in index.values():
            for list in listOfList:
                tempDict[list[0]] += list[1]**2
        for doc_id, sum in tempDict.items():
            tempDict[doc_id] =  float(math.sqrt(sum))

        return dict(tempDict)

    def create_tfidf_index(self, docs, doc_freqs):
        tempDict = defaultdict(list)
        for line in docs:
            tempLine = list(set(line))
            for word in tempLine:
                innerList = []
                outerList = []
                temp = (1 + math.log10(float(line.count(word)))) * (math.log10(float(len(docs))/float(doc_freqs[word])))
                innerList.append(docs.index(line))
                innerList.append(temp)
                outerList.append(innerList)
                tempDict[word] += outerList
            
        return dict(tempDict)

    def count_doc_frequencies(self, docs):
        frequency = defaultdict(int)
        for line in docs:
            line = list(set(line))
            for word in line:
                frequency[word] += 1
        return dict(frequency)

    def query_to_vector(self, query_terms):
        tempDict = defaultdict(int)
        for word in query_terms:
            if word in self.doc_freqs.keys():
                temp = math.log10(float(len(self.documents))/float(self.doc_freqs[word]))
                tempDict[word] = temp
        return dict(tempDict)

    def search_by_cosine(self, query_vector, index, doc_lengths):
        tempDict = defaultdict(int)
        for word in query_vector.keys():
            for list in index[word]:
                tempDict[list[0]] += query_vector[word] * list[1]
    
        for doc_id in tempDict.keys():
            tempDict[doc_id] /=  float(doc_lengths[doc_id])
        
        tempDict = dict(tempDict)
        tempDict = sorted(tempDict.items(), key = lambda key: key[1], reverse = True)
        return tempDict

    def retrieval_status_value(self, query_terms):
        tempDict = defaultdict(int)
        temp = 0
        for doc_id in range(0, len(self.stemmed_docs)):
            for word in query_terms:
                if word in self.stemmed_docs[doc_id]:
                    temp += math.log10(float(len(self.stemmed_docs))/float(self.doc_freqs[word]))
            tempDict[doc_id + 1] = temp
            temp = 0

        tempDict = dict(tempDict)
        tempDict = sorted(tempDict.items(), key = lambda key: key[1], reverse = True)
        return tempDict
            

    def bm25(self, query_terms, k, b):
        tempDict = defaultdict(int)
        temp = 0
        for doc_id in range(0, len(self.stemmed_docs)):
            for word in query_terms:
                if word in self.stemmed_docs[doc_id]:
                    temp += (math.log10(float(len(self.stemmed_docs))/float(self.doc_freqs[word])) * (float((k + 1) * self.stemmed_docs[doc_id].count(word)) / float((b * k) + self.stemmed_docs[doc_id].count(word))))
            tempDict[doc_id + 1] = temp
            temp = 0
        
        tempDict = dict(tempDict)
        tempDict = sorted(tempDict.items(), key = lambda key: key[1], reverse = True)
        return tempDict

    def compute_evaluation_metrics_for_sbc(self):
        # for Cosine Similarity
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.map = 0

        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for query_no in range(0, len(self.querys)):
            tokens = self.tokenize(self.querys[query_no])
            stem = self.stem(tokens)
            vector = self.query_to_vector(stem)
            
            result_of_sbc = self.search_by_cosine(vector, self.index, self.doc_lengths)
            tp = 0
            fp = 0
            fn = 0
            for doc_id, value in result_of_sbc[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    tp += 1
                else:
                    fp += 1
                fn = len(self.relevant_documents_dict[query_no + 1]) - tp

            if tp + fp is not 0:
                self.precision += (float(tp) / float(tp+fp))
            if tp + fn is not 0:
                self.recall += (float(tp) / float(tp+fn))
            for doc_id, value in result_of_sbc[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    self.map += (float(tp) / float(tp+fp))
                    
        if self.precision + self.recall is not 0:
            self.f1 = float(2 * self.precision * self.recall) / float(self.precision + self.recall)

        self.precision = (self.precision * 100) / len(self.querys)
        self.recall = (self.recall * 100) / len(self.querys)
        self.f1 = (self.f1 * 100) / len(self.querys)
        self.map = (self.map * 100) / len(self.querys)
        print '|      Cosine      |  ', self.precision,'%   |  ', self.recall,'%  |  ', self.f1,'%  |  ', self.map,'%  |'
        print '--------------------------------------------------------------------------------------------------------'
        return

    def compute_evaluation_metrics_for_rsv(self):
        # for RSV
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.map = 0
        
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for query_no in range(0, len(self.querys)):
            tokens = self.tokenize(self.querys[query_no])
            stem = self.stem(tokens)
            vector = self.query_to_vector(stem)
            
            result_of_rsv = self.retrieval_status_value(stem)
            tp = 0
            fp = 0
            fn = 0
            for doc_id, value in result_of_rsv[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    tp += 1
                else:
                    fp += 1
                fn = len(self.relevant_documents_dict[query_no + 1]) - tp
            
            if tp + fp is not 0:
                self.precision += (float(tp) / float(tp+fp))
            if tp + fn is not 0:
                self.recall += (float(tp) / float(tp+fn))
            for doc_id, value in result_of_rsv[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    self.map += (float(tp) / float(tp+fp))

        if (self.precision + self.recall) is not 0:
            self.f1 = float(2 * self.precision * self.recall) / float(self.precision + self.recall)
        self.precision = (self.precision * 100) / len(self.querys)
        self.recall = (self.recall * 100) / len(self.querys)
        self.f1 = (self.f1 * 100) / len(self.querys)
        self.map = (self.map * 100) / len(self.querys)
        print '|       RSV        |  ', self.precision,'%   |  ', self.recall,'%  |  ', self.f1,'%  |  ', self.map,'%  |'
        print '--------------------------------------------------------------------------------------------------------'
        return
        
    def compute_evaluation_metrics_for_bm25(self, k, b):
        # for BM25
        self.precision = 0
        self.recall = 0
        self.f1 = 0
        self.map = 0
        
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for query_no in range(0, len(self.querys)):
            tokens = self.tokenize(self.querys[query_no])
            stem = self.stem(tokens)
            vector = self.query_to_vector(stem)
            
            result_of_bm25 = self.bm25(stem, k, b)
            tp = 0
            fp = 0
            fn = 0
            for doc_id, value in result_of_bm25[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    tp += 1
                else:
                    fp += 1
                fn = len(self.relevant_documents_dict[query_no + 1]) - tp
            
            if tp + fp is not 0:
                self.precision += (float(tp) / float(tp+fp))
            if tp + fn is not 0:
                self.recall += (float(tp) / float(tp+fn))
            for doc_id, value in result_of_bm25[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    self.map += (float(tp) / float(tp+fp))
        if self.precision + self.recall is not 0:
            self.f1 = float(2 * self.precision * self.recall) / float(self.precision + self.recall)
        self.precision = (self.precision * 100) / len(self.querys)
        self.recall = (self.recall * 100) / len(self.querys)
        self.f1 = (self.f1 * 100) / len(self.querys)
        self.map = (self.map * 100) / len(self.querys)
        print '| BM25 (', k, ',', b, ') |  ', self.precision,'%   |  ', self.recall,'%  |  ', self.f1,'%  |  ', self.map,'%  |'
        print '--------------------------------------------------------------------------------------------------------'
        return

    def precision_recall_curve(self):
        # incomplete method and incorrect result
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        precision_vector = []
        recall_vector = []
        xlabel('recall')
        ylabel('precision')
        
        for query_no in range(0, len(self.querys)):
            tokens = self.tokenize(self.querys[query_no])
            stem = self.stem(tokens)
            vector = self.query_to_vector(stem)
            
            result_of_rsv = self.retrieval_status_value(stem)
            tp = 0
            fp = 0
            fn = 0
            for doc_id, value in result_of_rsv[:20]:
                if str(doc_id + 1) in self.relevant_documents_dict[query_no + 1]:
                    tp += 1
                else:
                    fp += 1
                fn = len(self.relevant_documents_dict[query_no + 1]) - tp
            
            if tp + fp is not 0:
                self.precision = (float(tp) / float(tp+fp))
            if tp + fn is not 0:
                self.recall = (float(tp) / float(tp+fn))
            plot((self.recall * 100), (self.precision * 100), 'bo')
    
        xlim((0, 100))
        ylim((0, 100))

        plt.show()
        return

    def read_lines(self, filename):
        return [l.strip() for l in codecs.open(filename, 'rt', 'utf-8').readlines()]
    
    def readDocuments(self, document):
        outerList = []
        tempString = ''
        for lineNo in range(0, len(document)):
            if '*TEXT' in document[lineNo] or '*STOP' in document[lineNo]:
                if tempString is not '':
                    outerList.append(tempString)
                tempString = ''
            else:
                tempString = tempString + ' ' + document[lineNo]
        return outerList

    def tokenize(self, document):
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

    def stem(self, tokens):
        return [re.sub('^(did|does)$', 'do', t) for t in tokens]

    def readQuery(self, document):
        outerList = []
        tempString = ''
        for lineNo in range(1, len(document)):
            if '*FIND' in document[lineNo] or '*STOP' in document[lineNo]:
                outerList.append(tempString)
                tempString = ''
            else:
                tempString = tempString + ' ' + document[lineNo]
        return outerList

    def readRelevantDocuments(self, document):
        outerList = []
        for lineNo in range(0, len(document)):
            if len(document[lineNo]) is not 0:
                outerList.append(document[lineNo])
        return outerList

    def makeRelevantDocumentDictionary(self, relevant_document):
        tempDict = defaultdict(list)
        for rel_doc in relevant_document:
            rel_doc_id = rel_doc[0]
            rel_doc.pop(0)
            tempDict[int(rel_doc_id)] = rel_doc
        
        tempDict = dict(tempDict)
        return tempDict

def main():
    indexer = Index('time/TIME.ALL', 'time/TIME.QUE', 'time/TIME.REL')
    
    print '\n\n--------------------------------------------------------------------------------------------------------'
    print '|      System      |      Precision      |       Recall       |         F1         |        MAP        |'
    print '--------------------------------------------------------------------------------------------------------'
    
    # for Cosine Similarity
    indexer.compute_evaluation_metrics_for_sbc()
    
    # for RSV
    indexer.compute_evaluation_metrics_for_rsv()

    # for BM25
    for k in [1, 2]:
        for b in [0.5, 1]:
            indexer.compute_evaluation_metrics_for_bm25(k, b)

    indexer.precision_recall_curve()

if __name__ == '__main__':
    main()
