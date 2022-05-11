import sys
sys.path.append('../src/')

from src.bib_processor import BiBProcessor

processor = BiBProcessor('bibtex_collection.bib')
processor.preparser()
tags = processor.get_tags() 
      
filter_list = ["ARTIFICIAL","INTELLIGENCE", "AI", "MACHINE LEARNING","AUTOMATION", "AUTONOMOUS","COGNITIVE","(AI)"]
filename = "noise.txt"
noise_list = []
with open(filename) as f:
    for line in f:
        noise_list +=line.replace("\n","").split(",")
noise_set = set(noise_list)

for tag in tags:
    print(tag)
    processor.filter_tag([tag])
    theme_data = processor.get_themes(filter_list,50, noise_list=noise_set)
    print(theme_data['common'])

