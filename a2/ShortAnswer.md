1. In `searcher.py`, why do we keep an inverted index instead of simply a list
of document vectors (e.g., dicts)? What is the difference in time and space
complexity between the two approaches?

	ANS:

	First of all inverted index is much more faster than document vector in retrieving data. Retrieval is easier in inverted index because we maintain the index of all the words in the document. In case of document vector, we have to search the entire document vector each time a search is performed.

	Consider a example:

		doc_vec =
		[
			[‘the’, ‘cat’, ‘jumps’, ‘out’],
			[‘the’, ‘dog’, ‘is’, ‘barking’],
			[‘cat’, ‘and’, ‘dog’, ‘are’, ‘fighting’],
			[‘the’, ‘dog’, ‘jumps’, ‘on’, ‘cat’]
		]

	and its inverted index, which is

		index = 
		{
			‘the’      : [0, 1, 3],
			‘cat’      : [0, 2, 3],
			‘jumps’    : [0, 3],
			‘out’      : [0],
			‘dog’      : [1, 2, 3],
			‘is’       : [1],
			‘barking’  : [1],
			‘and’      : [2],
			‘are’      : [2],
			‘fighting’ : [2],
			‘on’       : [3]
		}

	If we use document vector to perform the search on `"cat and dog"` we have to go through the entire document vector.

	But if we use inverted index, which is a dictionary `{word:[doc_id]}` then we can take the intersection of all the words in the query and get the desired output.

	Here the same query can be executed by performing 

		cat ∩ and ∩ dog
		[0, 2, 3] ∩ [2] ∩ [1, 2, 3]
	
	So the result is document with doc_id 2.
	
	Time Complexity to perform search on document vector is `m*n` where `m` is length of the longest document and `n` is the total number of documents.
	
	While Time Complexity to perform search on inverted index is just `1` since it is a dictionary. But the Time Complexity to build the inverted index is `m*n`.
	
	Now, Space Complexity for document vector is `m*n`. But for inverted index it is `k+m*n` where k is number of unique words in the document. In the example above `k` is 11.

2. Consider the query `chinese` with and without using champion lists.  Why is
the top result without champion lists absent from the list that uses champion
lists? How can you alter the algorithm to fix this?

	ANS:
	
	Champion List is a list with higher tf-idf values. Only the first few documents with highest tf-idf values are considered.
	
	When we search the word `chinese` using champion list, top ten documents with highest tf-idf is considered and then the cosine scores for the documents are calculated using  vector query.
	
	But when we dont use champion list, all the cosine scores of the documents are computed. And documents with top ten highest cosine scores are displayed.
	
	Alteration in the algorithm:
	
	* Do not consider the document length (i.e. doc_lengths) in the `search_by_cosine()` method.
	
	* i.e. Remove the below two lines from `search_by_cosine()` method:
		
	        for doc_id in tempDict.keys():
    	        tempDict[doc_id] /= float(doc_lengths[doc_id])
	            
	Removing this lines will fix the algorithm.

3. Describe in detail the data structures you would use to implement the
Cluster Pruning approach, as well as how you would use them at query time.

	ANS:
	
	The data structure for Cluster Pruning Approach:
	
	I would use a dictionary to map doc_id of the leader (doc_id_leader) to the list of doc_ids of the followers ([doc_id_followers]) in the cluster.
	
		{doc_id_leader:[doc_id_followers]}
		
	
	Example of the data structure for Cluster Pruning Approach:
	
		clusterPruning = {3 : [10, 14, 19, 21], 5 : [0, 4, 8, 20], 15 : [2, 6, 11, 24], 17 : [7, 9, 12, 18], 22 : [1, 13, 16, 23]}
		
	Here {3, 10, 14, 19, 21} is one of the cluster.
		
	At query time:

	* Compute cosine similarity from the query to each of the leader (clusterPruning.keys()).
	* Now the canditate set will contain the leader with the most cosine similarity to the query and its followers.

			candidate = clusterPruning[leader]	#doc_ids_followers
			candidate.append(leader)			#doc_id_leader
			candidate = set(candidate)
												#'leader' is the selected leader
	* Compute the cosine scores of all the documents in the candidate set.