# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 15

import requests
import logging
from lxml.html.clean import Cleaner
import random
import time

__name__ = 'EzCrawl'

log = logging.getLogger(__name__)


def get_pure_html(url):
    """ Return pure html from the url """
    try:
        body = get_html(url)
        cleaner = Cleaner()
        doc = cleaner.clean_html(body)
        return doc
    except Exception as e:
        log.error('get_html() error. %s on URL: %s' % (e, url))
        return ''


def get_html(url):
    """ Return source html from the url """
    try:
        return _get_html_2xx_only(url)
    except Exception as e:
        raise e


def _by_pass_get_html(url):
    """ In case you are blocked """
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                    "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                    "134.213.29.202:4444"]

    proxies = {'https': random.choice(proxies_list)}
    time.sleep(0.5 * random.random())
    r = requests.get(url, headers, proxies=proxies)
    page_html = r.content
    return page_html


def _get_html_2xx_only(url):
    """
    If the response code is not 2XX raise an requests exception
    """
    status_code = ping(url)
    if status_code != -1:
        if status_code in range(200, 400):
            try:
                r = requests.get(url)
                return r.text

            except requests.ConnectionError as e:
                raise e
        else:
            print('Status code is not 2XX, return empty string')
            return ''
    else:
        raise requests.ConnectionError


def ping(url):
    """ Return status code of a website by making a HEAD request """
    try:
        r = requests.head(url=url)
        return r.status_code
    except requests.ConnectionError as e:
        raise e
