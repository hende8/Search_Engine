from parser_module import Parse
from ranker import Ranker
from indexer import Indexer
import numpy as np
from global_method import GlobalMethod


class Searcher:

    def __init__(self, inverted_index,path):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.path=path
        self.global_method=GlobalMethod(inverted_index,path)
        self.global_method.execute_global_method_and_generate_matrix()

    def relevant_docs_from_posting(self, query_tuple, inverted):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param inverted:
        :param query_tuple:
        :param query: query
        :return: dictionary of relevant documents.
        """
        temp_words=list()
        for word in query_tuple[0]:
            words= self.global_method.get_values_to_expand_query(term=word)
            if words!="":
                temp_words.extend(words.split(" "))

        query_tuple[0].extend(temp_words)

        index = 0
        query = []
        dict_tweet_tfidf = {}
        keys ={}
        keys = inverted.keys()
        for term in query_tuple[0]:
            if term in keys: query.append(str(term))
            if term.upper in keys: query.append(str(term.upper))
            if term.lower in keys: query.append(str(term.lower))
        for term in query_tuple[1]:
            if term in keys:  query.append(str(term))
            if term.upper in keys: query.append(str(term.upper))
            if term.lower in keys: query.append(str(term.lower))
        for term in query:
            if term == '' or term == ' ': continue
            curr_word = inverted[term]
            if 'A' <= term[0].upper() <='Z':
                dic_tweets = Indexer.get_values_in_posting_file_of_dictionary_term(term, str(term[0]).upper(),self.path)
            else:
                dic_tweets = Indexer.get_values_in_posting_file_of_dictionary_term(term, "nums",self.path)

            if len(dic_tweets) == 0: continue
            list_terms = []
            for tweet in dic_tweets:
                try:
                    tf_idf = round(float(dic_tweets[tweet]['tfl']) * float(curr_word["idf"]), 6)
                except:
                    continue
                if tweet not in dict_tweet_tfidf:
                    dict_term_tfidf = {}
                    for term_inner in query:
                        dict_term_tfidf[term_inner] = float(0)
                    list_terms.append(dict_term_tfidf)
                    dict_tweet_tfidf[tweet] = list_terms
                    list_terms[0][term] = tf_idf
                    dict_tweet_tfidf[tweet] = list(list_terms)
                else:
                    exist_list = list(dict_tweet_tfidf[tweet])
                    for dict_list in exist_list:
                        dict_list[term] += tf_idf
                list_terms.clear()
            index += 1
            dic_tweets.clear()
        dict_query = {}
        for term in query:
            if term not in dict_query.keys():
                dict_query[term] = 1
            else:
                dict_query[term] += 1

        numpy_array_query = np.array(list(dict_query.values()))
        index = 0
        dict_inner_product = {}
        for list_values in dict_tweet_tfidf.values():
            numpy_array_doc = np.array(list(list_values[0].values()))
            multiply_vectors = round(np.dot(numpy_array_query, numpy_array_doc),6)
            dict_inner_product[list(dict_tweet_tfidf.keys())[index]] = multiply_vectors
            index += 1
        return dict_inner_product

