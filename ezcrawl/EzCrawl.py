# -*- coding: utf-8 -*-

import lxml.html
from lxml import etree
import os
import re

from network import get_pure_html
from tree import get_all_leaf_nodes


class EzCrawl:

    def __init__(self, url):
        self._url = url
        self._prefix = self._find_prefix()

        self._root = self._construct_tree()
        self._tree = etree.ElementTree(self._root)

        self._leaf_nodes = []
        get_all_leaf_nodes(self._root, self._leaf_nodes)

    def _find_prefix(self):
        return os.path.dirname(self._url)

    def _construct_tree(self):
        page_src = self._page_source()
        root = lxml.html.fromstring(page_src)
        return root

    def _page_source(self):
        return get_pure_html(self._url)

    def _construct_items(self):
        paths = [self._simple_path(node) for node in self._leaf_nodes]
        items = [node for node in self._leaf_nodes
                 if paths.count(self._simple_path(node)) >= 5]
        return items

    def _simple_path(self, node):
        return re.sub(r'\[[^\]]*\]', '', self._tree.getpath(node))



