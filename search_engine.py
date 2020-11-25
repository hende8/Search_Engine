from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit



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
    idx=0
    documents_list_after_parse=[]
    length_of_array = len(pathes)
    for i in range(0,length_of_array):
        start = timeit.default_timer()
        if i==4:
            break
        if i==length_of_array-1:
            documents_list = r.get_documents(pathes[i][0], pathes[i][1])
            print(pathes[i][1])
        else:
            documents_list = r.get_documents(pathes[i][0],pathes[i][0])
            print(pathes[i][1])
            documents_list.extend(r.get_documents(pathes[i+1][0],pathes[i+1][0]))
            print(pathes[i+1][1])
            i+=2
        for document in documents_list:
            parsed_document = p.parse_doc(document)
            number_of_documents += 1
            documents_list_after_parse.append(parsed_document)
        stop = timeit.default_timer()
        print('Time in minutes: ', (stop - start) / 60, "round number :",i,i+1)
        for doc in documents_list_after_parse:
            indexer.add_new_doc(doc)
        print("start sort_dictionary_by_key...")
        indexer.sort_dictionary_by_key(indexer.inverted_idx)
        print("start sort_posting_file...")
        indexer.posting_file.sort_posting_file()
        print("start write_to_disk...")
        indexer.write_to_disk(indexer.sub_dic_posting_file_idx)
        print("**************** move to next sub dictionary :", idx)
    print("start merging sub dictionaries...")
    inverted_idx = indexer.merge_all_posting_and_inverted_idx()
    print("start sort_posting_file_by_abc...")
    indexer.sort_posting_file_by_abc()
    print("number of documents :", indexer.number_of_documents)



    # documents_list = r.read_file('covid19_07-11.snappy.parquet')

    # documents_list = r.read_file()
    # stop = timeit.default_timer()
    # print('Time in minutes: ', (stop - start)/60)
    # print('len of list : ',len(documents_list))
    # documents_list_after_parse=[]
    # Iterate over every document in the file
    # start = timeit.default_timer()
    # idx=0
    # for document in documents_list:
    #     # idx+=1
    #     # if idx>100:
    #     #    break
    #     parsed_document = p.parse_doc(document)
    #     number_of_documents += 1
    #     documents_list_after_parse.append(parsed_document)
    #
    # stop = timeit.default_timer()
    # print('Time in minutes: ', (stop - start)/60)

    #indexer.write_new_dictionary_to_disk()
    # index the document data
    # dic_index=0
    # len_parsed_documents = len(documents_list_after_parse)
    # indexer.divide_dictionary(documents_list_after_parse,idx)
    # sub_dic_idx=0
    # index = 0
    # limit = int(idx/10)
    # limit_extra = idx -limit*10
    # while dic_index<10:
    #     while sub_dic_idx< limit and index<len_parsed_documents:
    #         indexer.add_new_doc(documents_list_after_parse[index])
    #         sub_dic_idx+=1
    #         index+=1
    #         if dic_index==9:
    #             limit = limit +limit_extra
    #     indexer.sort_dictionary_by_key(indexer.inverted_idx)
    #     indexer.posting_file.sort_posting_file()
    #     indexer.write_to_disk(indexer.sub_dic_posting_file_idx)
    #     indexer.new_sub_dict()
    #     dic_index+=1
    #     sub_dic_idx=0
    # indexer.write_to_disk_dic_max_tf_and_uniqueness()
    # ans = indexer.open_dic_max_tf_and_uniqueness()
'''



    inverted_idx = indexer.merge_all_posting_and_inverted_idx()
    keys = inverted_idx.keys()
    counter_a=0
    counter_b=0
    counter_c=0
    counter_d=0
    counter_e=0
    counter_f=0
    counter_g=0
    counter_h=0
    counter_i=0
    counter_j=0
    counter_k=0
    counter_l=0
    counter_m=0
    counter_n=0
    counter_o=0
    counter_p=0
    counter_q=0
    counter_r=0
    counter_s=0
    counter_t=0
    counter_u=0
    counter_v=0
    counter_w=0
    counter_x=0
    counter_y=0
    counter_z=0
    counter_else=0
    for term in keys():
        letter= term[0].lower()
        if letter=='a': counter_a+=1
        elif letter=='b': counter_b+=1
        elif letter=='c': counter_c+=1
        elif letter=='d': counter_d+=1
        elif letter=='e': counter_e+=1
        elif letter=='f': counter_f+=1
        elif letter=='g': counter_g+=1
        elif letter=='h': counter_h+=1
        elif letter=='i': counter_i+=1
        elif letter=='j': counter_j+=1
        elif letter=='k': counter_k+=1
        elif letter=='l': counter_l+=1
        elif letter=='m': counter_m+=1
        elif letter=='n': counter_n+=1
        elif letter=='o': counter_o+=1
        elif letter=='p': counter_p+=1
        elif letter=='q': counter_q+=1
        elif letter=='r': counter_r+=1
        elif letter=='s': counter_s+=1
        elif letter=='t': counter_t+=1
        elif letter=='u': counter_u+=1
        elif letter=='v': counter_v+=1
        elif letter=='w': counter_w+=1
        elif letter=='x': counter_x+=1
        elif letter=='y': counter_y+=1
        elif letter=='z': counter_z+=1
        else : counter_else+=1
    print("********************************************")
    print("counter_a : ", counter_a)
    print("counter_b : ", counter_b)
    print("counter_c : ", counter_c)
    print("counter_d : ", counter_d)
    print("counter_e : ", counter_e)
    print("counter_f : ", counter_f)
    print("counter_g : ", counter_g)
    print("counter_h : ", counter_h)
    print("counter_i : ", counter_i)
    print("counter_j : ", counter_j)
    print("counter_k : ", counter_k)
    print("counter_l : ", counter_l)
    print("counter_m : ", counter_m)
    print("counter_n : ", counter_n)
    print("counter_o : ", counter_o)
    print("counter_p : ", counter_p)
    print("counter_q : ", counter_q)
    print("counter_r : ", counter_r)
    print("counter_s : ", counter_s)
    print("counter_t : ", counter_t)
    print("counter_u : ", counter_u)
    print("counter_v : ", counter_v)
    print("counter_w : ", counter_w)
    print("counter_x : ", counter_x)
    print("counter_y : ", counter_y)
    print("counter_z : ", counter_z)
    print("counter_else : ", counter_else)
    print("********************************************")
'''
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
