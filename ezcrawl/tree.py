# -*- coding: utf-8 -*-

from lxml import etree


def get_all_leaf_nodes(node, leaf_nodes):
    """ Get all leaf nodes from the current node in a etree """
    if node.get_children():
        for child in node:
            get_all_leaf_nodes(child, leaf_nodes)
    else:
        leaf_nodes.append(node)