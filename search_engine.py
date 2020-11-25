from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import timeit


all_documents = []

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
    all_documents = documents_list_after_parse
    stop = timeit.default_timer()
    print('Time: ', stop - start)


    # index the document data
    # dic_index=0
    # len_parsed_documents = len(documents_list_after_parse)
    indexer.divide_dictionary(documents_list_after_parse,idx)
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

    indexer.merge_all_posting_and_inverted_idx()
    indexer.sort_posting_file_by_abc()

    # indexer.posting_file.open_posting_file()
    # indexer.open_sub_dic_inverted_index(indexer.sub_dic_posting_file_idx)
    # utils.save_obj(indexer.inverted_idx, "inverted_idx")
    # utils.save_obj(indexer.postingDict, "posting")

def get_document_after_parse():
    return all_documents

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
    dicrrr = {}
    dicrrr = search_and_rank_query(query,inverted_index,k)
    for doc_tuple in dicrrr:
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
# def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
