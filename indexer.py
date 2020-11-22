from collections import OrderedDict
from posting_file import PostingFile
from posting_node import PostingNode
import json
import re
import os

class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.config = config
        self.posting_file = PostingFile()
        self.sub_dic_posting_file_idx=0
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
        # Go over each term in the doc
        for term in document_dictionary.keys():
            keys = self.inverted_idx.keys()
            try:
                if term =="3.63M":
                    print("")
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
    def sort_dictionary_by_key(self,dictionary):
        self.inverted_idx= OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
        return self.inverted_idx
    def write_to_disk(self,idx, posting_file=None,inverted_idx=None):
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
        j =json.dumps(self.posting_file.posting_file_to_json())
        with open('posting_file_'+str(idx)+'.json','w') as f:
            f.write(j)
            f.close()

    def open_sub_dic_inverted_index(self,idx):
        with open('inverted_dic_file_'+str(idx)+'.json') as json_file:
            data = json.load(json_file)
            return data
    def merge_sub_dic_inverted_index(self,idx_origin,idx_aim):
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
        path = "C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project"
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




