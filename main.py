import sys
sys.path.append('../src/')

from bib_processor import BiBProcessor
import ml_lit

def load_list(filename):
    ret_list = []
    with open(filename) as f:
        for line in f:
            line=line.upper()
            ret_list +=line.replace("\n","").split(",")
    return ret_list

processor = BiBProcessor('bibtex_collection.bib')
processor.preparser()
tags = processor.get_tags() 
      
filter_list = ["ARTIFICIAL","INTELLIGENCE", "AI", "MACHINE LEARNING","AUTOMATION", "AUTONOMOUS","COGNITIVE","(AI)"]
noisefile = "noise.txt"
keysfile = "keywords.txt"
noise_list = load_list(noisefile)
keys_list= load_list(keysfile)

noise_set = set(noise_list)

processor.filter_tag([])
theme_data = processor.get_aggregate_themes( keywords=keys_list,top=67, noise_list=noise_list )
print(theme_data['common'])    

#for tag in tags:
    #processor.filter_tag([tag])
    #theme_data = processor.get_themes(filter_list,50, noise_list=noise_set)   
    #print(tag + " Records " + str(theme_data['records']))