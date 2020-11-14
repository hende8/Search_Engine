from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk import pos_tag
import re
from numerize import numerize as nume
import math
import ast



class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
    def parse_text(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text= "https://walla.com THE DOLLAR’s ... computer’s People… @go Hen’s #footballStadium... in New-York COVID-19 https://walla.com with 100 percent Alex Cohen-Levi in Tel Aviv"
        #text = text.replace("…", " ")
        text = self.remove_panctuation(text)
        # index_of_words={}
        # for word,idx in enumerate(text.split(" ")):
        #     index_of_words[word]=idx
        names_and_entities = self.get_name_and_entities(text)
        text=self.parse_percentage(text)
        text= self.convert_str_to_number(text)
        # take care of phrases
        array_text_ = text
        text_without_stopwords = []
        index = 0
        for word in array_text_:
            check_stop_word = word[0].lower() + word[1:]
            if word not in self.stop_words and check_stop_word not in self.stop_words:
                text_without_stopwords.append(word)
            else:
                continue
            if "www" in word or "https" in word or "http" in word:
                for word_www in self.parse_url(word):
                    if word_www not in self.stop_words:
                        text_without_stopwords.append(word_www)
                text_without_stopwords.remove(word)
                continue
            if "-" in word:
                splited_array = self.split_makaf(word)
                for word_ in splited_array:
                    if word_ not in text_without_stopwords:
                        text_without_stopwords.append(word_)
            if word[0] == '#' and len(word)>1:
                for word_hash_tag in self.parse_hashtag(word):
                    text_without_stopwords.append(word_hash_tag)
                text_without_stopwords.remove(word)


        return text_without_stopwords,names_and_entities
    def split_makaf(self,word):
        if word[0].isnumeric() or word[len(word)-1].isnumeric():
            array=[]
            array.append(word)
            return array
        else:
            return word.split("-")
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
        if "https://t." in string or "https://t" in string:
            return []
        if "www" in string and ("https" in string or "http" in string):
            index = 2
        elif "http" in string and "www" not in string:
            index = 1
        elif "www" in string and "http" not in string and "https" not in string:
            index = 1
        url_str =re.split(r"[/:\.?=&…]+",string)
        temp_website_name = url_str[index]+"." + url_str[index+1]
        url_str[index] = temp_website_name
        del url_str[index+1:index+2]
        index_while=0
        while index_while < len(url_str):
            if "-" in url_str[index_while]:
                temp=re.split("-",url_str[index_while])
                for term_temp,idx_within in zip(temp,range(len(temp))):
                    url_str.insert(index_while, term_temp)
                    index_while+=1
                url_str.remove(url_str[index_while])
            else:
                index_while+=1
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
                if math.isnan(float(text_demo[i])):
                    continue
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

    def get_long_url(self, url):
        """

        :param url: 2 two url . short and long
        :return:  long
        """
        c = '"'
        array=  ([pos for pos, char in enumerate(url) if char == c])
        start = array[0]
        stop = array[1]+1
        # Remove charactes from index 5 to 10
        if len(url) > stop:
            url = url[0: start:] + url[stop + 1::]
        url = url[:-2:]
        url = url[2::]
        return url

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
        array_of_text = str.split(text)
        chars = set('.,:;!()=+…')
        for word in array_of_text:
            if "www" in word or "http" in word or "https" in word:
                i += 1
                continue
            if word[-2:] == "'s" or word[-2:] == "’s":
                array_of_text[i] = word[:-2]
                i += 1
                continue
            if "#" == word:
                word=word.replace("#", "")
                array_of_text[i] = word
                i = i + 1
                continue

            for char in word:
                if any((c in chars) for c in char):
                    word = word.replace(str(char), "")
                    array_of_text[i] = word
            i = i + 1

        return ' '.join(array_of_text)
    def get_name_and_entities(self,text):
        array_text = text.split()
        array_names_and_entities = {}
        idx = 0
        while idx < len(array_text):
            current_word = array_text[idx]
            if current_word[0].isupper():
                entity =array_text[idx]
                first_index=idx
                check_stop_word =array_text[idx][0].lower() + array_text[idx][1:]
                if check_stop_word in self.stop_words and idx+1 <len(array_text) and not array_text[idx+1][0].isupper():
                    idx+=1
                    continue
                while idx+1 < len(array_text) and array_text[idx+1][0].isupper():
                    entity +=" "+array_text[idx+1]
                    idx+=1
                if entity in array_names_and_entities.keys():
                    array_names_and_entities[entity] = array_names_and_entities[entity]
                else:
                    array_names_and_entities[entity]=first_index
                idx += 1
            else:
                idx+=1
        # for word in array_names_and_entities.keys():
        #     temp=word[-2:]
        #     if word[:-2] == "'s" or word[:-2] == "’s" :
        #         word_tem = word[:-2]
        #         array_names_and_entities[word_tem] = array_names_and_entities[word]
        #         del array_names_and_entities[word]
        return array_names_and_entities

    def switch_long_url_in_short(self,text,url):
        text=text.replace("\n"," ")
        index_null= url.find("null")
        if index_null!=-1:
            url = url[:index_null] + '"' + url[index_null:index_null+4]+'"'+url[index_null+4:]
        dic_url = ast.literal_eval(url)
        array = text.split(" ")
        idx=0
        idx_value=0
        values = list(dic_url.values())
        keys = list(dic_url.keys())
        for word in  array:
            if "www" in word or "https" in word or "http" in word:
                if index_null!=-1 and values[idx_value] == "null" :
                    array[idx]= keys[idx_value]
                    idx += 1
                    idx_value+=1
                    continue
                if word == keys[idx_value]:
                    array[idx]=values[idx_value]
                    if idx_value+1>=len(values):
                        break
                idx_value += 1
            idx+=1
        return " ".join(array)



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
        doc_length = len(full_text.split(" "))
        #and tweet_id=="1280919843924070402"
        if str(url)!="{}" and ( "www" in full_text or "https" in full_text or "http" in full_text):
            print(tweet_id)
            print(full_text)
            print(url)
            full_text= self.switch_long_url_in_short(full_text,url)
        #parse text
        tokenized_text,names_and_entities = self.parse_text(full_text)

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        for term in names_and_entities:
            if term not in term_dict.keys():
                term_dict[term] = 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
