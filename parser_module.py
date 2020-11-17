from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk import pos_tag
import re
import math
import ast



class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.dictionary= {}
    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        #text= "# bla bal Thousand 4/7 million https://walla.com/hen-debi/evning.php THE DOLLAR’s computer’s People… @go Hen’s #football_Stadium... in New-York COVID-19 https://walla.com with percent Alex Cohen-Levi in Tel Aviv"
        #text= "U.S.A"
        # text= ""
        #text = text.replace("…", " ")
        text=text.replace('…', '')
        text=text.replace("\n"," ")
        array_text_space = text.split(" ")
        print(array_text_space)
        # index=0
        # while index<len(text):
        #     print(text[index], index)
        #     index+=1
        string_ans =""
        array_size = range(len(array_text_space))
        string_ans_index=0
        for word,idx in zip(array_text_space,array_size):
            if len(word)>3 and (("www" in word or "https" in word or "http" in word) and "www." != word and word[0]!='@' and word != "https://"):
                if word == "http" or word == "https" or word == "https:" or word == "https:/"or word == "https://":
                    continue
                ans = self.add_to_dictionary(self.parse_url(word),string_ans_index)
                string_ans+=ans
                string_ans_index += len(word)+1
                continue
            else:
                if len(word)>1 and word[0] != '#' and  self.is_ascii(word):
                    word = self.remove_panctuation(word)
                elif word == "" or (word[0]=='#' and len(word)==1) :
                    continue
            if len(word)>1 and word[0] == '#':
                temp_word = self.remove_panctuation(word)
                ans = self.add_to_dictionary(self.parse_hashtag(temp_word),string_ans_index)
                string_ans+=ans
                string_ans_index += len(word)+1
            elif len(word)==1 and word[0] == '#':
                continue
            elif len(word)>1 and word[0] == '@':
                string_ans+=self.add_to_dictionary(word,string_ans_index)
                string_ans_index += len(word)+1
            elif "percent" == word or "Percent" == word or "Percentage" ==word or "percentage" ==word:
                if(idx>0 and self.isfloat(array_text_space[idx-1])):
                    ans=self.add_to_dictionary(self.parse_percentage(array_text_space[idx-1]+" "+word),string_ans_index)
                    newstr = string_ans[:len(string_ans)-len(word)-1] + string_ans[len(string_ans)+len(word):]
                    string_ans= newstr+ans
                    string_ans_index += len(word)+1
                else:
                    string_ans += self.add_to_dictionary(word, string_ans_index)
                    string_ans_index += len(word)+1
            elif word.lstrip('-').isdigit() or self.isfloat(word.lstrip('-')) or self.isFraction(word.lstrip('-')):
                ans =self.add_to_dictionary(self.convert_str_to_number(array_text_space,idx), string_ans_index)
                string_ans += ans
                string_ans_index += len(word)+1
            else:
                string_ans+=self.add_to_dictionary(word,string_ans_index)
                string_ans_index += len(word)+1

        ans =self.get_name_and_entities(string_ans)
        return string_ans,ans
    def add_to_dictionary(self,word,index):
        array_of_words = word.split()##########################maybe to lower all letters
        ans=""
        length = range(len(array_of_words))
        for word,idx in zip(array_of_words,length):
            if word in self.stop_words:
                continue
            else:
                    ans+= word+" "
                    self.dictionary[word]=index
        if ans =="":
            return ""
        else:
            return ans

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
        # temp_phrase = list(phrase)
        print(phrase)
        if phrase[1].islower():
            phrase = phrase[:1] + phrase[1].upper() + phrase[2:]
        # phrase = "".join(temp_phrase)
        temp = pattern.findall(phrase)
        temp = [str_to_lower.lower() for str_to_lower in temp]
        temp.insert(0, original_phrase[0:len(original_phrase)].lower().replace('_', ''))
        return " ".join(temp)

    def parse_url(self, string):
        """
        parsing url path
        return an array of the components
        """
        if "t.co" in string:
            return ""
        if "www" in string and ("https" in string or "http" in string):
            index = 2
        elif "http" in string and "www" not in string:
            index = 1
        elif "www" in string and "http" not in string and "https" not in string:
            index = 1
        url_str =re.split(r"[/:\.?=&…]+",string)
        print(url_str)
        if len(url_str)<3:
            return ""
        temp_website_name = url_str[index]+"." + url_str[index+1]
        # url_str[index] = temp_website_name
        ans = temp_website_name+" "
        # del url_str[index+1:index+2]
        index_while=index+2
        while index_while < len(url_str):
            if "-" in url_str[index_while]:
                temp=re.split("-",url_str[index_while])
                range_temp = range(len(temp))
                for term_temp,idx_within in zip(temp,range_temp):
                    # url_str.insert(index_while, term_temp)
                    ans += temp[idx_within] + " "
                index_while+=1
            else:
                ans += url_str[index_while] + " "
                index_while+=1
        return ans

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

    def isFraction(self, token):
        if '/' not in token:
            return False
        values = token.split('/')
        return all(i.isdigit() for i in values)

    def convert_str_to_number_try(self, word):
        tmb = ''
        if word >= 1000000000 or word <= -1000000000:
            word =float(word / 1000000000)
            tmb ='B'
        elif word >=1000000 or word <= -1000000:
            word =float(word / 1000000)
            tmb = 'M'
        elif word >= 1000 or word <= -1000:
            word =float(word / 1000)
            tmb = 'K'
        ans = '{:.3f}'.format(word) + tmb
        return ans

    def convert_str_to_number(self,text_demo, idx):
        help_minus = ''
        text_return = []
        my_word = text_demo[idx]
        text_demo_length=len(text_demo)
        my_word=my_word.replace(",","")
        my_word=self.remove_panctuation(my_word)
        if my_word.isdecimal() or self.isFraction(my_word):
            help_minus = ''
        elif my_word.lstrip('-').isdigit() or self.isfloat(my_word.lstrip('-')) or self.isFraction(my_word.lstrip('-')):
            help_minus = '-'
            my_word = my_word.replace("-","")
        if self.isFraction(my_word) and idx+1<text_demo_length:
            text_return = ''.join(help_minus + my_word)
            if text_demo[idx+1] == "Billion" or text_demo[idx+1] == "billion":
                text_return += 'B'
                text_demo[idx+1] = ""
            if text_demo[idx + 1] == "Million" or text_demo[idx + 1] == "million":
                text_return += 'M'
                text_demo[idx + 1] = ""
            if text_demo[idx + 1] == "Thousand" or text_demo[idx + 1] == "thousand":
                text_return += 'K'
                text_demo[idx + 1] = ""
            return help_minus + ''.join(text_return)
        if not math.isnan(float(my_word)):
            number = float(my_word)
            number_numerize = self.convert_str_to_number_try(number)
            if idx + 1 < len(text_demo):
                token_next = text_demo[idx + 1].lower()
                number_to_input = str(self.convert_str_to_number_try(number))
                if token_next.__eq__("billion"):
                    if 'K' in number_numerize or 'M' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        number_to_input = (number_to_input.translate({ord('M'): None}))
                        text_return.append(my_word)
                    else:
                        text_return.append(str(number_numerize + 'B'))
                    text_demo[idx + 1] = ""

                elif token_next.__eq__("million"):
                    if 'K' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        text_return.append(number_to_input + 'B')
                    else:
                        number_to_input = str(number_numerize)
                        text_return.append(number_to_input + 'M')
                    text_demo[idx + 1] = ""
                elif token_next.__eq__("thousand"):
                    if 'K' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        text_return.append(number_to_input + 'M')
                    elif 'M' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('M'): None}))
                        text_return.append(number_to_input + 'B')
                    else:
                        text_return.append(number_to_input + 'K')
                    text_demo[idx + 1] = ""
                elif 1000 > number > -1000:
                    text_return.append(number_numerize)
                else:
                    text_return.append(number_numerize)
            else:
                text_return.append(number_numerize)
            if 1900 < number <2100 and help_minus == '':
                text_return.append(text_demo[idx])
        return help_minus + ' '.join(text_return)

    def is_ascii(self,s):
        return all(ord(c) < 128 or c=='…' or c=='’'   for c in s)

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
        return string.split(" ")[0] + '%'

    def remove_panctuation(self, word):
        """
                remove pancuations from word (like . or , or : )
                :param word
                :return: word without panctuation
                """
        chars = set('.,:;!()[]{}?=+…')
        if ("www" in word or "http" in word or "https" in word) or ('@' in word and word[0] != '@' and '.' in word):
            return word
        if "gmail" in word or "hotmail" in word or "yahoo" in word: return word
        if word[-2:] == "'s" or word[-2:] == "’s" or word[-2:] == "`s": word = word.replace(word[-2:], "")
        if ":)" == word or ":(" == word or ":-]" == word or ":-)" == word or ";)" == word or ";-)" == word or ":-(" == word or ";(" == word or ";-(" == word: return word
        if "'s" in word: word = word.replace("'s", "")
        if "’s" in word: word = word.replace("’s", "")
        if "`s" in word: word = word.replace("`s", "")
        if "#" == word:
            return word.replace("#", "")
        if '#' in word and word[0] != '#': word = word.replace("#", "")
        if '@' in word and word[0] != '@': word = word.replace("@", "")
        for char in word:
            if any((c in chars) for c in char):
                word = word.replace(str(char), "")
        return word

    def get_name_and_entities(self,text):
        array_text = text.split()
        array_names_and_entities = {}
        idx = 0
        counter=0
        len_array_text = len(array_text)
        while idx < len_array_text:
            counter=idx
            current_word = array_text[idx]
            if current_word[0].isupper():
                entity =current_word
                while idx+1 < len_array_text and array_text[idx + 1][0].isupper():
                    entity +=" "+array_text[idx+1]
                    idx+=1
                array_names_and_entities[entity]=counter
                # if not array_names_and_entities[entity]:
                #     array_names_and_entities[entity] = idx
                # else:
                #     array_names_and_entities[entity]=str(array_names_and_entities[entity] +","+ idx)
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
        list_null = [m.start() for m in re.finditer("null", url)]
        quote = 0 #when add quote before and after null, we add 2 more chars and change the index of the next null
        len_list = range(len(list_null))
        for i in len_list:
            if str(url)[list_null[i] + quote - 1] == ':':
                url = url[:list_null[i] + quote] + '"' + url[list_null[i] + quote:list_null[i] + quote + 4] + '"' + url[list_null[i] + quote + 4:]
                quote += 2
        #index_null= url.find("null")
        #if index_null!=-1 and str(url)[index_null-1] == ':':
        #    url = url[:index_null] + '"' + url[index_null:index_null+4]+'"'+url[index_null+4:]
        dic_url = ast.literal_eval(url)
        array = text.split(" ")
        idx=0
        idx_value=0
        values = list(dic_url.values())
        keys = list(dic_url.keys())
        for word in array:
            if "www" in word or "https" in word or "http" in word:
                current_value = values[idx_value]
                current_key = keys[idx_value]
                if current_value == "null":
                    array[idx]= current_key
                    idx += 1
                    idx_value+=1
                    continue
                if word == current_key:
                    array[idx]=current_value
                    idx_value +=1
                    if idx_value+1>=len(values):
                        break
                #idx_value += 1
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
        array_url_parsed = []
        if str(url)!="{}":
            dict2 = eval(url)
            values = dict2.values()
            keys = dict2.keys()
            for key in keys:
                if dict2[key] != str("null") and  "t.co" not in dict2[key]:
                    url_parsed = self.parse_url(dict2[key])
                    array_url_parsed.append(url_parsed)
        #parse text
        tokenized_text,entities_and_names = self.parse_sentence(full_text)
        doc_length = len(tokenized_text)  # after text operations.
        array_=tokenized_text.split()
        for term in array_:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        for term in entities_and_names:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        for term in array_url_parsed:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1


        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
