from posting_node import PostingNode
from collections import OrderedDict
import json
import indexer
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

    def add_term_to_posting_file(self,tweet_id, tf, freq_in_tweet,posting_id=None):
        '''
        add term to the posting file
        :param tweet_id:
        :param freq_in_tweet:
        :param posting_id:
        :param tf:
        :param index_place:
        :return: posting id of the new/old posting node
        '''
        new_posting_node = PostingNode(tweet_id, tf, freq_in_tweet)
        new_posting_id = new_posting_node.posting_id
        keys = self.posting_file_dictionary.keys()
        if posting_id is not None and posting_id in keys:
            self.posting_file_dictionary[posting_id].append(new_posting_node)
            return posting_id
        else:
            self.posting_file_dictionary[new_posting_id]=list()
            self.posting_file_dictionary[new_posting_id].append(new_posting_node)
            return new_posting_id

    def sort_posting_file(self):
        '''
        sort and posting file by tweet id
        :return:
        '''
        items = self.posting_file_dictionary.items()
        for key,value in items:
            value.sort(key=lambda x: x.tweet_id, reverse=False)
        return self.posting_file_dictionary

    def posting_file_to_json(self):
        '''
        write posting file dictionary  to json
        :return:
        '''
        items=self.posting_file_dictionary.items()
        temp_dic={}
        for value,key in items:
            temp_dic[value] = json.dumps([ob.__dict__ for ob in key])
        return temp_dic

    def open_posting_file(self,idx):
        '''
        open posting file file json to dictionary
        :param idx:
        :return:
        '''
        with open('posting_file_'+str(idx)+'.json') as json_file:
            data = json.load(json_file)
            items = data.items()
            temp_dic_posting_file = {}
            for key,value in items:
                list= json.loads(value, object_hook=lambda d: PostingNode(**d))
                temp_dic_posting_file[key]=list
        return temp_dic_posting_file
