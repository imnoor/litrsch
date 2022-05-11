from pattern.text.en import singularize

class SynDict:
    def __init__(self):
        self.dict={}
        self.populate()
    
    def replace(self,word):
        word = singularize(word)
        if word in self.dict:
            return self.dict[word]
        return word
    
    def populate(self):
        self.dict["ALGORITHMIC"] = "ALGORITHM"
        self.dict["ALGORITHM"] = "ALGORITHM"
        self.dict["ALGORITHMS"] = "ALGORITHM"
        self.dict["NATIONAL"] = "NATION"
        self.dict["EXPLANATIONS"] = "EXPLAINABLE"
        self.dict["SOCIETAL"] = "SOCIETY"
        self.dict["SOCIETAL"] = "SOCIETY"
        self.dict["ORGANIZATIONAL"] = "ORGANIZATION"
        self.dict["SOCIETAL"] = "SOCIETY"
        self.dict["ENABLED"] = "ENABLE"
        self.dict["COMPUTING"] = "COMPUTE"
        