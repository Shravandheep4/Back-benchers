from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import re

class Google:
    @classmethod
    def search(self, search):
        page = requests.get("http://www.google.de/search?q="+search)
        soup = BeautifulSoup(page.content)
        links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        urls = [re.split(":(?=http)",link["href"].replace("/url?q=",""))[0] for link in links]
        return [url for url in urls if 'webcache' not in url]
 
search_links = Google.search("maching learning")

source = []    