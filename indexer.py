from posting_pointer import PostingPointer
from collections import OrderedDict

class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.posting_index=0

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
            #try:
            if term[0].isupper():
                term_upper = term.upper()
                term_lower=term_upper.lower()
                # in case of new term in the dictionary - capital or lower it doesnt matter
                if term_upper not in keys  and term_lower not in keys:
                    self.inverted_idx[term_upper] = {}
                    self.inverted_idx[term_upper]['frequency_show_term'] = 1
                    posting_list = list()
                    posting_list.append(PostingPointer(document.tweet_id, document_dictionary[term]))
                    self.inverted_idx[term_upper]['posting_pointer'] = posting_list
                    continue
                    #in case of capital letter already exists in the dictionary
                elif term_upper in  keys and term_lower not in keys:
                    self.inverted_idx[term_upper]['frequency_show_term']+=1
                    self.inverted_idx[term_upper]['posting_pointer'].append(PostingPointer(document.tweet_id,document_dictionary[term]))
                    #in case of word with capital letter fit to word with lower case
                elif term_lower in keys:
                    # self.inverted_idx[term_lower] = {}
                    self.inverted_idx[term_lower]['frequency_show_term'] +=1
                    posting_list.append(PostingPointer(document.tweet_id, document_dictionary[term]))
                    self.inverted_idx[term_lower]['posting_pointer']=posting_list
            else:
                term_upper= term.upper()
                # in case of word that already exists in dictionary
                if term_upper in keys:
                    self.inverted_idx[term] = {}
                    self.inverted_idx[term]['frequency_show_term'] = self.inverted_idx[term_upper]['frequency_show_term'] + 1
                    posting_list = list()
                    posting_list.extend(self.inverted_idx[term_upper]['posting_pointer'])
                    posting_list.append(PostingPointer(document.tweet_id, document_dictionary[term]))
                    self.inverted_idx[term]['posting_pointer']=posting_list
                    del self.inverted_idx[term_upper]  ## consume a lot of resource - check it
                    # in case of new term in dictionary
                elif term not in keys:
                    self.inverted_idx[term]={}
                    self.inverted_idx[term]['frequency_show_term']=1
                    posting_list=list()
                    posting_list.append(PostingPointer(document.tweet_id,document_dictionary[term]))
                    self.inverted_idx[term]['posting_pointer']=posting_list
                    continue
                    # in case of new term that join to exist term in dictionary
                elif term in keys:
                    self.inverted_idx[term]['frequency_show_term']+=1
                    self.inverted_idx[term]['posting_pointer'].append(PostingPointer(document.tweet_id,document_dictionary[term]))

           # except:
                #print("")
                # print(term)
                # print(document.tweet_id)
                # print(document.term_doc_dictionary)
                # print('problem with the following key {}'.format(term[0]))
                # print("#####################################")
    def sort_dictionary_by_key(self):
        self.inverted_idx= OrderedDict(sorted(self.inverted_idx.items(), key=lambda t: t[0]))