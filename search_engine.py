from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from configuration import ConfigClass
import pandas as pd

import datetime


def run_engine(corpus_path_, output_path_, stemming_):
    """

    :return:
    """

    number_of_documents = 0
    config = ConfigClass(corpuspath=corpus_path_,outputpath=output_path_,stemming=stemming_)
    config.corpusPath = corpus_path_
    config.savedFileMainFolder=output_path_
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)

    pathes = r.get_all_path_of_parquet()
    length_of_array = len(pathes)
    iteration = 0

    # indexer.split_posting_file_and_create_inverted_index()
    # indexer.write_inverted_index_to_txt_file()

    is_stemmer = config.toStem
    parsed_doc_list = list()
    for i in range(0, length_of_array):
        documents_list = r.get_documents(pathes[i][0], pathes[i][0])
        for doc, j in zip(documents_list, range(len(documents_list))):
            parsed_document = p.parse_doc(doc, stemmer=is_stemmer)
            if parsed_document == None:
                continue
            parsed_doc_list.append(parsed_document)
            number_of_documents += 1
            if number_of_documents % 200000 == 0:
                for doc in parsed_doc_list:
                    indexer.add_new_doc(doc)
                indexer.write_posting_to_txt_file_lower_upper(iteration)
                iteration += 1
                parsed_doc_list.clear()
                parsed_doc_list = list()
            elif j == len(documents_list) - 1 and i == length_of_array - 1:
                for doc in parsed_doc_list:
                    indexer.add_new_doc(doc)
                indexer.write_posting_to_txt_file_lower_upper(iteration)
                parsed_doc_list.clear()
                parsed_doc_list = list()
                indexer.merge_posting_file_round2()
                indexer.merge_two_last_posting_file()
                indexer.split_posting_file_and_create_inverted_index()
                indexer.write_inverted_index_to_txt_file()
                number_of_documents = 0

def load_index(path):
    inverted_index =Indexer.load_inverted_index_to_dictionary_offline(path)
    return inverted_index


def search_and_rank_query(query, inverted_index, k,path):
    p = Parse()

    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,path)
    # searcher.ranker.global_method_matrix(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, inverted_index)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)




def main(corpus_path, output_path, stemming, queries, num_doc_to_retrieve):
    # run_engine(corpus_path_=corpus_path, output_path_=output_path,stemming_=stemming)
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index(output_path)
    tuple_list=list()
    for query in queries:
        index = 0
        query = "trump going to jail"
        dict = search_and_rank_query(query, inverted_index, num_doc_to_retrieve,output_path)
        for key in dict.keys():
            print('tweet id: {}, score (unique common words with query): {}'.format(key, dict[key]))
            tupl = (index,key,dict[key])
            tuple_list.append(tupl)
        write_to_csv(tuple_list)
        index+=1
def write_to_csv(tuple_list):
    df=pd.DataFrame(tuple_list,columns=["Query_num","Tweet_id","Rank"])
    df.to_csv('results.csv')
