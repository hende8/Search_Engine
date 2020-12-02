import os
import pandas as pd
import json
from collections import Counter
from indexer import Indexer

class GlobalMethod:

    def __init__(self,indexer):
        self.inverted_index=indexer
        index = 0
        # path = os.path.dirname(os.path.abspath(__file__)) + '\\inverted_index\\inverted_index_dic.txt"'
        # if os.path.exists(path):
        # dic = indexer.load_inverted_index_to_dictionary_online()
        self.matrix=pd.DataFrame()
        self.execute_global_method_and_generate_matrix()
        self.load_json_to_df()

    def execute_global_method_and_generate_matrix(self):
        average_freq = int(self.calculate_average_of_frequency()*500)
        columns = []
        dic_of_designated_terms ={}
        designate_terms_in_inverted_index={}
        for term in self.inverted_index.keys():
            num_of_freq = int(self.inverted_index[term]['tf'])
            if num_of_freq > average_freq:
                dict_of_term = Indexer.get_details_about_term_in_inverted_index(term=term,inverted_index=self.inverted_index)
                details_dic_in_inverted_index=Indexer.get_values_in_posting_file_of_dictionary_term(term=term,pointer=dict_of_term['pt'])
                columns.append(term)
                dic_of_designated_terms[term]= {}
                dic_of_designated_terms[term]= details_dic_in_inverted_index
        df = pd.DataFrame(index=columns, columns=columns)
        for column in columns:
            for row in columns:
                df[row][column]=-1
        for column in columns:
            dic_with_tweet_id_col = dic_of_designated_terms[column]
            temp_list_tweet_id_row = []
            for row in columns:
                if df[row][column]!=-1:continue
                dic_with_tweet_id_row = dic_of_designated_terms[row]
                dic_temp ={}
                keys_1=dic_with_tweet_id_row.keys()
                keys_2=dic_with_tweet_id_col.keys()
                mutual_list=[]
                for tweet in keys_1:
                    temp_list_tweet_id_row.append(tweet)
                    dic_temp[tweet]=1
                keys_dic_temp = dic_temp.keys()
                for tweet in keys_2:
                    if tweet in keys_dic_temp:
                        mutual_list.append(tweet)
                temp_list_tweet_id_row.clear()
                temp_list_tweet_id_row=list()
                sigma = 0
                for item in mutual_list:
                    item = str(item)
                    column = str(column)
                    row = str(row)
                    try:
                        sigma += int(dic_of_designated_terms[row][item]['tf']) * int(dic_of_designated_terms[column][item]['tf'])
                    except:
                        print("error")
                        continue
                freq_row = int(self.indexer.inverted_index[row]['tf'])**2
                freq_col= int(self.indexer.inverted_index[column]['tf'])**2
                val = self.calculate_frequency_and_normalize(c_i_j=int(sigma),
                                                             c_i_i=int(freq_row),
                                                             c_j_j=int(freq_col))
                df[row][column] = val
                df[column][row] = val
        df.to_json('Global_method_matrix.json')


    def calculate_frequency_and_normalize(self, c_i_j, c_i_i, c_j_j):
        down = (c_i_i) + (c_j_j) - c_i_j
        return c_i_j / down

    def calculate_average_of_frequency(self):
        keys = self.inverted_index.keys()
        sum=0
        number_of_terms=len(keys)
        for key in keys :
            sum+=int(self.inverted_index[key]['tf'])
        return int(sum/number_of_terms)
    def load_json_to_df(self):
        path = os.path.dirname(os.path.abspath(__file__))
        file =path+'\\Global_method_matrix.json'
        with open(file) as train_file:
            data = json.load(train_file)
            self.matrix = pd.DataFrame.from_dict(data, orient='columns')
        return self.matrix

    def get_values_to_expand_query(self,term):
        dic={}
        for column in self.matrix.columns:
            if term==column:
                for row in column:
                    dic[row]=self.matrix[column][row]
            c = Counter(dic)
            return c.most_common(3)
        return None

