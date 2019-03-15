from bs4 import BeautifulSoup
import requests
import re
import sys

class Google:
    @classmethod
    def search(self, search):
        page = requests.get("http://www.google.com/search?q=site%3Aedu+OR+site%3Aorg+"+search)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        urls = [re.split(":(?=http)",link["href"].replace("/url?q=",""))[0] for link in links]
        return [url for url in urls if 'webcache' not in url]

def get_text_bs(html):
    tree = BeautifulSoup(html, 'lxml')

    body = tree.body
    if body is None:
        return None

    for tag in body.select('script'):
        tag.decompose()
    for tag in body.select('style'):
        tag.decompose()

    text = body.get_text(separator='\n')
    return text

def getContent(searchQuery="Booster") :
    search_links = Google.search(searchQuery)

    plaintext = []    
    
    for link in search_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html5lib")
        
        text = get_text_bs(str(soup))
        plaintext.append(text)
        
    return plaintext




if __name__=="__main__":
    query = ""
    defaultQuery = "word+vectorization"
    for i in range(1,len(sys.argv)):
        query = query + sys.argv[i] + " "
    
    query = query.strip() if len(query)>1 else defaultQuery
    getContent(query)
    