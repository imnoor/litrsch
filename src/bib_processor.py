from pybtex.database.input import bibtex
from collections import Counter
from string import punctuation
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from syndict import SynDict
import matplotlib.pyplot as plt
import itertools
import spacy


class BiBProcessor:
    def __init__(self, bib_file):
        self.bib_file = bib_file
        self.nlp = spacy.load('en_core_web_sm')
        parser = bibtex.Parser(encoding='UTF-8')
        self.bib_data = parser.parse_file(self.bib_file)
        self.preprocessed = []
        self.filtered = []
        self.tags = []

    def size(self):
        return len(self.filtered)
      
    def preparser(self):
        for item in self.bib_data.entries:
            if 'abstract' in self.bib_data.entries[item].fields:
                self.preprocessed.append(self.bib_data.entries[item])
                if 'mendeley-tags' in self.bib_data.entries[item].fields and self.bib_data.entries[item].fields['mendeley-tags']:
                    self.tags +=self.bib_data.entries[item].fields['mendeley-tags'].split(",")
                    
        self.tags= set(self.tags)
        
    def get_tags(self):
        return self.tags
        
    def filter_tag(self,tags =[]):
        tagged = []
        self.filtered = self.preprocessed.copy()
        for item in self.filtered:
            if 'mendeley-tags' in item.fields:
                if len(tags) == 0 :
                    tagged.append(item)
                else:
                    set_A = set(item.fields['mendeley-tags'].split(","))
                    set_B = set(tags)
                    if ( not set_A.intersection(set_B) == set()) :
                        tagged.append(item)
                        
        self.filtered = tagged
        
    def get_themes(self,filter_list=[], top=10, noise_list=[]):       
        words = []
        for entry in self.filtered:
            abstract = entry.fields['abstract'].upper()
            words += self.sanitize(abstract, filter_list=filter_list,noise_list=noise_list)
        words = itertools.chain(*words)
        counter_data = Counter(list(words))
        common_words = counter_data.most_common(top)
        return {'common' : common_words, 'data' : counter_data,'records': len(self.filtered)}
    
    def get_aggregate_themes(self, keywords=[],top=10, noise_list=[] ):
        words = []
        for entry in self.filtered:
            abstract = entry.fields['abstract'].upper()
            words += self.sanitize(abstract, keywords=keywords, filter_list=[],noise_list=noise_list)
        #words = itertools.chain(*words)
        #counter_data = Counter(list(words))
        #print(words)
        counter_data = Counter(words)
        common_words = counter_data.most_common(top)
        return {'common' : common_words, 'data' : counter_data,'records': len(self.filtered)}
    
    def sanitize(self,text, keywords=[], filter_list=[], noise_list=[]):
        words =[]
        has_key = [ele for ele in filter_list if(ele in text)]
        edit_string_as_list = text.split()
        first_filter = [word for word in edit_string_as_list if word not in filter_list]
        noise_filtered = [word for word in first_filter if word not in noise_list]
        if len(keywords) > 0: 
            keyword_filtered= [word for word in noise_filtered if word in keywords]
            words = keyword_filtered
        else:
            keyword_filtered= noise_filtered
            text = ' '.join(keyword_filtered)
            text = self.normalize_textual_information(text)
            text = self.apply_semantic_tranform(text)
            if has_key:
                p = self.nlp(text)
                words.append([t.text for t in p if not t.is_stop and not t.is_punct])
        return words
    
    def normalize_textual_information(self, text):
        # split text into tokens by white space
        token = text.split()

        # remove punctuation from each token
        table = str.maketrans('', '', punctuation)
        token = [word.translate(table) for word in token]
        # remove any tokens that are not alphabetic
        token = [word.lower() for word in token if word.isalpha()]

        # filter out English stop words
        stop_words = set(stopwords.words('english'))

        token = [word for word in token if word not in stop_words]

        # filter out any short tokens
        token = [word for word in token if len(word) > 1]
        return ' '.join(token)
    
    def apply_semantic_tranform(self,text):
        token = text.split()
        syn = SynDict()
        token = [ syn.replace(word) for word in token ]
        return ' '.join(token)
    