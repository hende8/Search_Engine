from parser_module import Parse
from ranker import Ranker
from indexer import Indexer
import numpy as np


class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        # self.indexer=Indexer

    def relevant_docs_from_posting(self, query_tuple, inverted):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param inverted:
        :param query_tuple:
        :param query: query
        :return: dictionary of relevant documents.
        """
        # posting = utils.load_obj("posting")
        inverted_list_ans = []
        posting = {}
        dict_idf = {}
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
                dic_tweets = Indexer.get_values_in_posting_file_of_dictionary_term(term, str(term[0]).upper())
            else:
                dic_tweets = Indexer.get_values_in_posting_file_of_dictionary_term(term, "nums")

            if len(dic_tweets) == 0: continue
            # Indexer.get_values_in_posting_file_of_dictionary_term(inverted, term ,str(term[0]).upper())
            # posting = indexer.Indexer.get_details_about_term_in_inverted_index(term)
            # try:
            #     inverted_list_ans.append(inverted[term]["pt"])
            # except:
            #     continue
            list_terms = []
            # dic_tweets = json.loads(posting[inverted_list_ans[index]])

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
        # sum_pows_query = 0
        # for values in dict_query.values():
        #     sum_pows_query += values*values
        # dist_query = math.sqrt(sum_pows_query)
        # dict_cossine_tweet ={}
        # index = 0
        # sum_pows_doc = 0
        # for list_values in dict_tweet_tfidf.values():
        #     for values in list_values[0].values():
        #         sum_pows_doc += values * values
        #     dist_doc = math.sqrt(sum_pows_doc)
        #     numpy_array_doc = np.array(list(list_values[0].values()))
        #     multiply_vectors = np.dot(numpy_array_query, numpy_array_doc)
        #     cosine_sim = multiply_vectors / (dist_query*dist_doc)
        #     dict_cossine_tweet[list(dict_tweet_tfidf.keys())[index]] = cosine_sim
        #     index += 1

        index = 0
        dict_inner_product = {}
        for list_values in dict_tweet_tfidf.values():
            numpy_array_doc = np.array(list(list_values[0].values()))
            multiply_vectors = round(np.dot(numpy_array_query, numpy_array_doc),6)
            dict_inner_product[list(dict_tweet_tfidf.keys())[index]] = multiply_vectors
            index += 1
        return dict_inner_product

    def expand_query(self):
        self.ranker.global_method_matrix(self.inverted_index)
