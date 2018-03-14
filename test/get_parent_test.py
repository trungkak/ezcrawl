from tree import get_all_ancestors
from EzCrawl import EzCrawl

ez = EzCrawl('https://www.ted.com/talks?language=vi')
root = ez.get_root()
child = root.getchildren()[0].getchildren()[0]

ancestors = get_all_ancestors(child)
for ancestor in ancestors:
    print(ancestor.xpath())