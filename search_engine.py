from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils

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
    documents_list = r.read_all_files()
    documents_list_after_parse=[]
    # Iterate over every document in the file
    for idx, document in enumerate(documents_list):
    # parse the document
        parsed_document = p.parse_doc(document)
        number_of_documents += 1
        add_to_dictionary_and_letters(parsed_document)
        documents_list_after_parse.append(parsed_document)
        if idx==1:
            break
    reorganize_dictionary_with_capital_letters()
    reorganize_documents_with_capital_letters(documents_list_after_parse)

    # index the document data
    for doc in documents_list_after_parse:
        indexer.add_new_doc(doc)
    print('Finished parsing and indexing. Starting to export files')

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
