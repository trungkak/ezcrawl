# -*- coding: utf-8 -*-

import lxml.html
from lxml import etree
import os
import re
from collections import defaultdict, Counter

from network import get_pure_html
from tree import get_all_leaf_nodes, get_all_ancestors


class EzCrawl(object):

    def __init__(self, url):
        self._url = url
        self._prefix = self._find_prefix()

        self._root = self._construct_tree()
        self._tree = etree.ElementTree(self._root)

        self._leaf_nodes = []
        # get_all_leaf_nodes(self._root, self._leaf_nodes)

    def get_root(self):
        return self._root

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

    def _find_data_items(self, threshold=3):
        get_all_leaf_nodes(self._root, self._leaf_nodes)
        tree_paths = []
        path_node_map = defaultdict(list)

        for l_node in self._leaf_nodes:
            # tp = self._tree.getpath(l_node)
            tp = self._simple_path(l_node)
            tree_paths.append(tp)
            path_node_map[tp].append(l_node)

        tree_paths = [tp for tp in tree_paths if len(path_node_map[tp]) > threshold]
        tree_paths = list(set(tree_paths))

        path_node_map = {tree_path: path_node_map[tree_path] for tree_path in tree_paths}

        return tree_paths, path_node_map

    def find_candidate_records(self):
        tree_paths, path_node_map = self._find_data_items()
        t_counter = Counter()
        for tp in tree_paths:
            for l_node in path_node_map[tp]:
                self._bu_count(tp, l_node, t_counter)
        cr = defaultdict(list)
        for tp in tree_paths:
            for node in path_node_map[tp]:
                ancestors = get_all_ancestors(node)
                for ancestor in ancestors:
                    if t_counter[(tp, ancestor)] == 1 \
                            and t_counter[(tp, ancestor.getparent())] > 1:
                        cr[tp].append(node)
        return cr

    def _bu_count(self, tp, node, counter):
        counter[(tp, node)] += 1
        if node.getparent() != self._root:
            self._bu_count(tp, node.getparent(), counter)





