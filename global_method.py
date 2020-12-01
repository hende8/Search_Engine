import os
import pandas as pd
class GlobalMethod:

    def __init__(self,indexer):
        self.indexer=indexer
        index = 0
        # path = os.path.dirname(os.path.abspath(__file__)) + '\\inverted_index\\inverted_index_dic.txt"'
        # if os.path.exists(path):
        # dic = indexer.load_inverted_index_to_dictionary_online()
        self.execute_global_method_and_generate_matrix()

    def execute_global_method_and_generate_matrix(self):
        average_freq = int(self.calculate_average_of_frequency()*1.4)
        columns = []
        dic_of_designated_terms ={}
        designate_terms_in_inverted_index={}
        for term in self.indexer.inverted_index.keys():
            num_of_freq = int(self.indexer.inverted_index[term]['tf'])
            if num_of_freq > average_freq:
                dict_of_term = self.indexer.get_details_about_term_in_inverted_index(term=term)
                details_dic_in_inverted_index=self.indexer.get_values_in_posting_file_of_dictionary_term(term=term,pointer=dict_of_term['pt'])
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
                for tweet in dic_with_tweet_id_col.keys():
                    temp_list_tweet_id_col.append(tweet)
                mutual_list = [value for value in temp_list_tweet_id_row if value in temp_list_tweet_id_col]
                sigma = 0
                for item in mutual_list:
                    sigma += dic_of_designated_terms[column][item]['tf'] * dic_of_designated_terms[row][item]['tf']
                freq_row = designate_terms_in_inverted_index[row]['tf']
                freq_col= designate_terms_in_inverted_index[column]['tf']
                dict_of_term_col = self.indexer.get_details_about_term_in_inverted_index(term=column)
                val = self.calculate_frequency_and_normalize(c_i_j=sigma,
                                                             c_i_i=freq_row,
                                                             c_j_j=freq_col)
                df[row][column] = val
        print(df)

    def calculate_frequency_and_normalize(self, c_i_j, c_i_i, c_j_j):
        down = (c_i_i) + (c_j_j) - c_i_j
        return c_i_j / down

    def calculate_average_of_frequency(self):
        keys = self.indexer.inverted_index.keys()
        sum=0
        number_of_terms=len(keys)
        for key in keys :
            sum+=int(self.indexer.inverted_index[key]['tf'])
        return int(sum/number_of_terms)


