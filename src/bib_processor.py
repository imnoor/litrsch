from pybtex.database.input import bibtex
from collections import Counter
import matplotlib.pyplot as plt
import itertools
import spacy

class BiBProcessor:
    def __init__(self, bib_file):
        self.bib_file = bib_file
        self.nlp = spacy.load('en_core_web_sm')
        parser = bibtex.Parser(encoding='UTF-8')
        self.bib_data = parser.parse_file(self.bib_file)
        self.filtered = []

    def size(self):
        return len(self.filtered)
      
    def filter_abstract(self):
        for entry in self.bib_data.entries:
            if 'abstract' in self.bib_data.entries[entry].fields:
                self.filtered.append(self.bib_data.entries[entry])

    def filter_tag(self,tags =[]):
        tagged = []
        for item in self.filtered:
            if 'mendeley-tags' in item.fields:
                set_A = set(item.fields['mendeley-tags'].split(","))
                set_B = set(tags)
                if ( not set_A.intersection(set_B) == set()) :
                    tagged.append(item)
        self.filtered = tagged
        
    def get_themes(self,filter_list=[], top=10, noise_list=[]):       
        words = []
        for entry in self.filtered:
            abstract = entry.fields['abstract'].upper()
            has_key = [ele for ele in filter_list if(ele in abstract)]
            edit_string_as_list = abstract.split()
            first_filter = [word for word in edit_string_as_list if word not in filter_list]
            noise_filtered = [word for word in first_filter if word not in noise_list]
            abstract = ' '.join(noise_filtered)
            if has_key:
                p = self.nlp(abstract)
                words.append([t.text for t in p if not t.is_stop and not t.is_punct])
                
        words = itertools.chain(*words)
        counter_data = Counter(list(words))
        common_words = counter_data.most_common(top)
        return {'common' : common_words, 'data' : counter_data}
    