import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

class Spam:
    def __init__(self):
        self.all_urls=[]

    def get_total_page_number(self):
        soup = BeautifulSoup(requests.get("https://www.axa.com/_api/search?query=||&locale=en").content, "html.parser")

        site_json = json.loads(soup.text)
        self.total_page_number = site_json['pagination']['pageCount']

    def get_all_urls(self):
        # range from first page to last page
        #for x in range(1,self.total_page_number+1):
        for x in range(1,4):
            soup = BeautifulSoup(requests.get(f"https://www.axa.com/_api/search?query=||&locale=en&page={x}").content, "html.parser")
            site_json = json.loads(soup.text)
            spam=[x['link'] for x in site_json['items']]
            self.all_urls.extend(spam)
            print(f"-------------------{x}----------------")
            time.sleep(3) #to avoid F5 error

        self.all_urls = set(self.all_urls)
        self.all_urls = sorted(self.all_urls)

    def set_prod_url(self):
        self.all_urls = ["https://www.axa.com" + url for url in self.all_urls]

class Ham:
    def __init__(self,urls):
        self.urls = urls[:]
        self.eclaire = dict()

    def scrap(self):
        for url in self.urls:
            try:
                print(url)
                soup = BeautifulSoup(requests.get(url).content, "html.parser")
                if soup.find(attrs={'role':"main"}):
                    acer=soup.find(attrs={'role':"main"})
                    ace = [str(x) for x in acer]
                    self.eclaire[url]=ace
                elif soup.find(attrs={'id':"__next"}):
                    acer=soup.find(attrs={'id':"__next"})
                    ace = [str(x) for x in acer]
                    self.eclaire[url]=ace
                    print('next page : ' + url )
            except:
                print('excepted url : '+ url)

    def dump_to_json(self):
        path = Path.cwd().joinpath("eclaire.json")
        with open(path, "w") as f:
            json.dump(self.eclaire, f)

if __name__=="__main__":
    a=Spam()
    a.get_total_page_number()
    a.get_all_urls()
    print(len(a.all_urls))
    print(a.all_urls)
    a.set_prod_url()
    print(a.all_urls)

    print("h--------am-----------")

    h=Ham(a.all_urls)
    print(h.urls)
    h.scrap()
    h.dump_to_json()
