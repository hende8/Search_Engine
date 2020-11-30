from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit

import datetime

def run_engine():
    """

    :return:
    """
    number_of_documents = 0
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    pathes = r.get_all_path_of_parquet()
    length_of_array = len(pathes)
    check=0
    check2=0
    parsed_doc_list = list()

    for i in range(0,length_of_array):
        if i ==10 or check2==11:
            break
        print(datetime.datetime.now())
        documents_list = r.get_documents(pathes[i][0],pathes[i][0])
        start3 = timeit.default_timer()
        for document in documents_list:
            parsed_document = p.parse_doc(document)
            check+=1
            if parsed_document ==None:
                continue
            number_of_documents += 1
            parsed_doc_list.append(parsed_document)
            if number_of_documents%1000==0:
                stop3 = timeit.default_timer()
                print('total 200K of docs time to parse', (stop3 - start3) / 60, "round number :", i,i + 1)
                print(datetime.datetime.now())
                for doc in parsed_doc_list:
                    indexer.add_new_doc(doc)
                print("start writing and finish to add docs to post dictionary ", number_of_documents)
                print(datetime.datetime.now())
                indexer.write_posting_file_to_txt_file(check2)
                print(datetime.datetime.now())
                check2 += 1
                parsed_doc_list.clear()
                parsed_doc_list=list()
                if check2==10:
                    start3 = timeit.default_timer()
                    indexer.merge_posting_files()
                    indexer.split_posting_file_and_create_inverted_index()
                    stop3 = timeit.default_timer()
                    print('total time to merge 400K of docs', (stop3 - start3) / 60, "round number :", i)
                    check2+=1
                    break
    stop3 = timeit.default_timer()
    print('total 200K of docs time to parse and write txt file', (stop3 - start3) / 60, "round number :", i)
    # start3 = timeit.default_timer()
    # indexer.merge_posting_files()
    # stop3 = timeit.default_timer()
    # print('total time to merge 400K of docs', (stop3 - start3) / 60, "round number :", i, i + 1)


    # stop = timeit.default_timer()
    # print(datetime.datetime.now())
    # print('parse Time in minutes: ', (stop - start) / 60, "round number :",i,i+1)
    # start = timeit.default_timer()
    # documents_list.clear()
    # documents_list=[]
    # check2=0
    # start2 = timeit.default_timer()
    #
    # for doc in documents_list_after_parse:
    #     indexer.add_new_doc(doc)
    #     if check2==200000:
    #         indexer.write_posting_file_to_txt_file(check2)
    #     if check2==400000:
    #         indexer.write_posting_file_to_txt_file(check2)
    #         start = timeit.default_timer()
    #         indexer.merge_posting_files()
    #         stop = timeit.default_timer()
    #         print('merge Time in minutes: ', (stop - start) / 60, "round number :", i, i + 1)
    #
    #     # if check2==3:
    #     #     indexer.write_posting_file_to_txt_file(check2)
    #     # if check2==4:
    #     #     indexer.write_posting_file_to_txt_file(check2)
    #     # if check2==5:
    #     #     indexer.write_posting_file_to_txt_file(check2)
    #     # if check2 == 6:
    #     #     indexer.write_posting_file_to_txt_file(check2)
    #     # # if check2 == 7:
    #     # #     indexer.write_posting_file_to_txt_file(check2)
    #     check2 += 1
    # print('total time in merge and create posting file in minutes: ', (stop - start2) / 60, "round number :", i,
    #       i + 1)
    # indexer.merge_posting_files()
    print("finish")
    # indexer.posting_file.merge_all_posting_and_inverted_idx_round2()
    # documents_list_after_parse.clear()
    # documents_list_after_parse=[]
    # stop2 = timeit.default_timer()
    #indexer.posting_file.write_last_posting_file_to_disk()
    print(datetime.datetime.now())
    # print('%%%%%%%%%create posting files Time in minutes: ', (stop2 - start) / 60, "round number :",i,i+1)
    # start = timeit.default_timer()
    # indexer.posting_file.write_last_posting_file_to_disk()
    # print("starting merging.........")
    # print(datetime.datetime.now())
    # indexer.merge_posting_files_by_index()
    # stop2 = timeit.default_timer()
    # print('#########Merge time ny minutes: ', (stop2 - start) / 60)

    # searcher =Searcher(inverted_idx)
    # searcher.expand_query()

    # indexer.posting_file.open_posting_file()
    # indexer.open_sub_dic_inverted_index(indexer.sub_dic_posting_file_idx)
    # utils.save_obj(indexer.inverted_idx, "inverted_idx")
    # utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    searcher.ranker.global_method_matrix(inverted_index)
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
