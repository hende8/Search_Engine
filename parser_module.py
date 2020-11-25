from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
import re
import math
import ast


class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.dictionary_term_index = {}
        self.array_names_and_entities = {}
        self.covid_list = ["corona", "covid", "covid-19", "covid19", "coronavirus", "coronaviruses", "#covid19",
                           "#corona", "#COVIDー19", "#coronaviruses", "#covid", "#covid-19", "#coronavirus"]
        self.list_percent = ["percent", "Percent", "Percentage", "percentage"]

    def parse_sentence(self, text, stemmer=False):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        # text= re.sub(r'http\S+|www.\S+', '', 'www.ynet.co.il')
        # print(text)
        # text = "6 9 0 7a ❶ ³"

        # text = "100⁰ # \ | @ ! $ % ^ & * ( ) ` ~ + = _ \ ' | : ; / ? . , } { ] [ https://  3.63 million say “not at all.” I walked in corona the Corona in Corona  covid-19 streed. COVID-19 and he found 10 million dollar for 6 percent"
        #text = "€£💐🔃🙏🏻❤⬇🐮💗，🎊🎁🎉🎈🍸‘🤦🏻‍♀🕯🙏🏼🔹€4️⃣🐣👍🏼🍰🚨💥🇺🇸🚫✅❗️👇⁦👏⁩“”⚠🇦🇷‼😭😩😪🤬🤡😷😁😳😂😢🤣⑥²⁸¹❶❷❽②⑦&$.,!?,…:;^ Meet walked Donald Trump in Y'all Tom the streed and he found 10 million dollar for 6 percent https://www.rawstory.com/2020/07/trump-to-blow-off-cdc-recommendations-and-issue-his-own-guidelines-for-reopening-schools-report"
        self.array_names_and_entities = {}
        self.dictionary_index = {}
        text = text.replace("\n", ". ")
        text = self.ignore_emojis(text)
        array_text_space = text.split(" ")
        array_text_space = self.seperate_words_with_dots(array_text_space)
        string_ans = ""
        array_size = range(len(array_text_space))
        string_ans_index = 0
        entities_url = []  # help us to replace the url to "" because in get_entities it returns parts of the url
        for word, idx in zip(array_text_space, array_size):
            ans = ""
            # print(text)
            if word == '' or word == ' ': continue
            check_digit = self.isdigit(word)
            if (len(word) < 2 and check_digit is False) or self.is_ascii(word) is False:
                word = self.remove_panctuation(word)
                if self.is_ascii(word) is False or word == '' or word == " " or len(word)<2:
                    # print(word)
                    continue
            if ans == "" and self.is_url(word):
                entities_url.append(word)
                if "t.co" in word: continue
                ans = self.parse_url(word)
                if ans == "": entities_url.remove(word)
            else:
                if ans == "" and len(word) < 2 and word[0] != '#' and self.is_ascii(word) and not self.isfloat(word):
                    word = self.remove_panctuation(word)
            if ans == "" and word[0] == '#':
                temp_word = self.remove_panctuation(word)
                if temp_word == "" or temp_word == "#":
                    continue
                ans = self.parse_hashtag(temp_word)
            elif ans == "" and word[0] == '@':
                ans = self.remove_panctuation(word)
            elif ans == "" and word in self.list_percent:
                if idx > 0 and self.isfloat(array_text_space[idx - 1]):
                    ans = self.parse_percentage(array_text_space[idx - 1] + " " + word)
                    string_ans = string_ans[:len(string_ans) - 1 - len(ans)] + string_ans[
                                                                               len(string_ans) + len(word):] + " "
                else:
                    ans = word
            elif ans == "" and (
                    word.lstrip('-').isdigit() or self.isfloat(word.lstrip('-')) or self.isFraction(word.lstrip('-'))):
                ans = self.convert_str_to_number(array_text_space, idx)
            if ans == "":
                ans = self.remove_panctuation(word)
                if word.lower() in self.stop_words: continue
            #ans = word
            string_ans += self.add_to_dictionary(ans, string_ans_index)
            string_ans_index += len(word) + 1

        self.get_name_and_entities(entities_url, array_text_space)
        array_parsed = string_ans.split()
        return array_parsed,self.array_names_and_entities

    def separate_words_with_dots(self, array_text):
        new_text = ""
        length = range(len(array_text))
        for i in length:
            word = array_text[i]
            if '.' not in word:
                new_text += word + " "
                continue
            if "http" in word or "www" in word or "t.co" in word or self.isfloat(word):
                new_text += word + " "
                continue
            separate = ""

            separate = str(word).split('.')
            new_text += separate[0] + ". " + separate[1] + " "
        return new_text.lstrip().split(" ")

    def is_url(self, text):
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
        array_of_words = text.split(" ")
        ans = ""
        for word in array_of_words:
            ans += word + " "
            self.dictionary_index[word] = index
        if ans == "": return ""
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
            ans = re.sub(r"http\S+", "", ans)

            ans = "".join(ans).strip().split()
            ans_len = len(ans)
            if ans_len > 0:
                remove_www = ans[0].replace("www.", "")
                ans[0] = ans[0].replace(ans[0], remove_www)
                string_without_stopword = ""
                length = range(len(ans))
                for word, idx in zip(ans, length):
                    if word in self.stop_words or word.isnumeric():
                        continue
                    string_without_stopword += word + " "
                return string_without_stopword.lstrip()
            else:
                return ""

    def isdigit(self, word):
        if "0" <= word <= "9":
            return True
        return False

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
        if my_word != '' and not math.isnan(float(my_word)):
            number = float(my_word)
            number_numerize = self.convert_str_to_number_kmb(number)
            if idx + 1 < len(text_demo):
                token_next = text_demo[idx + 1].lower()
                number_to_input = str(number_numerize)
                if token_next == "billion" or token_next == "billions":
                    if 'K' in number_numerize or 'M' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        number_to_input = (number_to_input.translate({ord('M'): None}))
                        text_return.append(my_word)
                    else:
                        text_return.append(str(number_numerize + 'B'))
                    text_demo[idx + 1] = ""

                elif token_next == "million" or token_next == "millions":
                    if 'K' in number_numerize:
                        number_to_input = (number_to_input.translate({ord('K'): None}))
                        text_return.append(number_to_input + 'B')
                    else:
                        number_to_input = str(number_numerize)
                        text_return.append(number_to_input + 'M')
                    text_demo[idx + 1] = ""
                elif token_next == "thousand" or token_next == "thousands":
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

    def ignore_emojis(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        ans = emoji_pattern.sub(r'', text)
        return ans

    def is_ascii(self, s):
        ans = all(ord(c) < 128 or c == '…' or c == '’' or c == '³' or c == "¹⁹" for c in s)
        return ans

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
        # chars = set('.,:;!()[]{}?=+…$&')
        if re.match(r'[^@]+@[^@]+\.[^@]+', word): return word
        if "#" == word: return ""
        # if ('@' in word and word[0] != '@' and '.' in word):
        #     return word
        # if "gmail" in word or "hotmail" in word or "yahoo" in word: return word
        if word[-2:] == "'s" or word[-2:] == "’s" or word[-2:] == "`s": word = word.replace(word[-2:], "")
        smiles = [":)", ":(", ":-]", ":-)", ";)", ";-)", ":-(", ";(", ";-(", ":-P", ":P"]
        if word in smiles: return word
        # if ":)" == word or ":(" == word or ":-]" == word or ":-)" == word or ";)" == word or ";-)" == word or ":-(" == word or ";(" == word or ";-(" == word: return word
        # if "'s" in word: word = word.replace("'s", "")
        # elif "’s" in word: word = word.replace("’s", "")
        # elif "`s" in word: word = word.replace("`s", "")
        if "\n" in word: word = word.replace("\n", " ")
        if '#' in word and word[0] != '#': word = word.replace("#", "")
        if '@' in word and word[0] != '@': word = word.replace("@", "")

        word = word.replace("-", " ")
        word = re.sub(r'[€£€4️⃣“”‘⁦⁩‼⑥²⁸¹❶❷❽②⑦&$.,!?,…:;^"{}=+()⁰/[\[\]]', '', word)
        return word


    def get_name_and_entities(self, entities_url, array_text_space):
        text = ""
        regular_word = ""
        for corona_word in array_text_space:
            regular_word = corona_word
            corona_word = corona_word.lower()
            if corona_word in self.covid_list:
                corona_word = corona_word.upper()
                text += corona_word + " "
            else:
                text += regular_word + " "

        rx2 = re.compile(r'[A-Z][-a-zA-Z]+[1-9]*(?:\s+[A-Z][-a-zA-Z]+[1-9]*)*')
        text = ' '.join("" if i in entities_url else i for i in text.split())
        matches = rx2.findall(text)
        tokinzed_entity_new = set()
        tokinzed_entity_new.update([e for e in matches if len(e) > 1])

        for word in tokinzed_entity_new:
            if word.lower() not in self.stop_words:
                all_places = [m.start() for m in re.finditer(word, text)]
                self.array_names_and_entities[word] = all_places
        return tokinzed_entity_new

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
        entities_local_dict = {}
        array_url_parsed = []
        url = str(url)
        rt=False
        if "RT"  in full_text:
            rt=True
        if url != "{}" and "null" not in url:
            dict2 = eval(url)
            keys = dict2.keys()
            for key in keys:
                if dict2[key] != str("null") and "t.co" not in dict2[key]:
                    url_parsed = self.parse_url(dict2[key])
                    check = url_parsed.split()
                    for word in check:
                        array_url_parsed.append(word)
        tokenized_text,names_and_entities = self.parse_sentence(full_text, stemmer=False)
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        for term in array_url_parsed:
            if term in self.stop_words or term == 'http' or term == 'https' or term == 'www':
                continue
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        for term in names_and_entities.keys():
            if term in self.stop_words :
                continue
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict,rt, doc_length)
        return document
