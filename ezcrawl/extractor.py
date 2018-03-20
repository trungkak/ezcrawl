# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 15

from lxml import etree
from bs4 import BeautifulSoup


def _get_inner_html(node):
    return etree.tostring(node, encoding='unicode')


def get_record_name(node):
    inner_html = _get_inner_html(node)
    soup = BeautifulSoup(inner_html, 'lxml')
    title = soup.find('a')['title']
    return title

