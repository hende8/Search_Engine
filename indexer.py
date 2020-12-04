from collections import OrderedDict
import math
import os
import datetime


class Indexer:

    def __init__(self, config):
        '''

        :param config: configuration file
        '''
        self.postingDic={}
        self.number_of_documents=0
        self.details_about_docs={}
        self.postingDic_lower={}
        self.postingDic_upper={}
        self.inverted_index={}
        self.config = config

    def add_new_doc(self,document):
        '''
        add new document to the posting dictionary by first letter in the term
        :param document: tweet to dd
        :return:
        '''
        mechane_tf = (document.doc_length - document.size_of_entities)
        if mechane_tf == 0: document.doc_length = 0.01
        document_dictionary = document.term_doc_dictionary
        max_tf=-1

        for term in document_dictionary.keys():
            if term==document.tweet_id:continue
            self.number_of_documents += 1
            tf = round(document_dictionary[term] / document.doc_length, 4)
            tf_in_doc = document_dictionary[term]
            tweet_id = document.tweet_id
            if tf_in_doc > max_tf:
                max_tf = tf_in_doc
            if term[0].islower():
                if term in self.postingDic_lower:
                    text =str(tweet_id) + " " + str(tf_in_doc) + " " + str(tf)
                    self.postingDic_lower[term] +=  text+","
                else:
                    text =  str(tweet_id) + " " + str(tf_in_doc) + " " + str(tf)
                    self.postingDic_lower[term] = text + ","
            else:
                if 'A'<=term[0]<='Z':
                    term_upper = term.upper()
                else:
                    term_upper=term
                if term_upper in self.postingDic_upper:
                    text = str(tweet_id) + " " + str(tf_in_doc) + " " + str(tf)
                    self.postingDic_upper[term_upper] += text + ","
                else:
                    text =  str(tweet_id) + " " + str(tf_in_doc) + " " + str(tf)
                    self.postingDic_upper[term_upper] = text + ","
        self.details_about_docs[document.tweet_id]={}
        self.details_about_docs[document.tweet_id]['rt']= str(document.rt)
        self.details_about_docs[document.tweet_id]['date']= str(document.tweet_date)
        self.details_about_docs[document.tweet_id]['max_tf']= str(max_tf)
        self.details_about_docs[document.tweet_id]['uni_w']= str(len(document.term_doc_dictionary))
    def write_posting_to_txt_file_lower_upper(self,idx):
        '''
        write the posting file of lower and upper cases
        :param idx: idx to write to disk
        :return:
        '''
        self.write_details_about_docs()
        self.postingDic_lower=self.sort_dictionary_by_key(self.postingDic_lower)
        path =  self.config.savedFileMainFolder+"\\"
        file = open(path + str(idx) + "_l.txt", "w",encoding="utf-8")
        self.sort_dictionary_by_key(self.postingDic_lower)
        keys = self.postingDic_lower.keys()
        for term in keys:
            text = term + ":" + self.postingDic_lower[term] + "\n"
            try:
                file.write(text)
            except:
                continue
        file.close()
        self.postingDic_lower.clear()
        self.postingDic_lower = {}
        self.postingDic_upper=self.sort_dictionary_by_key(self.postingDic_upper)
        path =  self.config.savedFileMainFolder+"\\"
        file = open(path + str(idx) + "_u.txt", "w",encoding="utf-8")
        self.sort_dictionary_by_key(self.postingDic_upper)
        keys = self.postingDic_upper.keys()
        for term in keys:
            text = term + ":" + self.postingDic_upper[term] + "\n"
            try:
                file.write(text)
            except:
                continue

        file.close()
        self.postingDic_upper.clear()
        self.postingDic_upper = {}
        self.write_details_about_docs()
    def merge_posting_file(self):
        '''
        merge every two posting files- upper and lower
        till get 2 posting files (upper and lower)
        tournament algorithm
        :return:
        '''
        path = self.config.savedFileMainFolder
        files = []
        has_files_to_merge = True
        counter = 0
        while has_files_to_merge:
            files_in_path = os.listdir(path)
            count = 0
            for i in files_in_path:
                if "txt" not in i:continue
                if i.split(".")[0][2]=="u":continue
                temp = i.split(".")[0]
                sep="_"
                temp_2= temp.split(sep,1)[0]
                files.append(int(temp_2))
                counter += 1
            files.sort()
            max_size = int(max(files)) + 1
            even = True
            if len(files) % 2 == 1:
                even = False
            if len(files) > 1:
                is_merge = True
                for i in range(0, len(files), 2):
                    if i + 1 == len(files) and not even:
                        continue
                    self.merge_two_posting_file_txt(files[i], files[i + 1], str(max_size),"l")
                    os.remove(path + "\\" + str(files[i]) + "_l.txt")
                    os.remove(path + "\\" + str(files[i + 1]) + "_l.txt")
                    max_size += 1
                files = []
            else:
                has_files_to_merge = False
        path = self.config.savedFileMainFolder
        files = []
        has_files_to_merge = True
        counter = 0
        while has_files_to_merge:
            files_in_path = os.listdir(path)
            count = 0
            for i in files_in_path:
                if "txt" not in i:continue
                if i.split(".")[0][2]=="l":continue
                temp = i.split(".")[0]
                sep = "_"
                temp_2 = temp.split(sep, 1)[0]
                files.append(int(temp_2))
                counter += 1
            files.sort()
            max_size = int(max(files)) + 1
            even = True
            if len(files) % 2 == 1:
                even = False
            if len(files) > 1:
                is_merge = True
                for i in range(0, len(files), 2):
                    if i + 1 == len(files) and not even:
                        continue
                    self.merge_two_posting_file_txt(files[i], files[i + 1], str(max_size),"u")
                    os.remove(path + "\\" + str(files[i]) + "_u.txt")
                    os.remove(path + "\\" + str(files[i + 1]) + "_u.txt")
                    max_size += 1
                files = []
            else:
                has_files_to_merge = False

    def merge_two_posting_file_txt(self, idx1, idx2, idx3, case):
        '''
        merge the values in posting files
        :param idx1: origin
        :param idx2: aim
        :param idx3: output of those index
        :param case:
        :return:
        '''
        path = self.config.savedFileMainFolder + "\\"
        dic_1 = path + str(idx1) + "_" + case + ".txt"
        dic_2 = path + str(idx2) + "_" + case + ".txt"
        path = self.config.savedFileMainFolder + "\\"
        file = open(path + str(idx3) + "_" + case + ".txt", "w", encoding="utf-8")
        with open(dic_1) as dic_1_fp, open(dic_2) as dic_2_fp:
            dic_1_line = dic_1_fp.readline()
            dic_2_line = dic_2_fp.readline()
            while dic_1_line and dic_2_line:
                try:
                    dic_1_line_term, dic_1_line_details = self.get_line_details(dic_1_line)
                    if dic_1_line_term == "" or dic_1_line_details == "":
                        dic_1_line = dic_1_fp.readline()
                        continue
                    dic_2_line_term, dic_2_line_details = self.get_line_details(dic_2_line)
                    if dic_2_line_term == "" or dic_2_line_details == "":
                        dic_2_line = dic_2_fp.readline()
                        continue
                    if dic_1_line_term == dic_2_line_term:
                        detailes_merge = dic_1_line_details + dic_2_line_details
                        file.write(dic_2_line_term + ":" + detailes_merge + '\n')
                        dic_1_line = dic_1_fp.readline()
                        dic_2_line = dic_2_fp.readline()
                    elif dic_2_line_term.lower() <= dic_1_line_term.lower():
                        file.write(dic_2_line_term + ":" + dic_2_line_details + '\n')
                        dic_2_line = dic_2_fp.readline()
                    elif dic_2_line_term.lower() > dic_1_line_term.lower():
                        file.write(dic_1_line_term + ":" + dic_1_line_details + '\n')
                        dic_1_line = dic_1_fp.readline()
                except:
                    dic_1_line = dic_1_fp.readline()
                    dic_2_line = dic_2_fp.readline()
                    continue
            while dic_1_line:
                try:
                    file.write(dic_1_line_term + ":" + dic_1_line_details + "\n")
                    dic_1_line = dic_1_fp.readline()
                    if dic_1_line:
                        dic_1_line_term, dic_1_line_details = self.get_line_details(dic_1_line)
                except:
                    dic_1_line = dic_1_fp.readline()
                    continue
            while dic_2_line:
                try:
                    file.write(dic_2_line_term + ":" + dic_2_line_details + "\n")
                    dic_2_line = dic_2_fp.readline()
                    if dic_2_line:
                        dic_2_line_term, dic_2_line_details = self.get_line_details(dic_2_line)
                except:
                    dic_2_line = dic_1_fp.readline()
                    continue
            file.close()
            dic_1_fp.close()
            dic_2_fp.close()
    def get_line_details(self,line):
        '''
        get details about thel ine
        term , tweet id , tf
        :param line:
        :return: splited line by the values
        '''
        line=line.rstrip()
        splited_line=line.split(":")
        term = ""
        list_details = ""
        try:
            term = splited_line[0]
            list_details=""
            list_details=splited_line[1]
        except:
            term=""
            list_details = ""
        return term,list_details
    def merge_two_last_posting_file(self):
        '''
        merge two last posting files and create a merged text file
        :return:
        '''
        path = self.config.savedFileMainFolder+"\\"
        files_in_path = os.listdir(path)
        list_=list()
        for f in files_in_path:
            if ".txt" in f:
                splited_file=f.split(".")
                list_.append(splited_file[0])
        dic_1= path+list_[0]+".txt"
        dic_2= path+list_[1]+".txt"
        file = open(path+"merge_posting_file.txt", "w",encoding="utf-8")
        with open(dic_1) as dic_1_fp, open(dic_2) as dic_2_fp:
            dic_1_line = dic_1_fp.readline()
            dic_2_line = dic_2_fp.readline()
            while dic_2_line and dic_1_line:
                try:
                    dic_1_line_term, dic_1_line_details = self.get_line_details(dic_1_line)
                    if dic_1_line_term =="" or dic_1_line_details=="":
                        dic_1_line = dic_1_fp.readline()
                        continue
                    dic_2_line_term, dic_2_line_details = self.get_line_details(dic_2_line)
                    if dic_2_line_term =="" or dic_2_line_details=="":
                        dic_2_line = dic_2_fp.readline()
                        continue
                    if dic_2_line_term.lower() == dic_1_line_term:
                        detailes_merge= dic_1_line_details+dic_2_line_details
                        file.write(dic_1_line_term+":"+detailes_merge+'\n')
                        dic_1_line = dic_1_fp.readline()
                        dic_2_line = dic_2_fp.readline()
                    elif dic_2_line_term.lower()<dic_1_line_term:
                        file.write(dic_2_line_term+":"+dic_2_line_details+'\n')
                        dic_2_line = dic_2_fp.readline()
                    elif dic_2_line_term.lower()>dic_1_line_term:
                        file.write(dic_1_line_term+":"+dic_1_line_details+'\n')
                        dic_1_line = dic_1_fp.readline()
                except:
                    dic_2_line = dic_2_fp.readline()
                    dic_1_line = dic_1_fp.readline()
            while dic_1_line:
                try:
                    file.write(dic_1_line_term + ":" + dic_1_line_details + "\n")
                    dic_1_line = dic_1_fp.readline()
                    if dic_1_line:
                        dic_1_line_term, dic_1_line_details = self.get_line_details(dic_1_line)
                except:
                    dic_1_line = dic_1_fp.readline()
            while dic_2_line:
                try:
                    file.write(dic_2_line_term + ":" + dic_2_line_details + "\n")
                    dic_2_line = dic_2_fp.readline()
                    if dic_2_line:
                        dic_2_line_term, dic_2_line_details = self.get_line_details(dic_2_line)
                except:
                    dic_2_line = dic_2_fp.readline()
            file.close()
            dic_1_fp.close()
            dic_2_fp.close()
    def split_posting_file_and_create_inverted_index(self):
        '''
        merge posting file and create the dictionary inverted index
        :return: inveted index
        '''
        main_posting_file = self.config.savedFileMainFolder+ '\\'
        merge_file = main_posting_file+"merge_posting_file.txt"
        array = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        counter_falta=0
        for i in array:
            open(main_posting_file + str(i) + ".txt", "w",encoding="utf-8")
        open(main_posting_file  + "nums.txt", "w",encoding="utf-8")
        with open(merge_file) as main_posting_file_fp:
            line_main_posting_file = main_posting_file_fp.readline()
            while line_main_posting_file and line_main_posting_file!="":
                letter= line_main_posting_file[0]
                letter_upper = line_main_posting_file[0].upper()
                letter_lower = line_main_posting_file[0].lower()

                if 'A'<=letter_upper<='Z':

                    path_posting_sub_file=self.config.savedFileMainFolder+"\\"+str(letter_upper)+".txt"
                    with open(path_posting_sub_file,'a') as sub_posting_file_fp:
                        while line_main_posting_file!="" and (line_main_posting_file[0] == letter_upper or line_main_posting_file[0] == letter_lower) :
                            sub_posting_file_fp.write(line_main_posting_file)
                            term,frequency,pointer=self.get_details_from_posting_file_by_line(line=line_main_posting_file)
                            try:
                                if term is None or frequency is None or pointer is None:
                                    line_main_posting_file = main_posting_file_fp.readline()
                                    continue
                                if 0==int(frequency):
                                    line_main_posting_file = main_posting_file_fp.readline()
                                    continue
                                self.inverted_index[term]={}
                                self.inverted_index[term]['tf'] = frequency
                                self.inverted_index[term]['idf'] = math.log2(self.number_of_documents/int(frequency))
                                self.inverted_index[term]['pt'] = pointer
                                line_main_posting_file = main_posting_file_fp.readline()
                            except:
                                if term in self.inverted_index.keys():
                                    del self.inverted_index[term]
                                try:
                                    line_main_posting_file = main_posting_file_fp.readline()
                                except:
                                    line_main_posting_file = main_posting_file_fp.readline()
                        sub_posting_file_fp.close()
                        continue

                else:
                    path_posting_sub_file=self.config.savedFileMainFolder+"\\"+"nums.txt"
                    with open(path_posting_sub_file,'a') as sub_posting_file_fp:
                        while line_main_posting_file!="" and line_main_posting_file[0].upper() not in array :
                            sub_posting_file_fp.write(line_main_posting_file)
                            term,frequency,pointer=self.get_details_from_posting_file_by_line(line=line_main_posting_file,pt="nums")
                            try:
                                if term is None or frequency is None or pointer is None:
                                    line_main_posting_file = main_posting_file_fp.readline()
                                    continue
                                if 0 == int(frequency) :
                                    line_main_posting_file = main_posting_file_fp.readline()
                                    continue
                                self.inverted_index[term]={}
                                self.inverted_index[term]['tf'] = frequency
                                self.inverted_index[term]['idf'] = math.log10(self.number_of_documents/float(frequency))
                                self.inverted_index[term]['pt'] = pointer
                                line_main_posting_file = main_posting_file_fp.readline()
                            except:
                                if term in self.inverted_index.keys():
                                    del self.inverted_index[term]
                                try:
                                    line_main_posting_file = main_posting_file_fp.readline()
                                except:
                                    line_main_posting_file = main_posting_file_fp.readline()

                        sub_posting_file_fp.close()
                        continue
    def write_inverted_index_to_txt_file(self):
        '''
        write the dictionary to the disk
        :return:
        '''
        path = self.config.savedFileMainFolder
        file = open(path + "\\inverted_index_dic.txt", "w",encoding="utf-8")
        keys = self.inverted_index.keys()
        for key in keys:
            frequency = self.inverted_index[key]['tf']
            idf = self.inverted_index[key]['idf']
            pointer = self.inverted_index[key]['pt']
            text = key + ":" + str(frequency) + " " + str(idf) + " " + str(pointer) + "\n"
            file.write(text)
        file.close()
    def load_inverted_index_to_dictionary_online(self):
        '''
        load inverted index when has instance of indexer
        :return:
        '''
        path = self.config.savedFileMainFolder
        file = open(path + "\\inverted_index_dic.txt", "r")
        inverted_index = {}
        line = file.readline()
        while line:
            splited_line = line.split(":")
            term = splited_line[0]
            inverted_index[term] = {}
            values = splited_line[1].split(" ")
            inverted_index[term]["tf"] = values[0]
            inverted_index[term]["idf"] = values[1]
            inverted_index[term]["pt"] = values[2].rstrip()
            line = file.readline()
        file.close()
        self.inverted_index = inverted_index
        return inverted_index
    @staticmethod
    def load_inverted_index_to_dictionary_offline(path):
        '''
        load inverted index when doesnt have an instance of Indexer
        :param path:
        :return:
        '''
        file = open(path+"\\inverted_index_dic.txt", "r")
        inverted_index={}
        line = file.readline()
        while line :
            splited_line=line.split(":")
            term=splited_line[0]
            inverted_index[term]={}
            values = splited_line[1].split(" ")
            inverted_index[term]['tf']=values[0]
            inverted_index[term]['idf']=values[1]
            inverted_index[term]['pt']=values[2].rstrip()
            line = file.readline()
        file.close()
        return inverted_index
    @staticmethod
    def get_values_in_posting_file_of_dictionary_term(term, pointer,path):
        '''
        get the values in the posting file by pointer
        :param term: term get
        :param pointer: the address
        :param path: path to the path in disk
        :return:
        '''
        path = path + '\\'
        file = open(path + str(pointer) + ".txt", "r")
        dic_tweet = {}
        with file as fp_small:
            line_small = fp_small.readline()
            while line_small:
                splited_line = line_small.split(":")
                term_ = splited_line[0]
                if term_ == term:
                    dic_tweet = Indexer.get_details_about_term_in_posting_file(splited_line[1])
                    break
                line_small = fp_small.readline()
        file.close()
        return dic_tweet

    @staticmethod
    def get_details_about_term_in_posting_file(line):
        '''
        get details about the term in posting file doesnt have an instance of indexer
        :param line:
        :return:
        '''
        details_dic = {}
        splited_line = line.split(",")
        for i in splited_line:
            details_array = i.split(" ")
            if i != "\n":
                tweet_id = details_array[0]
                details_dic[tweet_id] = {}
                details_dic[tweet_id]['tf'] = details_array[1]
                details_dic[tweet_id]['tfl'] = details_array[2]
        return details_dic
    def sort_dictionary_by_key(self, dictionary):
                        '''
                        sort dictionary by key
                        :param dictionary: dictionary to sort
                        :return: sorted dictionary
                        '''
                        self.postingDic = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))
                        return self.postingDic
    def write_details_about_docs(self):
        '''
        details about the docs like if RT and the date
        :return:
        '''
        path = self.config.savedFileMainFolder
        if not os.path.exists(path+'\\Details_about_docs'):
            os.makedirs(path+'\\Details_about_docs')
        path_to_file = self.config.savedFileMainFolder+ '\\Details_about_docs\\details_about_docs.txt'
        if os.path.isfile(path_to_file):
            file = open(path_to_file, "a")
        else:
            file = open(path_to_file, "w",encoding="utf-8")
        keys =self.details_about_docs.keys()
        for key in keys:
            file.write(key+":"+self.details_about_docs[key]['date'] +" "+self.details_about_docs[key]['rt']+" "+self.details_about_docs[key]['uni_w']+" "+self.details_about_docs[key]['max_tf']+"\n")
        file.close()
        self.details_about_docs.clear()
        self.details_about_docs={}


    def get_details_from_posting_file_by_line(self,line,pt=""):
        '''
        get details from posting file in a line
        :param line:
        :param pt:
        :return:
        '''
        split_double_dots = line.split(":")
        term = split_double_dots[0]
        try:
            tweets_=split_double_dots[1].split(",")
        except:
            return None,None,None

        number_of_tweets =str(len(tweets_))
        if pt=="":
            pointer = line[0]
        elif pt=="nums":
            pointer="nums"
        return term,number_of_tweets,pointer

    def get_details_about_term_in_inverted_index(self,term):
        '''
        get details about a term in invereted index
        :param term:
        :return:
        '''
        dic=None
        if term in self.inverted_index.keys():
            dic={}
            dic["tf"]=self.inverted_index[term]["tf"]
            dic["idf"]=self.inverted_index[term]["idf"]
            dic["pt"]=self.inverted_index[term]["pt"]
            return dic
        return dic
    @staticmethod

    def get_details_about_term_in_inverted_index(term,inverted_index):
        '''
        get deatils about therm in inverted index
        :param term:
        :param inverted_index:
        :return:
        '''
        dic=None
        if term in inverted_index.keys():
            dic={}
            dic["tf"]=inverted_index[term]["tf"]
            dic["idf"]=inverted_index[term]["idf"]
            dic["pt"]=inverted_index[term]["pt"]
            return dic
        return dic



