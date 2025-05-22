from serpapi import GoogleSearch
import anthropic
import os
import requests
import json


os.environ["ANTHROPIC_API_KEY"] = "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"
client_anthropic = anthropic.Anthropic()

class SearchObject:
    toadd = {}
    thisthing={}
    found = 0
    betterdata = {}
    
    def __init__(self):
        self.params = None
        self.results = None
        self.link_list = []

    def set_params(self, query):
        global toadd
        global thisthing
        global found
        global betterdata
        print(query, flush=True)
        self.params = {
            "q": query,
            "api_key": "a2a1474b2e6ba99d36ae610c49bb60d13f3cc56025adf403882509320f517bcd"
        }
        found = 0
        if os.path.exists('temporary.txt'):
            with open('temporary.txt','r') as f:
                datawhatever = f.read()
            betterdata = json.loads(datawhatever)
            for key in betterdata.keys():
                if(key==query & found==0):
                    compiledInfo=betterdata[key]
                    
                    thisthing = betterdata[key]
                    found = 1
        else:
            
            compiledInfo = self.compile_info()
            found=1
        if(found==0):  
            compiledInfo = self.compile_info()
        



    

    def search(self):
        search = GoogleSearch(self.params)
        to_parse = search.get_dict().get("organic_results", [])

        self.link_list = [result.get("link") for result in to_parse if result.get("link")]

    def get_link_list(self):
        return self.link_list

    def get_website_structure(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text[:5000]  
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def analyze_with_anthropic(self, html_content, prompt="analyze websites to find interesting and challenging calculus questions. Return your answer in a list seperated by '&', do not include a number at the beginning of a list entry and do not create new lines between entries. Do not generate any additional dialgoue beyond the questions"):
        try:
            message = client_anthropic.messages.create(
                model="claude-3-opus-20240229",  
                max_tokens=500,
                temperature=0,
                system="analyze websites to find interesting and challenging calculus questions. Return your answer in a list seperated by '&', do not include a number at the beginning of a list entry and do not create new lines between entries. Do not generate any additional dialgoue beyond the questions",
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n{html_content}"
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic error: {e}")
            return None

    def compile_info(self): 
        global toadd
        global found
        global betterdata
        global thisthing
        if(found==1):
            return thisthing
        
        self.search()
        links = self.get_link_list()
        count = 0
        compiledQuestions = []
        jsonquestions = {}
        for link in links:
            if(count > 3):
                break
            print(f"Fetching and analyzing: {link}")
            html = self.get_website_structure(link)
            print(html)
            jsonquestions[count] = {}
            if html:
                result = self.analyze_with_anthropic(html)
                if(result != None):
                    result = result.split('&')
                    print(result)
                    compiledQuestions.append({
                        "link": link,
                        "questions": result
                    }) #WAIT THATS LITERALLY ALMOST JSON FORMAT LOL
                    jsonquestions[count]["link"]=link
                    jsonquestions[count]["questions"]=result
                # sorry guys, a lil fix here but we gotta get more credits
                # oh yeah can one of you make a thing that else's the result and says HEY WE OUTTA CREDITS ty.
            count = count + 1
        toadd = jsonquestions
        betterdata[self.params["q"]]=toadd
        with open("temporary.txt","w") as f:
            jonsified = json.dumps(betterdata)
            f.write(jonsified)
        return compiledQuestions
    
