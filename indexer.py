from collections import OrderedDict
from posting_file import PostingFile
from posting_node import PostingNode
import json
import re
import os

class Indexer:

    def __init__(self, config):
        '''

        :param config: configuration file
        '''
        self.inverted_idx = {}
        self.config = config
        self.posting_file = PostingFile()
        self.sub_dic_posting_file_idx=0
        self.dic_max_tf_and_uniqueness ={}
    def new_sub_dict(self):
        self.inverted_idx={}
        self.posting_file=PostingFile()
        self.sub_dic_posting_file_idx+=1

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        max_tf=0
        # Go over each term in the doc
        for term in document_dictionary.keys():
            tf = document_dictionary[term]
            if tf>max_tf:
                max_tf= tf
            keys = self.inverted_idx.keys()
            try:
                if term[0].isupper():
                    term_upper = term.upper()
                    term_lower=term_upper.lower()
                    # in case of new term in the dictionary - capital or lower it doesnt matter
                    if term_upper not in keys  and term_lower not in keys:
                        self.inverted_idx[term_upper] = {}
                        self.inverted_idx[term_upper]['frequency_show_term'] = 1
                        new_pointer = self.posting_file.add_term_to_posting_file(tweet_id=document.tweet_id,freq_in_tweet=document_dictionary[term])
                        self.inverted_idx[term_upper]['posting_pointer'] = new_pointer
                        continue
                    #in case of capital letter already exists in the dictionary
                    elif term_upper in  keys and term_lower not in keys:
                        self.inverted_idx[term_upper]['frequency_show_term']+=1
                        self.posting_file.add_term_to_posting_file(tweet_id=document.tweet_id,
                                                                   freq_in_tweet=document_dictionary[term],posting_id=self.inverted_idx[term_upper]['posting_pointer'])
                        #in case of word with capital letter fit to word with lower case
                    elif term_lower in keys:
                        self.inverted_idx[term_lower]['frequency_show_term'] +=1
                        self.posting_file.add_term_to_posting_file(tweet_id=document.tweet_id,
                                                                   freq_in_tweet=document_dictionary[term],posting_id=self.inverted_idx[term_lower]['posting_pointer'])
                else:
                    term_upper= term.upper()
                    # in case of word that already exists in dictionary
                    if term_upper  in keys and not term_upper.isnumeric() :
                        temp_freq = self.inverted_idx[term_upper]['frequency_show_term']
                        temp_pointer = self.inverted_idx[term_upper]['posting_pointer']
                        self.inverted_idx[term] = {}
                        self.inverted_idx[term]['frequency_show_term'] = temp_freq + 1
                        new_pointer = self.posting_file.add_term_to_posting_file(document.tweet_id,document_dictionary[term],temp_pointer)
                        self.inverted_idx[term]['posting_pointer']=new_pointer
                        del self.inverted_idx[term_upper]  ## consume a lot of resource - check it
                    # in case of new term in dictionary
                    elif term not in keys:
                        self.inverted_idx[term]={}
                        self.inverted_idx[term]['frequency_show_term']=1
                        new_pointer=self.posting_file.add_term_to_posting_file(document.tweet_id,document_dictionary[term])
                        self.inverted_idx[term]['posting_pointer']=new_pointer
                        continue
                    # in case of new term that join to exist term in dictionary
                    elif term in keys:
                        self.inverted_idx[term]['frequency_show_term']+=1
                        self.posting_file.add_term_to_posting_file(document.tweet_id,document_dictionary[term],
                                                                   self.inverted_idx[term]['posting_pointer'])

            except:
                print(term)
                print(document.tweet_id)
                print(document.term_doc_dictionary)
                print('problem with the following key {}'.format(term[0]))
                print("#####################################")
        self.dic_max_tf_and_uniqueness[str(document.tweet_id)]={}
        self.dic_max_tf_and_uniqueness[str(document.tweet_id)]['max_tf']=max_tf
        self.dic_max_tf_and_uniqueness[str(document.tweet_id)]['uniqueness_words']=len(document_dictionary)
    def write_to_disk_dic_max_tf_and_uniqueness(self):
        '''
        write dictionary max tf and number of uniqueness word in document
        :return:
        '''
        j = json.dumps(self.dic_max_tf_and_uniqueness)
        with open('dic_max_tf_and_uniqueness.json','w') as f:
            f.write(j)
            f.close()
    def open_dic_max_tf_and_uniqueness(self):
        '''
        get max_tf and uniqueness dictionary from json to dictionary
        :return:
        '''
        with open('dic_max_tf_and_uniqueness.json') as json_file:
            data = json.load(json_file)
            return data
    def divide_dictionary(self, documents_list_after_parse,idx=None):
        '''
        divide the dictionary to multiple smaller dictionaries
        :param documents_list_after_parse: dictionary
        :param idx:
        :return:
        '''
        if idx is None:
            idx= len(documents_list_after_parse)
        dic_index=0
        sub_dic_idx = 0
        index = 0
        limit = int(idx / 10)
        limit_extra = idx - limit * 10
        len_parsed_documents = len(documents_list_after_parse)
        while dic_index < 10:
            while sub_dic_idx < limit and index < len_parsed_documents:
                self.add_new_doc(documents_list_after_parse[index])
                sub_dic_idx += 1
                index += 1
                if dic_index == 9:
                    limit = limit + limit_extra
            self.sort_dictionary_by_key(self.inverted_idx)
            self.posting_file.sort_posting_file()
            self.write_to_disk(self.sub_dic_posting_file_idx)
            self.new_sub_dict()
            dic_index += 1
            sub_dic_idx = 0
        self.write_to_disk_dic_max_tf_and_uniqueness()
        # ans = self.open_dic_max_tf_and_uniqueness()
    def sort_dictionary_by_key(self,dictionary):
        '''
        sort dictionary by key
        :param dictionary: dictionary to sort
        :return: sorted dictionary
        '''
        self.inverted_idx= OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
        return self.inverted_idx
    def write_to_disk(self,idx, posting_file=None,inverted_idx=None):
        '''
        write posting file and inverted index to disk
        :param idx: offset of the dictionary
        :param posting_file:
        :param inverted_idx:
        '''
        if inverted_idx is not None:
            j=json.dumps(inverted_idx)
        else:
            j =json.dumps(self.inverted_idx)
        with open('inverted_dic_file_'+str(idx)+'.json','w') as f:
            f.write(j)
            f.close()
        # j =json.dumps(self.posting_file.posting_file_to_json())
        if posting_file is not None:
            j = json.dumps(posting_file.posting_file_to_json())
        else:
            j = json.dumps(self.posting_file.posting_file_to_json())

        with open('posting_file_'+str(idx)+'.json','w') as f:
            f.write(j)
            f.close()
    def write_posting_file_to_disk(self,idx):
        '''
        write posting file to disk
        :param idx: offset of the posting file
        '''
        j =json.dumps(self.posting_file.posting_file_to_json())
        with open('posting_file_'+str(idx)+'.json','w') as f:
            f.write(j)
            f.close()
    def open_sub_dic_inverted_index(self,idx):
        '''
        open sub dictionary of inverted dictionary
        :param idx: offset of the sub dictionary
        :return:
        '''
        with open('inverted_dic_file_'+str(idx)+'.json') as json_file:
            data = json.load(json_file)
            return data
    def merge_sub_dic_inverted_index(self,idx_origin,idx_aim):
        '''
        merge sub dic inverted index and posting file
        :param idx_origin: offset of origin dictionary
        :param idx_aim: offset of aim dictionary
        :return:
        '''
        dic_idx_origin = self.open_sub_dic_inverted_index(idx_origin)
        posting_file_origin = self.posting_file.open_posting_file(idx_origin)
        dic_idx_aim = self.open_sub_dic_inverted_index(idx_aim)
        posting_file_aim =  self.posting_file.open_posting_file(idx_aim)
        items_origin =dic_idx_origin.items()
        keys_aim = dic_idx_aim.keys()
        for key,value in items_origin:
            if key in keys_aim:
                dic_idx_aim[key]['frequency_show_term']+=dic_idx_origin[key]['frequency_show_term']
                pointer = dic_idx_aim[key]['posting_pointer']
                temp = dic_idx_origin[key]['posting_pointer']
                posting_file_aim[pointer].extend(posting_file_origin[dic_idx_origin[key]['posting_pointer']])
            else:
                dic_idx_aim[key]={}
                dic_idx_aim[key]['frequency_show_term'] = dic_idx_origin[key]['frequency_show_term']
                dic_idx_aim[key]['posting_pointer'] = dic_idx_origin[key]['posting_pointer']
                pointer = dic_idx_origin[key]['posting_pointer']
                temp_1 = posting_file_origin[pointer]
                posting_file_aim[pointer]=posting_file_origin[pointer]
                temp_1 = posting_file_aim[pointer]

        dic_idx_aim=self.sort_dictionary_by_key(dic_idx_aim)
        self.posting_file.posting_file_dictionary=posting_file_aim
        posting_file_aim=self.posting_file.sort_posting_file()
        self.inverted_idx=dic_idx_aim
        self.posting_file.posting_file_dictionary=posting_file_aim
        return PostingFile(posting_file_aim),dic_idx_aim
    def sort_posting_file_by_abc(self):
        '''
        split the posting file to a'b'c
        '''
        items_inverted_idx = self.inverted_idx.items()
        sorted_posting_file_hashtag={}
        a_k=['a','b','c','d','e','f','g','h','i','j','k']
        l_z=['l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        sorted_posting_file_a_k={}
        sorted_posting_file_l_z={}
        for key,value in items_inverted_idx:
            posting_id = self.inverted_idx[key]['posting_pointer']
            first_letter = key[0].lower()
            if first_letter in a_k:
                sorted_posting_file_a_k[posting_id]=self.posting_file.posting_file_dictionary[posting_id]
            elif first_letter in l_z:
                sorted_posting_file_l_z[posting_id]=self.posting_file.posting_file_dictionary[posting_id]
            else:
                sorted_posting_file_hashtag[posting_id]=self.posting_file.posting_file_dictionary[posting_id]
        self.posting_file.posting_file_dictionary= sorted_posting_file_hashtag
        self.write_posting_file_to_disk("hash")
        self.posting_file.posting_file_dictionary= sorted_posting_file_a_k
        self.write_posting_file_to_disk("a_k")
        self.posting_file.posting_file_dictionary= sorted_posting_file_l_z
        self.write_posting_file_to_disk("l_z")
    def merge_all_posting_and_inverted_idx(self):
        '''
        build the posting file and the inverted index step by step like a tournament
        '''
        path =  "C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project"
        files = []
        has_files_to_merge = True
        counter=0
        while has_files_to_merge:
            files_in_path =os.listdir(path)
            count=0
            for i in files_in_path:
                if re.match('posting_file_',i):
                    file = re.findall("\d+", i)[0]
                    files.append(file)
                    counter+=1
            max_size = int(max(files))+1
            even =True
            if len(files) %2==1:
                even=False
            if len(files) >1:
                for i in range(0,len(files),2):
                    if i+1 == len(files) and not even:
                        continue
                    posting_file_aim,dic_idx_aim = self.merge_sub_dic_inverted_index(files[i],files[i+1])
                    os.remove(path+"\\posting_file_"+files[i]+".json")
                    os.remove(path+"\\inverted_dic_file_"+files[i]+".json")
                    os.remove(path+"\\posting_file_"+files[i+1]+".json")
                    os.remove(path+"\\inverted_dic_file_"+files[i+1]+".json")
                    self.write_to_disk(max_size,posting_file=posting_file_aim,inverted_idx=dic_idx_aim)
                    max_size+=1
                files = []
            else:
                has_files_to_merge=False






