import json
from get_and_parseData import SIScraper


class SIScraperJson(SIScraper):
    def __init__(self):
        super().__init__()
        self.data = {}


    def retrieveRecordsAsJson(self, url): 
        yield from map(self.toJson, self.retrieveRecords(url))

## the toJson method that transforms each record Tag returned by retrieveRecords to a JSON string
    def toJson(self, record):

        # a dict of strings that store the title of the record (the text of the h2 tag)
        self.data['Label'] = record.find('h2').text 

        # Key/value pairs are extracted from the dl tag of the record, 
        # where each key is the text of the dt tag, and each value is a list of all dd tag.

        for dl in record.find_all('dl'):
            dt = dl.find('dt')
            key = dt.text.strip(':')
            value = []

            for dd in dl.find_all('dd'):
                values = dd.text.replace('\xa0 Search this', '')
                value.append(values.strip())
              
            self.data[key] = value

        return json.dumps(self.data)

if __name__ == "__main__":
    URL = 'https://collections.si.edu/search/results.htm?date.slider=&q=&dsort=&fq=object_type%3A%22Outdoor+sculpture%22&fq=data_source%3A%22Art+Inventories+Catalog%2C+Smithsonian+American+Art+Museum%22&fq=date:%221400s%22'
    scraper = SIScraperJson()
    records = scraper.retrieveRecordsAsJson(URL)

    print('\n>> The FIRST record')
    display(next(records))

    print('\n>> The LAST record')
    display(max(enumerate(records))[1])