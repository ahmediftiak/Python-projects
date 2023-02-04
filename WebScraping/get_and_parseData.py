import requests
from bs4 import BeautifulSoup

## This class works as a generator that sequentially 
## returns all the records (of tag div and class record)
## on the result as a BeautifulSoup's Tag. 
## This method seamlessly jump to next page when reaching the end of the current page,
## and only exit when there is no more result.

class SIScraper():
    def __init__(self):
        self.session = requests.Session()
        self.prefix = ''
        
    def retrieveRecords(self, url: str): #-> Generator[bs4.Tag]
        self.prefix = url[:url.rfind('?')+1]  #The url prefix
        for soup in self.getPages(url): 
            for record in soup.find_all('div', {'class': 'record'}):
                yield record

    def getPages(self, url): #returns the page contains and updates the url to next page
      while url:
        page = self.session.get(url)
        soup = BeautifulSoup(page.content)
        yield soup
        url = self.nextPage(soup)
      
    def nextPage(self, soup): #gets the link for next page
        for a in soup.select('div.pagination a'):
            if a.text.strip()=='next':
                return f'{self.prefix}{a["href"]}'
        return None

# disclaimer: this code is based on class code 

if __name__ == "__main__":
    URL = 'https://collections.si.edu/search/results.htm?date.slider=&q=&dsort=&fq=object_type%3A%22Outdoor+sculpture%22&fq=data_source%3A%22Art+Inventories+Catalog%2C+Smithsonian+American+Art+Museum%22&fq=date:%221400s%22'
    scraper = SIScraper()
    records = scraper.retrieveRecords(URL)
    for i,record in enumerate(records, 1):
        print(i, record.find('h2').text)