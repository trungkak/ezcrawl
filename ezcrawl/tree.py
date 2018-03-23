# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 15


def get_all_leaf_nodes(node, leaf_nodes):
    """ Return all leaf nodes from the current node in a etree """
    if node.getchildren():
        for child in node:
            get_all_leaf_nodes(child, leaf_nodes)
    else:
        leaf_nodes.append(node)


def get_all_ancestors(node):
    """ Return all ancestor nodes from a node """
    return node.iterancestors()



