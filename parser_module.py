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
        self.dictionary = {}
        self.dictionary_index = {}
        self.dic_entities = {}
        self.dic_entities_index = {}
        self.array_names_and_entities={}
    def parse_sentence(self, text,stemmer=False):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text ="https://www.rawstory.com/2020/07/trump-to-blow-off-cdc-recommendations-and-issue-his-own-guidelines-for-reopening-schools-report"
        self.array_names_and_entities={}
        array_text_space = text.split(" ")
        # print(text)
        string_ans = ""
        array_size = range(len(array_text_space))
        string_ans_index = 0
        for word, idx in zip(array_text_space, array_size):
            if self.is_url(word):
                if "t.co" in word:continue
                ans = self.add_to_dictionary(self.parse_url(word), string_ans_index)
                string_ans += ans
                string_ans_index += len(word) + 1
                continue
            else:
                if len(word)>1 and word[0] != '#' and  self.is_ascii(word) and not self.isfloat(word):
                    word = self.remove_panctuation(word)
                elif word == "" or (len(word)==1 and word[0]=='#') :
                    continue
            if len(word)>1 and word[0] == '#':
                temp_word = self.remove_panctuation(word)
                if temp_word == "" or temp_word == "#":
                    continue
                ans = self.add_to_dictionary(self.parse_hashtag(temp_word), string_ans_index)
                string_ans += ans
                string_ans_index += len(word) + 1
            elif len(word) == 1 and (word[0] == '#' or word[0] == '³'):
                continue
            elif len(word) > 1 and word[0] == '@':
                string_ans += self.add_to_dictionary(word, string_ans_index)
                string_ans_index += len(word) + 1
            elif "percent" == word or "Percent" == word or "Percentage" == word or "percentage" == word:
                if (idx > 0 and self.isfloat(array_text_space[idx - 1])):
                    ans = self.add_to_dictionary(self.parse_percentage(array_text_space[idx - 1] + " " + word),
                                                 string_ans_index)
                    newstr = string_ans[:len(string_ans) - len(word) - 1] + string_ans[len(string_ans) + len(word):]
                    string_ans = newstr + ans
                    string_ans_index += len(word) + 1
                else:
                    string_ans += self.add_to_dictionary(word, string_ans_index)
                    string_ans_index += len(word) + 1
            elif word.lstrip('-').isdigit() or self.isfloat(word.lstrip('-')) or self.isFraction(word.lstrip('-')):
                ans = self.add_to_dictionary(self.convert_str_to_number(array_text_space, idx), string_ans_index)
                string_ans += ans
                string_ans_index += len(word) + 1
            else:
                string_ans += self.add_to_dictionary(word, string_ans_index)
                string_ans_index += len(word) + 1
        entities_and_names =self.get_name_and_entities(text)
        array_parsed = string_ans.split()
        array_parsed_stemmer=[]
        stemmer_s=PorterStemmer()
        temp_array=[]
        if stemmer:
            for term in array_parsed:
                if term[0].isupper():
                    temp_array.append(term)
                else:
                    temp_array.append(stemmer_s.stem(term))
            array_parsed=temp_array
        for term in entities_and_names:
            array_parsed.append(term)
        return array_parsed
    def is_url(self,text):
        '''
        check if string is a url path
        :param text: url
        :return: boolean
        '''
        regex = re.compile(
            r'^(?:http|ftp)s?://|(?:www)?.'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, text) is not None

    def add_to_dictionary(self, text, index):
        array_of_words = re.split('\s+', text)
        length = range(len(array_of_words))
        ans = ""
        for word, idx in zip(array_of_words, length):
            if word.lower() not in self.stop_words:
                ans += word + " "
                self.dictionary[word] = index
        if ans == "":
            return ""
        return ans

    def parse_hashtag(self, phrase):
        """"
        parser hash tag and lower the letters
        return array of string
        #stayAtHome -> ['@stayathome',stay,at,home]
        """
        original_phrase = phrase
        pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
        if phrase[1].islower():
            phrase = phrase[:1] + phrase[1].upper() + phrase[2:]
        temp = pattern.findall(phrase)
        temp = [str_to_lower.lower() for str_to_lower in temp]
        temp.insert(0, original_phrase[0:len(original_phrase)].lower().replace('_', ''))
        return " ".join(temp)

    def parse_url(self, string):
        """
        parsing url path
        return an array of the components
        """
        if string is not None:
            r = re.split('[/://?=-]', string)
            ans = " ".join(r).lstrip()
            array_url= ans.split()
            length= range(len(array_url))
            for word,idx in zip(array_url,length):
                if "www" in word and "http" not in word and "https" not in word:
                    temp_website_name = array_url[1] + "." + array_url[2]
                    array_url[idx]=temp_website_name
                    break
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
        """
        check if value is a fraction number
        :return: boolean
        """
        if '/' not in token:
            return False
        values = token.split('/')
        return all(i.isdigit() for i in values)

    def convert_str_to_number_kmb(self, word):
        """
                check if value is a float number, and return the wanted number. etc: 1000->1K, 1013456->1.013M
                :return: boolean
                """
        tmb = ''
        if word >= 1000000000 or word <= -1000000000:
            word = float(word / 1000000000)
            tmb = 'B'
        elif word >= 1000000 or word <= -1000000:
            word = float(word / 1000000)
            tmb = 'M'
        elif word >= 1000 or word <= -1000:
            word = float(word / 1000)
            tmb = 'K'
        ans = '{:0.3f}'.format(word)
        return '{0:g}'.format(float(ans)) + tmb

    def convert_str_to_number(self, text_demo, idx):
        """
        check every type of number and return it as a string. etc: 1K,1M,1B,-900,23/5,2020,2K
        :return: boolean
        """
        help_minus = ''
        text_return = []
        my_word = text_demo[idx]
        text_demo_length = len(text_demo)
        my_word = my_word.replace(",", "")
        if re.search('-', my_word):
            help_minus = '-'
            my_word = my_word.replace("-", "")
        if not self.isfloat(my_word): my_word = self.remove_panctuation(my_word)
        if self.isFraction(my_word):
            if idx + 1 == text_demo_length:
                return ''.join(help_minus + my_word)
            text_return = ''.join(help_minus + my_word)
            token_next = text_demo[idx + 1].lower()
            if token_next == "billion" or token_next == "billions":
                text_return += 'B'
                text_demo[idx + 1] = ""
            if token_next == "million" or token_next == "millions":
                text_return += 'M'
                text_demo[idx + 1] = ""
            if text_demo[idx + 1] == "thousand" or token_next == "thousands":
                text_return += 'K'
                text_demo[idx + 1] = ""
            return help_minus + ''.join(text_return)
        if not math.isnan(float(my_word)):
            number = float(my_word)
            number_numerize = self.convert_str_to_number_kmb(number)
            if idx + 1 < len(text_demo):
                token_next = text_demo[idx + 1].lower()
                number_to_input = str(number_numerize)
                if token_next.__eq__("billion") or token_next.__eq__("billions"):
                    if 'K' in number_numerize or 'M' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        number_to_input = (number_to_input.translate({ord('M'): None}))
                        text_return.append(my_word)
                    else:
                        text_return.append(str(number_numerize + 'B'))
                    text_demo[idx + 1] = ""

                elif token_next.__eq__("million") or token_next.__eq__("millions"):
                    if 'K' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        text_return.append(number_to_input + 'B')
                    else:
                        number_to_input = str(number_numerize)
                        text_return.append(number_to_input + 'M')
                    text_demo[idx + 1] = ""
                elif token_next.__eq__("thousand") or token_next.__eq__("thousands"):
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
            if 1900 < number < 2100 and help_minus == '':
                text_return.append(text_demo[idx])
        return help_minus + ' '.join(text_return)

    def is_ascii(self, s):
        return all(ord(c) < 128 or c == '…' or c == '’' or c == '³' for c in s)

    def parse_percentage(self, string):
        """
        change word to percent
        100 percent -> 100%
        :param string: string to check if there is a percent within
        :return: array of converted strings
        """
        return re.split('\s+', string)[0] + '%'

    def remove_panctuation(self, word):
        """
                remove pancuations from word (like . or , or : )
                :param word
                :return: word without panctuation
                """
        chars = set('.,:;!()[]{}?=+…$&')
        if re.match(r'[^@]+@[^@]+\.[^@]+', word): return word
        if "#" == word: return ""
        # if ('@' in word and word[0] != '@' and '.' in word):
        #     return word
        # if "gmail" in word or "hotmail" in word or "yahoo" in word: return word
        if word[-2:] == "'s" or word[-2:] == "’s" or word[-2:] == "`s": word = word.replace(word[-2:], "")
        smiles= [":)",":(",":-]",":-)",";)",";-)",":-(", ";(",";-(",":-P",":P"]
        if word in smiles:return word
        # if ":)" == word or ":(" == word or ":-]" == word or ":-)" == word or ";)" == word or ";-)" == word or ":-(" == word or ";(" == word or ";-(" == word: return word
        # if "'s" in word: word = word.replace("'s", "")
        # elif "’s" in word: word = word.replace("’s", "")
        # elif "`s" in word: word = word.replace("`s", "")
        if "\n" in word: word = word.replace("\n", " ")
        if '#' in word and word[0] != '#': word = word.replace("#", "")
        if '@' in word and word[0] != '@': word = word.replace("@", "")

        word = word.replace("-"," ")
        word = re.sub(r'[.,!?,…:;^“"{}=+()/[\[\]]', '', word)
        return word

    # def get_name_and_entities(self,idx, text):
    #     array_text = text
    #     counter = 0
    #     len_array_text = len(array_text)
    #     part_of_entity=False
    #     # while idx < len_array_text:
    #     counter = idx
    #     current_word = array_text[idx]
    #     if current_word[0].isupper():
    #         entity = current_word
    #         self.dic_entities_index[idx] = 1
    #         while idx + 1 < len_array_text and array_text[idx + 1][0].isupper():
    #             part_of_entity=True
    #             entity += " " + self.remove_panctuation(array_text[idx + 1])
    #             idx += 1
    #             self.dic_entities_index[idx]=1
    #         if not part_of_entity:
    #             if entity.lower() in self.stop_words:
    #                 idx += 1
    #             else:
    #                 self.array_names_and_entities[entity] = counter
    #                 self.dic_entities_index[idx] = 1
    #         else:
    #             self.array_names_and_entities[entity] = counter
    #         part_of_entity=False
    #         idx += 1
    #     else:
    #         idx += 1
    #     return self.array_names_and_entities

    def get_name_and_entities(self,text):
        rx2 = re.compile(r'[A-Z][-a-zA-Z]*(?:\s+[A-Z][-a-zA-Z]*)*')
        matches = rx2.findall(text)
        tokinzed_entity_new = [e for e in matches if len(e.split()) > 1]
        return tokinzed_entity_new

    # def get_name_and_entities_new(self, array_text):
    #     counter = 0
    #     len_array_text = len(array_text)
    #     part_of_entity=False
    #     idx=0
    #     change=False
    #     current_word=array_text[idx]
    #     while idx < len_array_text :
    #         counter = idx
    #         current_word = array_text[idx]
    #         if len(current_word)>1 and current_word[0].isupper():
    #             entity=self.remove_panctuation(current_word)
    #             while idx + 1 < len_array_text and array_text[idx + 1][0].isupper():
    #                 part_of_entity=True
    #                 array = self.remove_panctuation(array_text[idx + 1]).split()
    #                 if len(array)>1 and array[1][0].isupper():
    #                     entity += " " + array[0]
    #                     array_text[idx+1]=array[1]
    #                     idx+=1
    #                     change = True
    #                     break
    #                 entity += " " + array[0]
    #                 idx += 1
    #             if not part_of_entity:
    #                 if entity.lower() in self.stop_words:
    #                     idx += 1
    #                     continue
    #                 else:
    #                     self.array_names_and_entities[entity] = counter
    #                     idx += 1
    #             else:
    #                 self.array_names_and_entities[entity] = counter
    #                 if change :
    #                     change=False
    #                 else:
    #                      idx += 1
    #             part_of_entity=False
    #         else:
    #             idx += 1
    #     return self.array_names_and_entities

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
        url=str(url)
        if url!="{}" and "null" not in url :
            dict2 = eval(url)
            values = dict2.values()
            keys = dict2.keys()
            for key in keys:
                if dict2[key] != str("null") and  "t.co" not in dict2[key]:
                    url_parsed = self.parse_url(dict2[key])
                    check= url_parsed.split()
                    for word in check:
                        array_url_parsed.append(word)
        #parse text
        tokenized_text = self.parse_sentence(full_text,stemmer=False)
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        for term in array_url_parsed:
            if term=='http' or term=='https' or term=='www':
                continue
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1


        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
