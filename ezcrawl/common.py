# -*- coding: utf-8 -*-
# Author: Trung Le Hoang <le.hg.trung@gmail.com>, created on Wed, Mar 21


import re


def is_static(node):
    """
        Ignore elements containing static component properties
        such as: "nav", "histogram", ..
    """
    patterns_static = [".*[Nn]av.*", ".*[Hh]istogram.*"]
    node_class = node.get('class')
    if node_class:
        for pattern in patterns_static:
            if re.match(pattern, node_class):
                return True
    children = node.getchildren() or []
    for child in children:
        child_class = child.get('class')
        if not child_class:
            continue
        for pattern in patterns_static:
            if re.match(pattern, child_class):
                return True
    return False
