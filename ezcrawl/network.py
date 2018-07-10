# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 15

import requests
import logging
from lxml.html.clean import Cleaner
import random
import time
from fake_useragent import UserAgent


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
        # return _get_html_2xx_only(url)
        return _by_pass_get_html(url)
    except Exception as e:
        raise e


def _by_pass_get_html(url):
    """ In case you are blocked """

    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    print(header)

    time.sleep(0.5 * random.random())
    r = requests.get(url, headers=header)
    page_html = r.text
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