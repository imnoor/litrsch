from bib_processor import BiBProcessor
import ml_lit

processor = BiBProcessor('../bibtex_collection.bib')
processor.filter_abstract()

tags = ['Enterprise Architecture']

processor.filter_tag(tags)

filter_list = ["ARTIFICIAL","INTELLIGENCE", "AI", "MACHINE LEARNING","AUTOMATION", "AUTONOMOUS","COGNITIVE","(AI)"]
noise_list = ["RESEARCH", "NEW","STUDY","INFORMATION","CHANGE","TIME","BASED","LEVEL","ERA","MAIN", "INTRODUCTION","USE", "NEED",
             "AIM", "EFFORTS","CONCEPTS","BIG","BOLD","BASIS","HELP", "PRACTICES", "CONTEXT","CREATED","EANBLE", "CASE","EVENTS","CREATION", "PROVIDED", "HIGHLY",
             "INCLUDING", "ENABLED","ENABLE", "LEVELS", "LASTLY","UNITS", "ENHANCED", "BEST","LASTLY","DRAWN","OBJECTIVE","THESIS","KNOWN"]

theme_data = processor.get_themes(filter_list,50, noise_list=noise_list)
print(theme_data['common'])