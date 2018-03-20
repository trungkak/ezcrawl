from EzCrawl import EzCrawl
from extractor import get_record_name
from network import ping
import csv


cate_queue = {
    'dien-thoai-may-tinh-bang': ['https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=mega-menu'],

    'tivi-thiet-bi-nghe-nhin': ['https://tiki.vn/tivi-thiet-bi-nghe-nhin/c4221?src=mega-menu'],

    'thiet-bi-kts-phu-kien-so': ['https://tiki.vn/thiet-bi-kts-phu-kien-so/c1815?src=mega-menu'],

    'laptop-may-vi-tinh': ['https://tiki.vn/laptop-may-vi-tinh/c1846?src=mega-menu'],

    'may-anh': ['https://tiki.vn/may-anh/c1801?src=mega-menu'],

    'dien-gia-dung': ['https://tiki.vn/dien-gia-dung/c1882?src=mega-menu'],

    'nha-cua-doi-song': ['https://tiki.vn/nha-cua-doi-song/c1883?src=mega-menu'],

    'bach-hoa-online': ['https://tiki.vn/thuc-pham-kho/c4393?order=newest',
                        'https://tiki.vn/do-uong/c4394?order=newest',
                        'https://tiki.vn/cham-soc-ve-sinh-nha-cua/c4386?order=newest',
                        'https://tiki.vn/cham-soc-co-the/c4390?order=newest',
                        'https://tiki.vn/cham-soc-toc/c4392?order=newest'],

    'me-be': ['https://tiki.vn/me-be/c2549?src=mega-menu'],

    'lam-dep-suc-khoe': ['https://tiki.vn/trang-diem/c1584?order=newest',
                         'https://tiki.vn/cham-soc-da-mat/c1582?order=newest',
                         'https://tiki.vn/cham-soc-toc-da-dau/c1591?order=newest',
                         'https://tiki.vn/cham-soc-co-the/c1592?order=newest',
                         'https://tiki.vn/cham-soc-ca-nhan/c1594?order=newest',
                         'https://tiki.vn/nuoc-hoa/c1595?order=newest'],

    'thoi-trang': ['https://tiki.vn/thoi-trang-nam/c915',
                    'https://tiki.vn/thoi-trang-nu/c931'],

    'the-thao': ['https://tiki.vn/the-thao/c1975?src=mega-menu'],

    'xe-may-oto-xe-dap': ['https://tiki.vn/o-to-xe-may-xe-dap/c8594?src=mega-menu'],

    'nha-sach-tiki': ['https://tiki.vn/ebook/c5290',
                      'https://tiki.vn/sach-truyen-tieng-viet',
                      'https://tiki.vn/sach-tieng-anh/c320?order=top_seller',
                      'https://tiki.vn/van-phong-pham-qua-luu-niem/c7741'],

    'voucher-dich-vu': ['https://tiki.vn/voucher-dich-vu/c11312?src=mega-menu'],
}


if __name__ == '__main__':

    csv_file = open('output.csv', 'w')
    writer = csv.writer(csv_file, delimiter=',')

    for cate in list(cate_queue.keys()):

        for url in cate_queue[cate]:
            i = 1
            visited_urls = set()
            full_url = url + '&page=' + str(i)
            while ping(full_url) == 200:

                print(url + '&page=' + str(i))

                ez = EzCrawl(full_url)

                records = ez.identify_records()

                print(len(records))

                if len(records) != 23:
                    break

                for record in records:
                    name = get_record_name(record)

                    writer.writerow([name, cate])
                i += 1

    csv_file.close()






