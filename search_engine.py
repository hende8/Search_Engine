from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit
from global_method import GlobalMethod

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
    # indexer.split_posting_file_and_create_inverted_index()
    # indexer.merge_two_last_posting_file()
    # indexer.create_matrix_global_method()
    # indexer.write_inverted_index_to_txt_file()
    # dic={}
    # dic= indexer.load_inverted_index_to_dictionary_online()
    # gl=GlobalMethod(indexer)
    # print(dic.keys())
    # dic = Indexer.load_inverted_index_to_dictionary_offline()
    # print(dic.keys())


    # print("start :" ,datetime.datetime.now())
    # print("start to merge")
    # indexer.merge_posting_file_round2()


    ######################################################
    for i in range(0,length_of_array):
        print("Start :", datetime.datetime.now())
        documents_list = r.get_documents(pathes[i][0], pathes[i][0])
        for doc,j in zip(documents_list,range(len(documents_list))):
            parsed_document = p.parse_doc(doc)
            if parsed_document == None:
                continue
            parsed_doc_list.append(parsed_document)
            number_of_documents += 1
            if number_of_documents % 200000 == 0:
                print(number_of_documents)
                for doc in parsed_doc_list:
                    indexer.add_new_doc(doc)
                indexer.write_posting_to_txt_file_lower_upper(check2)
                check2 += 1
                parsed_doc_list.clear()
                parsed_doc_list = list()
                # test += 1
            elif j==len(documents_list)-1 and i==length_of_array-1:
                print("last loop")
                print(number_of_documents)
                for doc in parsed_doc_list:
                    indexer.add_new_doc(doc)
                indexer.write_posting_to_txt_file_lower_upper(check2)
                parsed_doc_list.clear()
                parsed_doc_list = list()
                print(datetime.datetime.now())
                print("@@start to merge@@")
                indexer.merge_posting_file_round2()
                indexer.merge_two_last_posting_file()
                indexer.split_posting_file_and_create_inverted_index()
                indexer.write_inverted_index_to_txt_file()
                print("end merge :", datetime.datetime.now())
    ######################################################
    #
    #
    #
    #
    #     test=0
    #     if i == length_of_array - 1:
    #         print("Start :", datetime.datetime.now())
    #         documents_list = r.get_documents(pathes[i][0], pathes[i][0])
    #         for doc in documents_list:
    #             parsed_document = p.parse_doc(doc)
    #             if parsed_document == None:
    #                 continue
    #             parsed_doc_list.append(parsed_document)
    #             number_of_documents += 1
    #             if number_of_documents%200000==0:
    #                 print( datetime.datetime.now())
    #                 print("done to parse "+str(number_of_documents)+"start to add docs to posting files")
    #                 for doc in parsed_doc_list:
    #                     indexer.add_new_docc(doc)
    #                 print("done to add "+str(number_of_documents)+"start to write to txt files")
    #                 indexer.write_posting_to_txt_file_lower_upper(check2)
    #                 check2 += 1
    #                 parsed_doc_list.clear()
    #                 parsed_doc_list=list()
    #                 test+=1
    #             # elif test==2:
    #             #     indexer.merge_posting_file_round2()
    #             #     parsed_doc_list.clear()
    #             #     parsed_doc_list = list()
    #             #     print("END :", datetime.datetime.now())
    #
    #         for doc in parsed_doc_list:
    #             indexer.add_new_docc(doc)
    #         indexer.write_posting_to_txt_file_lower_upper(check2)
    #         check2 += 1
    #         print(datetime.datetime.now())
    #         print("@@start to merge@@")
    #         indexer.merge_posting_file_round2()
    #         print("end merge :" ,datetime.datetime.now())
    #
    #         parsed_doc_list.clear()
    #         parsed_doc_list = list()
    #         print("END :", datetime.datetime.now())
    #     documents_list = r.get_documents(pathes[i][0],pathes[i][0])
    #     for document in documents_list:
    #         parsed_document = p.parse_doc(document)
    #         if parsed_document ==None:
    #             continue
    #         number_of_documents += 1
    #         # if number_of_documents%20000==0:
    #         #     print(number_of_documents)
    #         parsed_doc_list.append(parsed_document)
    #         if number_of_documents%200000==0:
    #             print(datetime.datetime.now())
    #             print("finish to parse 200K docs...")
    #             for doc in parsed_doc_list:
    #                 indexer.add_new_docc(doc)
    #             print(datetime.datetime.now())
    #             indexer.write_posting_to_txt_file_lower_upper(check2)
    #             check2 += 1
    #             # if check2==4:
    #             #     print("start to merge...")
    #             #     indexer.merge_posting_files()
    #             #     indexer.split_posting_file_and_create_inverted_index()
    #             #     indexer.write_inverted_index_to_txt_file()
    #             #     indexer.load_inverted_index_to_dictionary_online()
    #             parsed_doc_list.clear()
    #             parsed_doc_list=list()
    # print(datetime.datetime.now())
    # print("END :", datetime.datetime.now())
    #
    # # stop = timeit.default_timer()
    # # print(datetime.datetime.now())
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
    inverted_index = Indexer.load_inverted_index_to_dictionary_offline()
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    #searcher.ranker.global_method_matrix(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, inverted_index)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()
    is_continue = True
    is_loaded = False
    while is_continue is True:
        query = input("Please enter a query: ")
        if query.lstrip() == '':
            print("Please enter a valid query...")
            continue
        k = int(input("Please enter number of docs to retrieve: "))
        if str.isdigit(str(k)) is False or k < 0 or k > 2000:
            print("Please enter a valid number (between 0 to 2000...")
            continue
        if is_loaded is False:
            inverted_index = load_index()
            is_loaded = True
        relevant_docs = search_and_rank_query(query, inverted_index, k)
        if relevant_docs is not None:
            for doc in relevant_docs:
                print('tweet id: {}, score (unique common words with query): {}'.format(doc, relevant_docs[doc]))
            if k > len(relevant_docs):
                print('There were only: {} tweets, out of: {}'.format(len(relevant_docs), k))
        else:
            print('No match to query: {}'.format(query))
# def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
