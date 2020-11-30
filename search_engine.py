from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit
import json


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
    pathes = r.get_all_path_of_parquet()
    idx = 0
    index_inner = 0
    documents_list_after_parse = []
    length_of_array = len(pathes)
    check = 0
    for i in range(0, length_of_array):
        start = timeit.default_timer()
        i = index_inner
        if i == 4:
            break
        if i == length_of_array - 1:
            documents_list = r.get_documents(pathes[i][0], pathes[i][1])
            print(pathes[i][1])
            index_inner += 1
        else:
            documents_list = r.get_documents(pathes[i][0], pathes[i][0])
            print(pathes[i][1])
            # break
            documents_list.extend(r.get_documents(pathes[i + 1][0], pathes[i + 1][0]))
            print(pathes[i + 1][1])
            index_inner += 2
        for document in documents_list:
            parsed_document = p.parse_doc(document)
            check += 1
            if parsed_document == None:
                continue
            # if check > 10000:
            #     check = 0
            #     break
            number_of_documents += 1
            documents_list_after_parse.append(parsed_document)
        stop = timeit.default_timer()
        print('Time in minutes: ', (stop - start) / 60, "round number :", i, i + 1)
        for doc in documents_list_after_parse:
            number_of_documents += 1
            indexer.add_new_doc(doc)
        documents_list_after_parse = []
        print("start sort_dictionary_by_key...")
        indexer.sort_dictionary_by_key(indexer.inverted_idx)
        print("start sort_posting_file...")
        indexer.posting_file.sort_posting_file()
        print("start write_to_disk...")
        indexer.write_to_disk(indexer.sub_dic_posting_file_idx)
        print("****** move to next sub dictionary :", idx)
        indexer.new_sub_dict()
    print("start merging sub dictionaries...")
    inverted_idx, max_index_dic = indexer.merge_all_posting_and_inverted_idx()
    print("start sort_posting_file_by_abc...")
    indexer.sort_posting_file_by_abc()
    # indexer.get_global_method_matrix(inverted_idx)
    print("number of documents :", indexer.number_of_documents)
    indexer.add_idf_to_dictionary(number_of_documents, max_index_dic)


def load_index():
    print('Load inverted index')
    # inverted_index = utils.load_obj("inverted_dic_file_2.json")
    with open('inverted_dic_file_2.json') as json_file:
        inverted_index = json.load(json_file)
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()

    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    # searcher.ranker.global_method_matrix(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    if relevant_docs is None: return None
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()
    inverted_index = load_index()
    is_continue = True
    while is_continue is True:
        query = input("Please enter a query: ")
        if query == "exit" or query == "Exit":
            is_continue = False
            continue
        if query.lstrip() == '':
            print("Please enter a valid query...")
            continue
        try:
            k = int(input("Please enter number of docs to retrieve: "))
            if k < 0 or k > 2000:
                print("Please enter a valid number (between 0 to 2000...)")
                continue
        except:
            print("Please enter a valid number (between 0 to 2000...)")
            continue

        relevant_docs = search_and_rank_query(query, inverted_index, k)
        if relevant_docs is not None:
            for doc in relevant_docs:
                print('tweet id: {}, score (unique common words with query): {}'.format(doc, relevant_docs[doc]))
            if k > len(relevant_docs):
                print('There were only: {} tweets, out of: {}'.format(len(relevant_docs), k))
        else:
            print('No match to query: {}'.format(query))
        print("")
