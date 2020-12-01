import os
import pandas as pd
class GlobalMethod:

    def __init__(self,indexer):
        self.indexer=indexer
        index = 0
        path = os.path.dirname(os.path.abspath(__file__)) + '\\inverted_index\\inverted_index_dic.txt"'
        if os.path.exists(path):
            self.execute_global_method_and_generate_matrix(path)

    def execute_global_method_and_generate_matrix(self):
        columns = []
        dic_of_designated_terms ={}
        designate_terms_in_inverted_index={}
        for term in self.indexer.inverted_index.keys():
                dict_of_term = self.indexer.get_details_about_term_in_inverted_index(term=term)
                details_dic_in_inverted_index=self.indexer.get_values_of_dictionary_term(term=term,pointer=dict_of_term['pt'])
                num_of_tweets = len(details_dic_in_inverted_index)
                if num_of_tweets>30:
                    designate_terms_in_inverted_index[term]= dict_of_term
                    columns.append(term)
                    dic_of_designated_terms[term]= {}
                    dic_of_designated_terms[term]= details_dic_in_inverted_index
        df = pd.DataFrame(index=columns, columns=columns)
        for column in columns:
            dic_with_tweet_id_col = dic_of_designated_terms[column]
            temp_list_tweet_id_row = []
            temp_list_tweet_id_col = []
            for row in columns:
                dic_with_tweet_id_row = dic_of_designated_terms[row]
                for tweet in dic_with_tweet_id_row.keys():
                    temp_list_tweet_id_row.append(tweet)
                for tweet in dic_with_tweet_id_col:
                    temp_list_tweet_id_col.append(tweet)
                mutual_list = [value for value in temp_list_tweet_id_row if value in temp_list_tweet_id_col]
                sigma = 0
                for item in mutual_list:
                    sigma += dic_of_designated_terms[column][item]['fr'] * dic_of_designated_terms[row][item]['fr']
                freq_row = designate_terms_in_inverted_index[row]['fr']
                freq_col= designate_terms_in_inverted_index[column]['fr']
                dict_of_term_col = self.indexer.get_details_about_term_in_inverted_index(term=column)
                val = self.calculate_frequency_and_normalize(c_i_j=sigma,
                                                             c_i_i=freq_row,
                                                             c_j_j=freq_col)
                df[row][column] = val
        print(df)

    def calculate_frequency_and_normalize(self, c_i_j, c_i_i, c_j_j):
        down = (c_i_i) + (c_j_j) - c_i_j
        return c_i_j / down



