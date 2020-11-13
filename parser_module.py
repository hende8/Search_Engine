from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from document import Document
from numerize import numerize as nume


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokens = word_tokenize(text)
        text = "10000"

        text_demo = Parse.convert_str_to_number(text_demo)
        print(text_demo)
        text_tokens_without_stopwords_ex = [w.lower() for w in text_demo if w not in self.stop_words]
        print(text_tokens_without_stopwords_ex)

        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords

    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def convert_str_to_number(text_demo):
        text_demo = word_tokenize(text)

        for i in range(len(text_demo)):
            if text_demo[i].isdecimal() or Parse.isfloat(text_demo[i]):
                number = float(text_demo[i])
                if i+1 < len(text_demo):
                    token_next = text_demo[i+1].lower()
                    number_to_input = str(nume.numerize(number, 3))
                    if token_next.__eq__("billion"):
                        if 'K' in nume.numerize(number, 3) or 'M' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            number_to_input = (number_to_input.translate({ord('M'): None}))
                            text_demo[i] = number_to_input + 'B'
                            del (text_demo[i+1])
                        else:
                            text_demo[i] = str(nume.numerize(number, 3))
                    elif token_next.__eq__("million"):
                        if 'K' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            text_demo[i] = number_to_input + 'B'
                        else:
                            number_to_input = str(nume.numerize(number, 3))
                            text_demo[i] = number_to_input + 'M'
                        del (text_demo[i + 1])
                    elif token_next.__eq__("thousand"):
                        if 'K' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            text_demo[i] = number_to_input + 'M'
                            del (text_demo[i + 1])
                        elif 'M' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('M'): None}))
                            text_demo[i] = number_to_input + 'B'
                            del (text_demo[i + 1])
                        else:
                            text_demo[i] = number_to_input + 'K'
                            del (text_demo[i + 1])
                    elif 1000 > number > -1000:
                        text_demo[i] = nume.numerize(number, 3)
                else:
                    text_demo[i] = nume.numerize(number, 3)

        return text_demo


    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
