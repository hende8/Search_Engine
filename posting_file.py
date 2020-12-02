from string import ascii_lowercase
import os
import json
import timeit
from collections import OrderedDict
import re

import sys
def obj_dict(obj):
    return obj.__dict__
class PostingFile:
    '''
    posting file is a data structure that holds an posting node in a list (e.g. linked-list)
    '''

    def __init__(self, dict=None):
        if dict is not None:
            self.posting_file_dictionary = dict
        else:
            self.posting_file_dictionary = {}
            # self.initial_posting_file_by_abc()
            self.initial_posting_file_letters={}
            # self.initial_dict_letters()
        self.counter=0
        self.number_of_remove_memory_=0
        self.prepare_to_merge=[]
        self.index_posting_file=0
    def initial_dict_letters(self):
        for term in ascii_lowercase:
            self.initial_posting_file_letters[term]=term+"_0"
        self.initial_posting_file_letters['number'] = 'number_0'

    def add_term_to_posting_file(self,tweet_id, tf, freq_in_tweet,term,posting_id=None):
        '''
        add term to the posting file
        :param tweet_id:
        :param freq_in_tweet:
        :param posting_id:
        :param tf:
        :param index_place:
        :return: posting id of the new/old posting node
        '''
        self.counter+=1
        new_posting_node = PostingNode(tweet_id, tf, freq_in_tweet)

        letter = term[0]
        if 96<ord(letter)<123 or 64<ord(letter)<91:
            temp_1=term[0].lower()
            temp2=self.initial_posting_file_letters[term[0].lower()]
            keys = self.posting_file_dictionary[self.initial_posting_file_letters[term[0].lower()]].keys()
            first_letter = self.initial_posting_file_letters[term[0].lower()]
        else:
            keys = self.posting_file_dictionary[self.initial_posting_file_letters['number']].keys()
            first_letter =  self.initial_posting_file_letters['number']
        new_posting_id = new_posting_node.pid + "_" + first_letter
            #in case of existing posting pointer in the dictionary
        if posting_id is None :
            self.posting_file_dictionary[first_letter][new_posting_id]=list()
            self.posting_file_dictionary[first_letter][new_posting_id].append(new_posting_node)
            return new_posting_id
        elif posting_id is not None and posting_id in keys:
            self.posting_file_dictionary[first_letter][posting_id].append(new_posting_node)
            return posting_id
        elif posting_id is not None and posting_id not in keys:
            self.posting_file_dictionary[first_letter][posting_id]=list()
            self.posting_file_dictionary[first_letter][posting_id].append(new_posting_node)
            return posting_id
    def sort_posting_file(self,letter):
        '''
        sort and posting file by tweet id
        :return:
        '''
        keys = self.posting_file_dictionary[letter].keys()
        temp_dict = self.open_posting_file(letter,path=os.path.dirname(os.path.abspath(__file__)) + '\\posting_file_dir\\')
        for i in keys:
            items = temp_dict.items()
            for key,value in items:
                value.sort(key=lambda x: x.tid, reverse=False)
        self.posting_file_dictionary[letter].clear()
        self.posting_file_dictionary[letter]={}
        self.posting_file_dictionary[letter]=temp_dict

    def posting_file_to_json(self,letter):
        '''
        write posting file dictionary  to json
        :return:
        '''
        items=self.posting_file_dictionary[letter].items()
        temp_dic={}
        for key,value in items:
            temp_dic[key]={}
            for i in range(len(value)):
                if i == 0:
                    temp_dic[key] = list()
                tweet_id = value[i].tid
                posting_id = value[i].pid
                frequency_show_in_document = value[i].fr
                tf = value[i].tf
                p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                temp_dic[key].append(p)
        return json.dumps(temp_dic, default=lambda o: o.__dict__,
            sort_keys=True)
    def posting_file_to_json_after_merge(self,dic):
        '''
        write posting file dictionary  to json
        :return:
        '''
        items=dic.items()
        temp_dic={}
        for key,value in items:
            temp_dic[key]={}
            for i in range(len(value)):
                if i == 0:
                    temp_dic[key] = list()
                tweet_id = value[i].tid
                posting_id = value[i].pid
                frequency_show_in_document = value[i].fr
                tf = value[i].tf
                p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                temp_dic[key].append(p)
        return json.dumps(temp_dic, default=lambda o: o.__dict__,
            sort_keys=True)
    def open_posting_file(self,idx,path=""):
        '''
        open posting file file json to dictionary
        :param idx:
        :return:
        '''
        with open(path+'posting_file_'+str(idx)+'.json') as json_file:
            data = eval(json.load(json_file))
            items = data.items()
            temp_dic_posting_file = {}
            for key,value in items:
                for i in range(len(value)):
                    if i==0:
                        temp_dic_posting_file[key] = list()
                    tweet_id = value[i]['tid']
                    posting_id = value[i]['pid']
                    frequency_show_in_document = value[i]['fr']
                    tf = value[i]['tf']
                    p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                    temp_dic_posting_file[key].append(p)
        return temp_dic_posting_file

    def initial_posting_file_by_abc(self,symbol_array=None):
        if symbol_array is None:
            for c in ascii_lowercase:
                self.posting_file_dictionary[c+"_0"] = {}
            self.posting_file_dictionary['number_0'] = {}
        else:
            for c in symbol_array:
                self.posting_file_dictionary[c] = {}
        self.counter=0
    def clear_memory(self):
        print("CLEAR MEMORY !!!!!!")
        path = os.path.dirname(os.path.abspath(__file__))
        symbol_posting_file=[]
        if not os.path.exists(path+'\\posting_file_dir'):
            os.mkdir(path+'\\posting_file_dir')

        path = os.path.dirname(os.path.abspath(__file__))+'\\posting_file_dir\\'
        keys=list()
        for term,i in zip(self.posting_file_dictionary.keys(),range(len(self.posting_file_dictionary.keys()))):
            keys.append(term)
        for c in keys:
            if os.path.exists(path+'posting_file_' + str(c) + '.json'):
                if len(self.posting_file_dictionary[c].items())< 5000:
                    # symbol_posting_file.append(c)
                    continue
                print("number of items before write and delete: ",len(self.posting_file_dictionary[c].items()))
                if c[-1].isdigit():
                    temp = c[:-1] + str(int(c[-1]) + 1)
                    if 'number' in c:
                        self.initial_posting_file_letters['number'] = temp
                    else:
                        self.initial_posting_file_letters[c[0]] = temp
                else:
                    temp = c + "_0"
                    if 'number' in c :
                        self.initial_posting_file_letters['number']=temp
                    else:
                        self.initial_posting_file_letters[c[0]]=temp
                self.posting_file_dictionary[temp] = {}
                self.posting_file_dictionary[temp]=self.posting_file_dictionary[c]
                self.write_posting_file_to_disk(idx=temp)
                self.posting_file_dictionary[c].clear()
                self.posting_file_dictionary[temp].clear()
                del self.posting_file_dictionary[temp]
                del self.posting_file_dictionary[c]
                if temp[-1].isdigit():
                    temp = c.split("_")[0]+"_" + str(int(temp[-1]) + 1)
                    if 'number' in c:
                        self.initial_posting_file_letters['number'] = temp
                    else:
                        self.initial_posting_file_letters[c[0]] = temp
                    self.posting_file_dictionary[temp] = {}
                else:
                    temp = c + "_0"
                    if 'number' in c :
                        self.initial_posting_file_letters['number']=temp
                    else:
                        self.initial_posting_file_letters[c[0]]=temp
                self.posting_file_dictionary[temp] = {}
                print("new index :", temp)
                symbol_posting_file.append(temp)
            elif self.posting_file_dictionary[c] is not None:
                if len(self.posting_file_dictionary[c].items())< 7000:
                    # symbol_posting_file.append(c)
                    continue
                print("first create of json file: ",len(self.posting_file_dictionary[c].items()),"   "+c)
                self.write_posting_file_to_disk(idx=c)
                self.posting_file_dictionary[c].clear()
                del self.posting_file_dictionary[c]
                arr = c.split("_")
                temp = arr[0] + "_" + str(int(arr[1]) + 1)
                if 'number' in c:
                    self.initial_posting_file_letters['number'] = temp
                else:
                    self.initial_posting_file_letters[c[0]] = temp
                self.posting_file_dictionary[temp]={}
        self.counter = 0
        # self.initial_posting_file_by_abc(symbol_posting_file)

    def write_posting_file_to_disk(self,idx,new_dictionary=None):
        '''
        write posting file to disk
        :param idx: offset of the posting file
        '''
        # create new one
        if new_dictionary is None:
            j = json.dumps(self.posting_file_to_json(idx))
        else:
            j = json.dumps(self.posting_file_to_json_after_merge(new_dictionary))
        with open(os.path.dirname(os.path.abspath(__file__))+'\\posting_file_dir\\'+'posting_file_' + str(idx) + '.json', 'w') as f:
            f.write(j)
            f.close()
    def merge_and_clear_posting_file(self,dictionary_origin,aim_posting_file):
        keys= dictionary_origin.keys()
        keys_posting_file_disk = aim_posting_file.keys()
        has_change=False
        for key in keys:
            has_change=True
            for i in range(len(dictionary_origin[key])):
                tweet_id = dictionary_origin[key][i].tid
                posting_id = dictionary_origin[key][i].pid
                frequency_show_in_document = dictionary_origin[key][i].fr
                tf = dictionary_origin[key][i].tf
                p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                if key in keys_posting_file_disk:
                    aim_posting_file[key].append(p)
                else:
                    aim_posting_file[key]=list()
                    aim_posting_file[key].append(p)
        if has_change:
            return aim_posting_file
        else:
            dictionary_origin
    # def write_last_posting_file_to_disk(self):
    #     path = os.path.dirname(os.path.abspath(__file__))+'\\posting_file_dir\\'
    #     keys= self.initial_posting_file_letters.keys()
    #     for c in self.posting_file_dictionary.keys():
    #         self.write_posting_file_to_disk(idx=self.initial_posting_file_letters[c[0]])
    def merge_posting_files_by_index(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '\\posting_file_dir\\'
        indexes =list()
        for i in ascii_lowercase:
            indexes.append(i)
        indexes.append('number')
        for c in indexes:
            index=0
            dic_of_posting_file= {}
            dictionary={}
            start = timeit.default_timer()

            while(os.path.exists(path+'posting_file_' + str(c) +"_"+ str(index) + '.json')):
                dic_of_posting_file[str(index)]=self.open_posting_file(idx=str(c) +"_"+ str(index), path=path)
                dictionary[str(index)]= {}
                index+=1
            if index<=1:continue
            for dic,i in zip(range(1,len(dic_of_posting_file)),range(1,len(dic_of_posting_file))):
                to_del=list()
                keys = dic_of_posting_file[str(dic)].keys()
                for key in keys:
                    if str(i) not in key:
                        aim_index =key.split("_")[2]
                        temp = dic_of_posting_file[str(dic)][key]
                        dictionary[str(aim_index)][key]= list()
                        dictionary[str(aim_index)][key]=dic_of_posting_file[str(dic)][key]
                        to_del.append(key)
                for item in to_del:
                    del dic_of_posting_file[str(dic)][item]
                to_del.clear()
                to_del=list()
            for key in dic_of_posting_file.keys():
                for item in dictionary[key]:
                    dic_of_posting_file[key][item].extend(dictionary[key][item])
            for i in range(len(dictionary)):
                temp_index = c+"_"+str(i)
                self.write_posting_file_to_disk(idx=temp_index,new_dictionary=dic_of_posting_file[str(i)])
            dictionary.clear()
            dic_of_posting_file.clear()
            stop2 = timeit.default_timer()
            print('merge index in minutes : ',c, (stop2 - start) / 60)
    def add_term_to_posting_file_round2(self,tweet_id, tf, freq_in_tweet,term,write=False):

        if term not in self.posting_file_dictionary.keys():
            self.posting_file_dictionary[term]=[]
            new_posting_node = PostingNode(tweet_id=tweet_id,tf=tf,frequency_show_in_document=freq_in_tweet)
            self.posting_file_dictionary[term].append(new_posting_node)
        else:
            new_posting_node = PostingNode(tweet_id=tweet_id,tf=tf,frequency_show_in_document=freq_in_tweet)
            self.posting_file_dictionary[term].append(new_posting_node)

    def write_to_disk_after_X_of_documents(self):
        self.clear_posting_file_and_write_to_disk_round2(index=self.index_posting_file)
        self.posting_file_dictionary.clear()
        self.posting_file_dictionary={}
        self.index_posting_file+=1

    def clear_posting_file_and_write_to_disk_round2(self,index):
        self.write_posting_file_to_disk_round_2(idx=index,new_dictionary=self.sort_posting_list_by_key_round2(self.posting_file_dictionary))
    def write_posting_file_to_disk_round_2(self,idx,new_dictionary=None):
        '''
        write posting file to disk
        :param idx: offset of the posting file
        '''
        # create new one
        if new_dictionary is None:
            j = json.dumps(self.posting_file_to_json(idx))
        else:
            j = json.dumps(self.posting_file_to_json_round2(new_dictionary))
        with open(os.path.dirname(os.path.abspath(__file__))+'\\posting_file_dir\\'+'posting_file_' + str(idx) + '.json', 'w') as f:
            f.write(j)
            f.close()
    def posting_file_to_json_round2(self,dic=None):
        '''
        write posting file dictionary  to json
        :return:
        '''
        if dic is None:
            items=self.posting_file_dictionary.items()
        else:
            items = dic.items()
        temp_dic={}
        for key,value in items:
            temp_dic[key]={}
            for i in range(len(value)):
                if i == 0:
                    temp_dic[key] = list()
                tweet_id = value[i].tid
                posting_id = value[i].pid
                frequency_show_in_document = value[i].fr
                tf = value[i].tf
                p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                temp_dic[key].append(p)
        return json.dumps(temp_dic, default=lambda o: o.__dict__,
            sort_keys=True)
    def sort_posting_list_by_key_round2(self,dictionary):
        '''
        sort dictionary by key
        :param dictionary: dictionary to sort
        :return: sorted dictionary
        '''
        self.posting_file_dictionary= OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
        return self.posting_file_dictionary
    def merge_posting_two_files_round2(self,i,path):
        dictionary_origin=self.open_posting_file_round2(str(i),path)
        int_temp = int(i)+1
        aim_posting_file=self.open_posting_file_round2(str(int_temp),path)
        keys= dictionary_origin.keys()
        keys_posting_file_disk = aim_posting_file.keys()
        has_change=False
        for key in keys:
            has_change=True
            for i in range(len(dictionary_origin[key])):
                tweet_id = dictionary_origin[key][i].tid
                posting_id = dictionary_origin[key][i].pid
                frequency_show_in_document = dictionary_origin[key][i].fr
                tf = dictionary_origin[key][i].tf
                p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                if key in keys_posting_file_disk:
                    aim_posting_file[key].append(p)
                else:
                    aim_posting_file[key]=list()
                    aim_posting_file[key].append(p)
        return aim_posting_file
    def open_posting_file_round2(self,idx,path):
        '''
        open posting file file json to dictionary
        :param idx:
        :return:
        '''
        with open(path+'posting_file_'+str(idx)+'.json') as json_file:
            data = eval(json.load(json_file))
            items = data.items()
            temp_dic_posting_file = {}
            for key,value in items:
                for i in range(len(value)):
                    if i==0:
                        temp_dic_posting_file[key] = list()
                    tweet_id = value[i]['tid']
                    posting_id = value[i]['pid']
                    frequency_show_in_document = value[i]['fr']
                    tf = value[i]['tf']
                    p = PostingNode(tweet_id, tf, frequency_show_in_document, posting_id)
                    temp_dic_posting_file[key].append(p)
        return temp_dic_posting_file
    def remove_posting_file_round2(self,idx):
        os.remove(os.path.dirname(os.path.abspath(__file__))+'\\posting_file_dir\\posting_file_' + str(idx) + '.json',)
    def merge_all_posting_and_inverted_idx_round2(self):
        '''
        build the posting file and the inverted index step by step like a tournament
        '''
        path =  "C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project\\posting_file_dir"
        files = []
        has_files_to_merge = True
        is_merge = False
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
                is_merge = True
                for i in range(0,len(files),2):
                    if i+1 == len(files) and not even:
                        continue
                    if max_size == 6:
                        print("")
                    posting_file_aim = self.merge_posting_two_files_round2(files[i],path+'\\')
                    os.remove(path+"\\posting_file_"+files[i]+".json")
                    os.remove(path+"\\posting_file_"+files[i+1]+".json")

                    self.write_posting_file_to_disk_round_2(max_size,new_dictionary=posting_file_aim)
                    max_size+=1
                files = []
            else:
                has_files_to_merge=False
        if is_merge:
            self.posting_file_dictionary=posting_file_aim
            return self.posting_file_dictionary
        return self.posting_file_dictionary





