# -*- coding: utf-8 -*-

import requests
import logging
from lxml.html.clean import Cleaner

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


def _get_html_2xx_only(url):
    """
    If the response code is not 2XX raise an requests exception
    """
    status_code = _ping(url)
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


def _ping(url):
    """ Return status code of a website by making a HEAD request """
    try:
        r = requests.head(url=url)
        return r.status_code
    except requests.ConnectionError as e:
        raise e
