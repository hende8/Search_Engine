from parser_module import Parse
from ranker import Ranker
import utils
import json
import indexer
import math
import pandas as pd
import numpy as np
import copy
import os


class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index

    # #def relevant_docs_from_posting_old(self, query_tuple):
    #     """
    #     This function loads the posting list and count the amount of relevant documents per term.
    #     :param query: query
    #     :return: dictionary of relevant documents.
    #     """
    #     # with open('posting_file_18.json') as json_file:
    #     #     posting = json.load(json_file)
    #     # with open('inverted_dic_file_2.json') as json_file:
    #     #     inverted = json.load(json_file)
    #     # posting = utils.load_obj("posting")
    #     inverted = self.inverted_index
    #     inverted_list_ans = []
    #     dict_tf = {}
    #     dict_idf = {}
    #     index = 0
    #     query = []
    #     for term in query_tuple[0]:
    #         if str(term) not in query: query.append(term)
    #         if str(term).lower() not in query: query.append(str(term).lower())
    #         if str(term).upper() not in query: query.append(str(term).upper())
    #     for term in query_tuple[1]:
    #         if str(term) not in query: query.append(term)
    #         if str(term).lower() not in query: query.append(str(term).lower())
    #         if str(term).upper() not in query: query.append(str(term).upper())
    #     if str(query).lstrip() == "" or str(query).lstrip() == '': return None
    #     dic_info_term ={}
    #     for term in query:
    #         if term == '' or term == ' ': continue
    #         first_letter = term[0]
    #         dic_info_term = indexer.Indexer.get_details_about_term_in_inverted_index(term)
    #         if 'a' <= first_letter <= 'k' or 'A' <= first_letter <= 'K':
    #             with open('posting_file_a_k.json') as json_file:
    #                 posting = json.load(json_file)
    #         elif 'l' <= first_letter <= 'z' or 'L' <= first_letter <= 'Z':
    #             with open('posting_file_l_z.json') as json_file:
    #                 posting = json.load(json_file)
    #         else:
    #             with open('posting_file_hash.json') as json_file:
    #                 posting = json.load(json_file)
    #         try:
    #             inverted_list_ans.append(inverted[term]["posting_pointer"])
    #             dict_idf[term] = float(inverted[term]["idf"])
    #         except:
    #             continue
    #         dic_tweets = json.loads(posting[inverted_list_ans[index]])
    #         for tweet in dic_tweets:
    #             if tweet["tweet_id"] in dict_tf:
    #                 dict_tf[tweet["tweet_id"]] += float(tweet["tf"])
    #             else:
    #                 dict_tf[tweet["tweet_id"]] = float(tweet["tf"])
    #         index += 1
    #     dict_tfidf = {}
    #     previus_tfidf = 0
    #     for term in dict_tf:
    #         for word in dict_idf:
    #             value_tf = float(dict_tf[term])
    #             value_idf = float(dict_idf[word])
    #             multiply = float(value_idf * value_tf)
    #             dict_tfidf[term] = float(multiply) + previus_tfidf
    #             previus_tfidf = float(multiply)
    #         previus_tfidf = 0
    #     if term.lstrip() == '' or term.lstrip() == ' ': return None
    #     return dict_tfidf

    def relevant_docs_from_posting(self, query_tuple, inverted):
        """
        This function loads the posting list and count the amount of relevant documents per term.
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
        for term in query_tuple[0]:
            if str(term) not in query: query.append(term)
            if str(term).lower() not in query: query.append(str(term).lower())
            if str(term).upper() not in query: query.append(str(term).upper())
        for term in query_tuple[1]:
            if str(term) not in query: query.append(term)
            if str(term).lower() not in query: query.append(str(term).lower())
            if str(term).upper() not in query: query.append(str(term).upper())
        for term in query:
            if term == '' or term == ' ': continue
            dic_tweets = indexer.Indexer.get_values_of_dictionary_term(term,term[0])
            #posting = indexer.Indexer.get_details_about_term_in_inverted_index(term)
            # try:
            #     inverted_list_ans.append(inverted[term]["pt"])
            # except:
            #     continue
            list_terms = []
            #dic_tweets = json.loads(posting[inverted_list_ans[index]])
            for tweet in dic_tweets:
                tf_idf = float(tweet["tf"]) * float(inverted[term]["idf"])
                if tweet["tweet_id"] not in dict_tweet_tfidf:
                    dict_term_tfidf = {}
                    for term_inner in query:
                        dict_term_tfidf[term_inner] = float(0)
                    list_terms.append(dict_term_tfidf)
                    dict_tweet_tfidf[tweet["tweet_id"]] = list_terms
                    list_terms[0][term] = tf_idf
                    dict_tweet_tfidf[tweet["tweet_id"]] = list(list_terms)
                else:
                    exist_list = list(dict_tweet_tfidf[tweet["tweet_id"]])
                    for dict_list in exist_list:
                        dict_list[term] += tf_idf
                list_terms.clear()
            index += 1
        dict_query = {}
        for term in query:
            if term not in dict_query.keys(): dict_query[term] = 1
            else: dict_query[term] += 1

        numpy_array_query = np.array(list(dict_query.values()))
        sum_pows_query = 0
        for values in dict_query.values():
            sum_pows_query += values*values
        dist_query = math.sqrt(sum_pows_query)
        dict_cossine_tweet ={}
        index = 0
        sum_pows_doc = 0
        for list_values in dict_tweet_tfidf.values():
            for values in list_values[0].values():
                sum_pows_doc += values * values
            dist_doc = math.sqrt(sum_pows_doc)
            numpy_array_doc = np.array(list(list_values[0].values()))
            multiply_vectors = np.dot(numpy_array_query, numpy_array_doc)
            cosine_sim = multiply_vectors / (dist_query*dist_doc)
            dict_cossine_tweet[list(dict_tweet_tfidf.keys())[index]] = cosine_sim
            index += 1
        return dict_cossine_tweet

    def expand_query(self):
        self.ranker.global_method_matrix(self.inverted_index)
