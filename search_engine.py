from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit


# dictionary that check if big letter show twice
dictionary_phrase_and_letters = {}
def add_to_dictionary_and_letters(parsed_document):
    for term in parsed_document.term_doc_dictionary:
            if term not in dictionary_phrase_and_letters.keys():
                dictionary_phrase_and_letters[term] = 1
            else:
                dictionary_phrase_and_letters[term] += 1
def reorganize_dictionary_with_capital_letters():
    for term in list(dictionary_phrase_and_letters.keys()):
        if term[0].isupper():
            word_letter_low = term[0].lower() + term[1:]
            if word_letter_low in dictionary_phrase_and_letters.keys():
                dictionary_phrase_and_letters[word_letter_low]  =dictionary_phrase_and_letters[word_letter_low] + dictionary_phrase_and_letters[term]
                del dictionary_phrase_and_letters[term]
def reorganize_documents_with_capital_letters( documents_list):
    for idx, document in enumerate(documents_list):
        for term in list(document.term_doc_dictionary):
            if term[0].isupper():
                word_letter_low = term[0].lower() + term[1:]
                if word_letter_low in dictionary_phrase_and_letters.keys():
                    document.term_doc_dictionary[word_letter_low] = document.term_doc_dictionary[term]
                    del document.term_doc_dictionary[term]
                else:
                    temp_upper_word = term.upper()
                    document.term_doc_dictionary[temp_upper_word] = document.term_doc_dictionary[term]
                    del document.term_doc_dictionary[term]
def run_engine():
    """

    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)

    # documents_list = r.read_file(file_name='sample3.parquet')
    documents_list = r.read_file()
    documents_list_after_parse=[]
    # Iterate over every document in the file
    start = timeit.default_timer()
    idx=0
    for document in documents_list:
        idx+=1
        if idx>100:
           break
        parsed_document = p.parse_doc(document)
        number_of_documents += 1
        documents_list_after_parse.append(parsed_document)

    stop = timeit.default_timer()
    print('Time: ', stop - start)


    # index the document data
    dic_index=0
    len_parsed_documents = len(documents_list_after_parse)

    sub_dic_idx=0
    index = 0
    limit = int(idx/10)
    limit_extra = idx -limit*10
    while dic_index<10:
        while sub_dic_idx< limit and index<len_parsed_documents:
            indexer.add_new_doc(documents_list_after_parse[index])
            sub_dic_idx+=1
            index+=1
            if dic_index==9:
                limit = limit +limit_extra
        indexer.sort_dictionary_by_key(indexer.inverted_idx)
        indexer.posting_file.sort_posting_file()
        indexer.write_to_disk(indexer.sub_dic_posting_file_idx)
        indexer.new_sub_dict()
        dic_index+=1
        sub_dic_idx=0

    indexer.merge_all_posting_and_inverted_idx()


    first = str(indexer.sub_dic_posting_file_idx-2)
    second= str (indexer.sub_dic_posting_file_idx-1)
    indexer.merge_sub_dic_inverted_index(first,second)
    print('Finished parsing and indexing. Starting to export files')
    file_name = first+','+ second
    indexer.write_to_disk(file_name)

    indexer.sort_posting_file_by_abc()

    # indexer.posting_file.open_posting_file()
    # indexer.open_sub_dic_inverted_index(indexer.sub_dic_posting_file_idx)
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
# def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
