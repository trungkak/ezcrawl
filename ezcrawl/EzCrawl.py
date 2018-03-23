# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 15

import lxml.html
from lxml import etree
import os
import re
from collections import defaultdict, Counter
from common import is_static

from network import get_pure_html
from tree import get_all_leaf_nodes, get_all_ancestors


class EzCrawl(object):

    def __init__(self, url):
        self._url = url
        self._prefix = self._find_prefix()

        self._root = self._construct_tree()
        self._tree = etree.ElementTree(self._root)

        self._leaf_nodes = []

    def get_root(self):
        return self._root

    def _find_prefix(self):
        """ Return domain name of a website """
        return os.path.dirname(self._url)

    def _construct_tree(self):
        """ Construct xml tree from html source """
        page_src = self._page_source()
        root = lxml.html.fromstring(page_src)
        return root

    def _page_source(self):
        return get_pure_html(self._url)

    def _simple_path(self, node):
        """ Ex: html/div[1]/div[3]/a -> html/div/div/a """
        return re.sub(r'\[[^\]]*\]', '', self._tree.getpath(node))

    def _find_data_items(self, threshold=2):
        """ Find data items (leaf nodes) with repetition over threshold"""
        get_all_leaf_nodes(self._root, self._leaf_nodes)
        ips = []
        p2i = defaultdict(list)

        for l_node in self._leaf_nodes:
            print(l_node.text_content())
            print(self._simple_path(l_node))
            if len(l_node.text_content().strip().split()) < threshold:
                continue
            tp = self._simple_path(l_node)
            ips.append(tp)
            p2i[tp].append(l_node)

        ips = [tp for tp in ips if len(p2i[tp]) > threshold]
        ips = list(set(ips))

        p2i = {ip: p2i[ip] for ip in ips}

        return ips, p2i

    def _find_candidate_records(self, ips, p2i):
        """ Find candidate records """
        t_counter = Counter()
        for ip in ips:
            for l_node in p2i[ip]:
                self._bu_count(ip, l_node, t_counter)
        ip2r = defaultdict(set)
        for ip in ips:
            for node in p2i[ip]:
                ancestors = get_all_ancestors(node)
                for ancestor in ancestors:
                    if t_counter[(ip, ancestor)] == 1 \
                            and t_counter[(ip, ancestor.getparent())] > 1:
                        ip2r[ip].add(ancestor)
        return ip2r

    def _group_by_path(self, nodes):
        """ Group records by its simple path """
        grp = defaultdict(list)
        for node in nodes:
            grp[self._simple_path(node)].append(node)
        return grp

    def identify_records(self, threshold=2):
        """ Select records that tend to be the main records """
        ips, p2i = self._find_data_items()

        ip2r = self._find_candidate_records(ips, p2i)

        cr = set()
        tps = defaultdict(list)
        for ip in ips:
            for rec in ip2r[ip]:
                cr.add(rec)
                tps[rec].append(ip)
        dr = []
        for rec in cr:
            if len(tps[rec]) >= threshold:
                dr.append(rec)

        grp = self._group_by_path(dr)
        _, records = max(grp.items(), key= lambda i: len(i[1]))

        return records

    def _bu_count(self, tp, node, counter):
        """ Count number of data items that a node has """
        counter[(tp, node)] += 1
        if node.getparent() != self._root:
            self._bu_count(tp, node.getparent(), counter)







