from EzCrawl import EzCrawl
from extractor import _get_inner_html
from network import ping
import csv


base_url = 'http://www.funtrivia.com/en/Sports/FIFA-World-Cup-627.html'


if __name__ == '__main__':

    ez = EzCrawl(base_url)

    records = ez.identify_records()

    print(len(records))

    for record in records:
        print(_get_inner_html(record))







