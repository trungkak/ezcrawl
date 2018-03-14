from EzCrawl import EzCrawl

ez = EzCrawl('https://www.ted.com/talks?language=vi')

if __name__ == '__main__':
    crs = ez.find_candidate_records()
    for key in list(crs.keys()):
        print(len(crs[key]))

