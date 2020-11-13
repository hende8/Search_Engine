from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk import pos_tag
import re
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
        text= "10000 People @go to #footballStadium in http://www.walla.com with 100 percent of winning"
        print(word_tokenize(text))
        text=self.parse_percentage(text)
        text= self.convert_str_to_number(text)
        # array_text_ = text.split()
        ## IMPORTANT ##
        # take care of phrases
        array_text_ = text.split(' ')
        text_without_stopwords=[]
        index = 0
        for word in array_text_:
            if word not in self.stop_words:
                text_without_stopwords.append(word)
            if "www" in word or "https" in word or "http" in word:
                for word_www in self.parse_url(word):
                    text_without_stopwords.append(word_www)
                text_without_stopwords.remove(word)
            elif word[0] == '#':
                for word_hash_tag in self.parse_hashtag(word):
                    text_without_stopwords.append(word_hash_tag)
                text_without_stopwords.remove(word)
        for i in range(len(text_without_stopwords)):
            if bool(re.search(r'\d', text_without_stopwords[i])):
                continue
            else:
                text_without_stopwords[i]=text_without_stopwords[i].lower()
        return text_without_stopwords

    def parse_hashtag(self, phrase):
        """"
        parser hash tag and lower the letters
        return array of string
        #stayAtHome -> ['@stayathome',stay,at,home]
        """
        original_phrase = phrase
        pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
        temp_phrase = list(phrase)
        if temp_phrase[1].islower():
            temp_phrase[1] = temp_phrase[1].upper()
        phrase = "".join(temp_phrase)
        temp = pattern.findall(phrase)
        temp = [str_to_lower.lower() for str_to_lower in temp]
        temp.insert(0, original_phrase[0:len(original_phrase)].lower().replace('_', ''))
        return temp

    def parse_url(self, string):
        """
        parsing url path
        return an array of the components
        """
        if "www" in string and ("https" in string or "http" in string):
            index = 2
        elif "http" in string and "www" not in string:
            index = 1
        elif "www" in string and "http" not in string and "https" not in string:
            index = 1
        url_str =re.split(r"[/:\.?=&]+",string)
        temp_website_name = url_str[index]+"." + url_str[index+1]
        url_str[index] = temp_website_name
        del url_str[index+1:index+2]
        #print(url_str)
        return url_str

    def isfloat(self, value):
        """
            check if value is a float number
        :return: boolean
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def convert_str_to_number(self, text_demo):
        """
        convert the string to number
        :param text_demo: text to parse to K\B\M
        :return: array
            10000 -> 10K
            1000000-> 1M
        """
        text_demo = text_demo.split()
        text_return = []
        for i in range(len(text_demo)):
            if text_demo[i].isdecimal() or self.isfloat(text_demo[i]):
                number = float(text_demo[i])
                if i + 1 < len(text_demo):
                    token_next = text_demo[i + 1].lower()
                    number_to_input = str(nume.numerize(number, 3))
                    if token_next.__eq__("billion"):
                        if 'K' in nume.numerize(number, 3) or 'M' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            number_to_input = (number_to_input.translate({ord('M'): None}))
                            text_return.append(text_demo[i])
                        else:
                            text_return.append(str(nume.numerize(number, 3) + 'B'))
                    elif token_next.__eq__("million"):
                        if 'K' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            text_return.append(number_to_input + 'B')
                        else:
                            number_to_input = str(nume.numerize(number, 3))
                            text_return.append(number_to_input + 'M')
                    elif token_next.__eq__("thousand"):
                        if 'K' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('K'): None}))
                            text_return.append(number_to_input + 'M')
                        elif 'M' in nume.numerize(number, 3):
                            number_to_input = (number_to_input.translate({ord('M'): None}))
                            text_return.append(number_to_input + 'B')
                        else:
                            text_return.append(number_to_input + 'K')
                    elif 1000 > number > -1000:
                        text_return.append(nume.numerize(number, 3))
                    else:
                        text_return.append(nume.numerize(number, 3))
                else:
                    text_return.append(nume.numerize(number, 3))
            else:
                if text_demo[i].__eq__("billion") or text_demo[i].__eq__("million") or text_demo[i].__eq__("thousand"):
                    continue
                if text_demo[i].__eq__("Billion") or text_demo[i].__eq__("Million") or text_demo[i].__eq__("Thousand"):
                    continue
                text_return.append(text_demo[i])

        return ' '.join(text_return)

    def parse_percentage(self, string):
        """
        change word to percent
        100 percent -> 100%
        :param string: string to check if there is a percent within
        :return: array of converted strings
        """
        text_array=string.split()
        if "percent" in text_array:
            index=text_array.index("percent")
        elif "percentage" in text_array:
            index = text_array.index("percentage")
        elif "Percentage" in text_array:
            index = text_array.index("Percentage")
        elif "Percent" in text_array:
            index = text_array.index("Percent")
        else:
            return ' '.join(text_array)
        text_array[index - 1] =text_array[index - 1] + '%'
        del text_array[index:index+1]
        return ' '.join(text_array)

    def remove_panctuation(self, text):
        """
                remove pancuations from text (like . or , or : )
                :param text: the tweet itself
                :return: tweet without panctuation
                """
        i = 0
        for char in text:
            chars = set('.,:;!()-=+')
            chars.add("\"'")
            if any((c in chars) for c in char):
                text = text.replace(str(char), "")
            i = i + 1
        return text

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
        indices = doc_as_list[4]
        retweet_text = doc_as_list[5]
        retweet_url = doc_as_list[6]
        retweet_indices = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url = doc_as_list[9]
        quote_indices = doc_as_list[10]
        term_dict = {}
        tokenized_text = self.parse_text(full_text)

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        dict_hard_words = {"keys: ": "values: "}

        i = 0
        for term in tokenized_text:
            chars = set('@#$%$')
            if any((c in chars) for c in term):
                dict_hard_words[str(i)] = tokenized_text[i]
                tokenized_text.remove(tokenized_text[i])
            i = i+1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
