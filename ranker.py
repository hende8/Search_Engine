import pandas as pd
import collections
from posting_file import PostingFile
class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc):
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

    def global_method_matrix(self, inverted_idx):
        '''
        create matrix of global method ranking to the inverted index
        :param inverted_idx:
        :return:
        '''
        keys = inverted_idx.keys()
        list =[]
        columns= []
        temp_dic = {}
        for key in keys :
            if inverted_idx[key]['frequency_show_term'] > 5:
                temp_dic[key]= {}
                temp_dic[key]['frequency_show_term']= inverted_idx[key]['frequency_show_term']
                temp_dic[key]['posting_pointer']= inverted_idx[key]['posting_pointer']
                list.append(temp_dic)
                columns.append(key)
        columns= sorted(columns)

        df = pd.DataFrame(index=columns, columns=columns)
        a_k=['a','b','c','d','e','f','g','h','i','j','k']
        l_z=['l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        posting_file=PostingFile()
        for column in columns:
            a_k_bool = False
            hash_bool = False
            l_z_bool = False
            letter_lower = column[0].lower()
            if letter_lower in a_k:
                posting_file_col=posting_file.open_posting_file(idx='a_k')
                a_k_bool=True
            elif letter_lower in l_z:
                posting_file_col=posting_file.open_posting_file(idx='l_z')
                l_z_bool=True
            else:
                posting_file_col=posting_file.open_posting_file(idx='hash')
                hash_bool=True
            temp_tweet_id_list_col = posting_file_col[temp_dic[column]['posting_pointer']]
            for row in columns:
                letter_lower = row[0].lower()
                if letter_lower in a_k:
                    if a_k_bool:
                        posting_file_row=posting_file_col
                    else:
                        posting_file_row = posting_file.open_posting_file(idx='a_k')
                elif letter_lower in l_z:
                    if l_z_bool:
                        posting_file_row=posting_file_col
                    else:
                        posting_file_row = posting_file.open_posting_file(idx='l_z')
                else:
                    if hash_bool:
                        posting_file_row = posting_file_col
                    else:
                        posting_file_row = posting_file.open_posting_file(idx='hash')
                temp_tweet_id_list_row = posting_file_row[temp_dic[row]['posting_pointer']]
                temp_list_tweet_id_row = {}
                temp_list_tweet_id_col ={}
                if row == column:
                    df[row][column] = -1
                else:
                    for item in temp_tweet_id_list_row:
                        temp_list_tweet_id_row[item.tweet_id]=int(item.frequency_show_in_document)
                    for item in temp_tweet_id_list_col:
                        temp_list_tweet_id_col[item.tweet_id]=int(item.frequency_show_in_document)
                    mutual_list=[x for x in temp_list_tweet_id_col.keys() if x in temp_list_tweet_id_row.keys()]
                    sigma =0
                    for item in mutual_list:
                        sigma+= temp_list_tweet_id_row[item] * temp_list_tweet_id_col[item]

                    val = self.calculate_frequency_and_normalize(c_i_j = sigma, c_i_i = temp_dic[row]['frequency_show_term'],c_j_j = temp_dic[column]['frequency_show_term'])
                    df[row][column] = val

        print(df)

    def calculate_frequency_and_normalize(self,c_i_j,c_i_i,c_j_j):
        down = (c_i_i*c_i_i)+(c_j_j*c_j_j)-c_i_j
        return c_i_j/down


        print(df)