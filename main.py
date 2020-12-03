import search_engine

if __name__ == '__main__':
    corpus_path = 'C:\\Users\\Niv\\PycharmProjects\\Search_EngineProject\\testData'
    output_path = 'C:\\Users\\Niv\\PycharmProjects\\Search_EngineProject\\testData'
    stemming = True
    queries = ['@']
    num_doc_to_retrieve = 10
    search_engine.main(corpus_path,output_path,stemming,queries,num_doc_to_retrieve)
