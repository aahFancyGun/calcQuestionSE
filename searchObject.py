from serpapi import GoogleSearch
import anthropic
import os
import requests

os.environ["ANTHROPIC_API_KEY"] = "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"
client_anthropic = anthropic.Anthropic()

class SearchObject:
    def __init__(self):
        self.params = None
        self.results = None
        self.link_list = []

    def set_params(self, query):
        self.params = {
            "q": query,
            "api_key": "a2a1474b2e6ba99d36ae610c49bb60d13f3cc56025adf403882509320f517bcd"
        }
    

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

    def analyze_with_anthropic(self, html_content, prompt="analyze websites to find interesting and challenging calculus questions. Return your answer in a list seperated by commas, do not include a number at the beginning of a list entry and do not create new lines between entries. Do not generate any additional dialgoue beyond the questions"):
        try:
            message = client_anthropic.messages.create(
                model="claude-3-opus-20240229",  
                max_tokens=500,
                temperature=0,
                system="analyze websites to find interesting and challenging calculus questions. Return your answer in a list seperated by commas, do not include a number at the beginning of a list entry and do not create new lines between entries. Do not generate any additional dialgoue beyond the questions",
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


if __name__ == "__main__":
    so = SearchObject()
    so.set_params("calculus") 
    so.search()

    links = so.get_link_list()
    for link in links:
        print(f"Fetching and analyzing: {link}")
        html = so.get_website_structure(link)
        if html:
            result = so.analyze_with_anthropic(html)
            result = result.split(',')
            print(result)
            print(link)