import tf_idf
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from document import Document
from indexer import Indexer
import indexer
import math
import copy
import pandas as pd


class Ranker:
    def __init__(self):
        pass
        self.docs = []
        self.docs = indexer.get_all_docs()
        dic_tf = {}

    @staticmethod
    def tf_single(relevant_doc_single,all_docs):
        # ddd = relevant_doc["tweet_id"]
        ddd = all_docs[relevant_doc_single]
        print ("ff")
        #return float(self.count(docs)) / len(self)


    @staticmethod
    def rank_relevant_doc(relevant_docs):
        all_docs = indexer.get_all_docs()
        len_docs = range(len(all_docs))
        dict_tf = {}
        dict_idf = {}
        relevant_docs_without_words ={}
        index = 0
        for doc in relevant_docs:
            ################calculate tf
            is_int = isinstance(relevant_docs[doc], int)
            if is_int is True:
                curr_doc = copy.deepcopy(all_docs[doc])
                tf = relevant_docs[doc]/curr_doc.doc_length
                dict_tf[doc] = tf
                relevant_docs_without_words[doc] = relevant_docs[doc]
            else:
                dict_idf[doc] = relevant_docs[doc]

        tfidf = {}
        save_list_word = []
        list_word = []
        for word in dict_idf:
            for term in dict_tf:
                list_word.append(dict_tf[term]*dict_idf[word])

                #list_word.append(dict_idf[i]*)
            tfidf[word] = list_word
            save_list_word.append(word)
            list_word =[]
        df = pd.DataFrame(tfidf)
        #df['tweet_id'] = relevant_docs_without_words
        print(df)
        #df.sum(axis=0)
        #print(df)
        #for word, val in relevant_docs[:2]:
        #    tfidf[word] =
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        return sorted(relevant_doc.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
