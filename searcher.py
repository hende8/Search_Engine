from parser_module import Parse
from ranker import Ranker
import utils
import json
import indexer
import math

class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index

    #def tf_single_doc(self, term, doc_length):
       # return self.inverted_index[word]["frequency_show_term"] / all_words_length

    #def idf(self,word):

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        with open('posting_file_18.json') as json_file:
            posting = json.load(json_file)
        with open('inverted_dic_file_18.json') as json_file:
            inverted = json.load(json_file)
        #posting = utils.load_obj("posting")
        relevant_docs = {}
        inverted_list_ans = []

        index=0
        dict_word_idf = {}
        for term in query:
            #tf = self.tf(term,len(inverted))
            #idf = self.idf()
            len_all_docs = len(indexer.all_docs)
            inverted_list_ans.append(inverted[term]["posting_pointer"])
            dic_tweets = json.loads(posting[inverted_list_ans[index]])
            count_all_exist_file = 0
            for tweet in dic_tweets:
                if tweet["tweet_id"] not in relevant_docs:
                    relevant_docs[tweet["tweet_id"]] = 1
                else:
                    relevant_docs[tweet["tweet_id"]] += 1
                count_all_exist_file += 1
            idf_temporary = math.log10(len_all_docs/len(dic_tweets))
            #dict_word_idf[term] = idf_temporary
            relevant_docs[term] = idf_temporary
            index += 1
        # for term in query:
        #     try: # an example of checks that you have to do
        #         posting_doc = posting[term]
        #         for doc_tuple in posting_doc:
        #             doc = doc_tuple[0]
        #             if doc not in relevant_docs.keys():
        #                 relevant_docs[doc] = 1
        #             else:
        #                 relevant_docs[doc] += 1
        #     except:
        #         print('term {} not found in posting'.format(term))
        return relevant_docs
