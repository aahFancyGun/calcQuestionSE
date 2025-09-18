from serpapi import GoogleSearch
import anthropic
import os
import requests

client_anthropic = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


class SearchObject:
    def __init__(self):
        self.params = None
        self.results = None
        self.link_list = []

    def set_params(self, query):
        print(query, flush=True)
        self.params = {
            "q": query,
            "api_key": "a2a1474b2e6ba99d36ae610c49bb60d13f3cc56025adf403882509320f517bcd"
        }

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

    def analyze_with_anthropic(self, html_content, prompt="analyze websites to find interesting and challenging calculus questions, only choose questions that go beyond a plug and chug level. Return your answer in a list seperated by '&', do not include a number at the beginning of a list entry and do not create new lines between entries. Do not generate any additional dialgoue beyond the questions"):
        try:
            message = client_anthropic.messages.create(
                model="claude-3-7-sonnet-20250219",  
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
        self.search()
        links = self.get_link_list()
        compiledQuestions = []
        
        for link in links[:1]:
            print(f"Fetching and analyzing: {link}")
            html = self.get_website_structure(link)
            print(html)
            
            if html:
                result = self.analyze_with_anthropic(html)
                if(result != None):

                    result = result.split('&')
                    print(result)
                    compiledQuestions.append({
                        "link": link,
                        "questions": result
                    })
                    
        return compiledQuestions
    
