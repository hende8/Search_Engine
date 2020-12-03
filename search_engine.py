from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from configuration import ConfigClass
from collections import OrderedDict
import operator

import utils
import timeit
from global_method import GlobalMethod
from matplotlib import pyplot as plt

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
    check = 0
    iteration = 0
    # indexer.split_posting_file_and_create_inverted_index()
    # indexer.merge_two_last_posting_file()
    # indexer.split_posting_file_and_create_inverted_index()
    # indexer.write_inverted_index_to_txt_file()
    # dic={}
    # dic= indexer.load_inverted_index_to_dictionary_online()
    # gl=GlobalMethod(indexer)
    # print(dic.keys())
    # dic = Indexer.load_inverted_index_to_dictionary_offline()
    # print(dic.keys())
    outer_loop = 1
    is_stemmer = True
    # indexer.merge_posting_file_round2(stemmer=is_stemmer)
    # indexer.merge_two_last_posting_file(stemmer=is_stemmer)
    # indexer.split_posting_file_and_create_inverted_index(stemmer=is_stemmer)
    # indexer.write_inverted_index_to_txt_file(stemmer=is_stemmer)

    parsed_doc_list = list()
    print("end merge :", datetime.datetime.now())
    while outer_loop < 2:
        for i in range(0, length_of_array):
            print("Start :", datetime.datetime.now())
            documents_list = r.get_documents(pathes[i][0], pathes[i][0])
            for doc, j in zip(documents_list, range(len(documents_list))):
                parsed_document = p.parse_doc(doc, stemmer=is_stemmer)
                if parsed_document == None:
                    continue
                parsed_doc_list.append(parsed_document)
                number_of_documents += 1
                if number_of_documents % 200000 == 0:
                    print(number_of_documents)
                    print(number_of_documents, ":", datetime.datetime.now())

                    for doc in parsed_doc_list:
                        indexer.add_new_doc(doc)
                    indexer.write_posting_to_txt_file_lower_upper(iteration, stemmer=is_stemmer)
                    iteration += 1
                    parsed_doc_list.clear()
                    parsed_doc_list = list()
                elif j == len(documents_list) - 1 and i == length_of_array - 1:
                    print("last loop")
                    print(number_of_documents)
                    for doc in parsed_doc_list:
                        indexer.add_new_doc(doc)
                    print(number_of_documents, ":", datetime.datetime.now())
                    indexer.write_posting_to_txt_file_lower_upper(iteration, stemmer=is_stemmer)
                    parsed_doc_list.clear()
                    parsed_doc_list = list()
                    print(datetime.datetime.now())
                    print("@@start to merge@@")
                    indexer.merge_posting_file_round2(stemmer=is_stemmer)
                    indexer.merge_two_last_posting_file(stemmer=is_stemmer)
                    indexer.split_posting_file_and_create_inverted_index(stemmer=is_stemmer)
                    indexer.write_inverted_index_to_txt_file(stemmer=is_stemmer)
                    print("end merge :", datetime.datetime.now())
                    outer_loop += 1
                    number_of_documents = 0
                    is_stemmer = True

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


def load_index():
    print('Load inverted index')
    inverted_index = Indexer.load_inverted_index_to_dictionary_offline()
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()

    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    # searcher.ranker.global_method_matrix(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, inverted_index)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


# # search_engine.main(corpus_path, output_path, stemming, queries, num_doc_to_retrieve)
# def main(corpus_path, output_path, stemming, queries, num_doc_to_retrieve):
#     c=ConfigClass()
#     c.corpusPath=corpus_path
#     c.toStem=stemming
#     run_engine()


# def main():
#
#
#
#
#     run_engine()
# is_continue = True
# is_loaded = False
# while is_continue is True:
#     query = input("Please enter a query: ")
#     if query.lstrip() == '':
#         print("Please enter a valid query...")
#         continue
#     k = int(input("Please enter number of docs to retrieve: "))
#     if str.isdigit(str(k)) is False or k < 0 or k > 2000:
#         print("Please enter a valid number (between 0 to 2000...")
#         continue
#     if is_loaded is False:
#         inverted_index = load_index()
#         is_loaded = True
#     relevant_docs = search_and_rank_query(query, inverted_index, k)
#     if relevant_docs is not None:
#         for doc in relevant_docs:
#             print('tweet id: {}, score (unique common words with query): {}'.format(doc, relevant_docs[doc]))
#         if k > len(relevant_docs):
#             print('There were only: {} tweets, out of: {}'.format(len(relevant_docs), k))
#     else:
#         print('No match to query: {}'.format(query))

def main():
   # path = "C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project"
    #test_func(path)
    # run_engine()
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


def test_func(path):
    # print(" count terms in regular inverted index: {}".format(count_terms_regular()))
    # print(" count terms in stemming inverted index: {}".format(count_terms_stemming(path)))
    # print(" count numbers in regular inverted index: {}".format(count_numbers_regular(path)))
    # print(" count numbers in stemming inverted index: {}".format(count_numbers_stemming(path)))
    # inverted = load_index()
    # merge_dict = {*inverted}
    # print("num of terms {}".format(len(merge_dict)))
    # numbers = utils.load_obj(path + ")
    dict_inverted = Indexer.load_inverted_index_to_dictionary_offline()
    dict_tf_total = {}
    for dic in dict_inverted:
        dict_tf_total[str(dic)] = int(dict_inverted[str(dic)]["tf"])
    # print(len(dict_tf_total))
    # sorted_d = sorted((value, key) for (key, value) in dict_tf_total.items())
    # sorted_d.reverse()
    # lent = len(dict_tf_total)
    # print("most common {}".format(sorted_d[0:10]))
    # print("less common {}".format(sorted_d[lent - 10:]))

    zip_low = sorted(dict_tf_total.items(), key=lambda item: item[1], reverse=True)
    key, val = zip(*zip_low)
    plt.title("Zip's low")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel('terms')
    plt.ylabel('frequency')
    plt.plot(val)
    plt.show()


def count_terms_regular():
    inverted = load_index()
    merge_dict = {*inverted}
    return len(merge_dict)


def count_terms_stemming(path):
    file = open(path + "\\Stemmer\\inverted_index\\inverted_index_dic.txt", "r")
    inverted_index = {}
    line = file.readline()
    i = 0
    while line:
        i += 1
        line = file.readline()
    file.close()
    return i


def count_numbers_regular(path):
    file = open(path + "\\Posting_Files\\nums.txt", "r")
    i = 0
    with file as fp_small:
        line_small = fp_small.readline()
        while line_small:
            splited_line = line_small.split(":")
            term_ = splited_line[0]
            try:
                float(term_)
                i += 1
            except:
                line_small = fp_small.readline()
                continue
            line_small = fp_small.readline()
    file.close()
    return i


def count_numbers_stemming(path):
    file = open(path + "\\Stemmer\\Posting_Files\\nums.txt", "r")
    i = 0
    with file as fp_small:
        line_small = fp_small.readline()
        while line_small:
            splited_line = line_small.split(":")
            term_ = splited_line[0]
            try:
                float(term_)
                i += 1
            except:
                line_small = fp_small.readline()
                continue
            line_small = fp_small.readline()
    file.close()
    return i
