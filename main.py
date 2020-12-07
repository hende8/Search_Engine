import search_engine
import utils

if __name__ == '__main__':
    corpus_path = 'C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project\\testData'
    output_path = 'C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project\\testData'
    q_path = 'C:\\Users\\HEN\\PycharmProjects\\Search_Engine_Project\\queries.txt'
    stemming = False
    queries = ['trump']
    num_doc_to_retrieve = 2000
    # queries = utils.read_text_queries(q_path)
    search_engine.main(corpus_path,output_path,stemming,queries,num_doc_to_retrieve)
