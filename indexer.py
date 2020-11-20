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
            try:
                if term[0].isupper():
                    term_upper = term.upper()
                    term_lower=term_upper.lower()
                    if term_upper not in self.inverted_idx.keys() and term_lower not in self.inverted_idx.keys():
                        print(term_upper)
                        self.inverted_idx[term_upper] = {}
                        self.inverted_idx[term_upper]['frequency_show_term'] = 1
                        posting_list = list()
                        posting_list.append(PostingPointer(document.tweet_id, document_dictionary[term]))
                        self.inverted_idx[term_upper]['posting_pointer'] = posting_list
                        continue
                    else:
                        print(term_upper)
                        self.inverted_idx[term_upper]['frequency_show_term']+=1
                        self.inverted_idx[term_upper]['posting_pointer'].append(PostingPointer(document.tweet_id,document_dictionary[term]))

                else:
                    term_upper= term.upper()
                    print(term_upper)
                    if term_upper in self.inverted_idx.keys():
                        print(term_upper)
                        self.inverted_idx[term] = {}
                        self.inverted_idx[term]['frequency_show_term'] = self.inverted_idx[term_upper]['frequency_show_term'] + 1
                        posting_list = list()
                        posting_list.extend(self.inverted_idx[term_upper]['posting_pointer'])
                        posting_list.append(PostingPointer(document.tweet_id, document_dictionary[term]))
                        self.inverted_idx[term]['posting_pointer']=posting_list
                        del self.inverted_idx[term_upper]  ## consume a lot of resource - check it
                    elif term not in self.inverted_idx.keys():
                        self.inverted_idx[term]={}
                        self.inverted_idx[term]['frequency_show_term']=1
                        posting_list=list()
                        posting_list.append(PostingPointer(document.tweet_id,document_dictionary[term]))
                        self.inverted_idx[term]['posting_pointer']=posting_list
                        continue
                    elif term in self.inverted_idx.keys():
                        self.inverted_idx[term]['frequency_show_term']+=1
                        self.inverted_idx[term]['posting_pointer'].append(PostingPointer(document.tweet_id,document_dictionary[term]))

            except:
                print('problem with the following key {}'.format(term[0]))
    def sort_dictionary_by_key(self):
        self.inverted_idx= OrderedDict(sorted(self.inverted_idx.items(), key=lambda t: t[0]))