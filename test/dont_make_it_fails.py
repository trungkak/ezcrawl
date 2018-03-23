#
# IMPORTANT: Always make sure this test would always works before commit anything new
#


from network import ping
from EzCrawl import EzCrawl

if __name__ == '__main__':
    url = 'https://tiki.vn/sach-tieng-anh/c320?order=top_seller&page=2'
    ez = EzCrawl(url)
    print(ping(url))
    records = ez.identify_records()
    assert len(records) == 23
