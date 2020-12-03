
class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_docs):
        """
                This function provides rank for each relevant document and sorts them by their scores.
                The current score considers solely the number of terms shared by the tweet (full_text) and query.
                :param relevant_docs:
                :param relevant_doc: dictionary of documents that contains at least one term from the query.
                :return: sorted list of documents by score
                """
        ans= {k: v for k, v in sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)}
        return ans

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        dic_ans ={}
        i=0
        for tweet in sorted_relevant_doc:
            if i < k:
                dic_ans[tweet] = sorted_relevant_doc[tweet]
            i += 1
        return dic_ans


