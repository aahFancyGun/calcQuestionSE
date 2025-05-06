from serpapi import GoogleSearch
import anthropic
import os

os.environ["ANTHROPIC_API_KEY"] = "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"
client_anthropic = anthropic.Anthropic()

class searchObject:
    def __init__(self) :
        print('asdf')
        self.params = None
        self.search = None
        self.linkList = None

    def setParams(self, query) :
        self.params = {
            "q": f"{query}",
            "api_key": "a2a1474b2e6ba99d36ae610c49bb60d13f3cc56025adf403882509320f517bcd"
        }
    
    def getParams(self) :
        return self.params
    
    def search(self) :
        self.search = GoogleSearch(self.params)

        toParse = self.search["organic_results"]

        for idx, webInfo in enumerate(toParse):
            self.linkList.append(webInfo["link"])
    
    def getSearch(self) :
        return self.search
    
    def getLinkList(self) :
        return self.linkList
    
    def analyze(self) :
        #will do later :p
    




