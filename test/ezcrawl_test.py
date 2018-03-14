from EzCrawl import EzCrawl
from pprint import pprint

ez = EzCrawl('https://tiki.vn/tivi/c5015/lg?src=mega-menu')

if __name__ == '__main__':
    dg = ez.identify_records()
    pprint(dg)
