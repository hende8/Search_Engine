class PostingNode:
    '''
    posting node consist a details of the tweet id ,frequency in documents
    '''
    index = 0

    def __init__(self, tweet_id, tf, frequency_show_in_document, posting_id=''):
        self.tid = str(tweet_id)
        self.fr = str(frequency_show_in_document)
        if posting_id == '':
            self.pid = str(PostingNode.index)
            PostingNode.index += 1
        else:
            self.pid = str(posting_id)
        self.tf = tf
    def __iter__(self):
        print('__iter__ called')
        return self
