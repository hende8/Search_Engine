
class PostingPointer:
    index=0
    def __init__(self,doc_id,freq):
        self.document_id=doc_id
        self.frequency_show_in_document=freq
        self.posting_id=PostingPointer.index
        PostingPointer.index+=1
