
class PostingNode:
    index=0
    def __init__(self,tweet_id,frequency_show_in_document,posting_id=''):
        self.tweet_id=str(tweet_id)
        self.frequency_show_in_document=str(frequency_show_in_document)
        if posting_id=='':
            self.posting_id=str(PostingNode.index)
        else:
            self.posting_id=str(posting_id)

        PostingNode.index+=1
