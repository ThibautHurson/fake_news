import pandas as pd
import numpy as np

import twint


class Node:
    def __init__(self, data, children=None):
        self.data = data
        if children: self.children = children
        else: self.children = []


    def add_children(self,child):
        assert(child)
        self.children.append(child)


root = Node(1)
root.add_children(None)
print(root.data)
print(root.children)

# # Configure
# c = twint.Config()
# c.Username = "realDonaldTrump"
# c.Search = "great"

# # Run
# twint.run.Search(c)

# users = [
#     'shakira',
#     'KimKardashian',
#     'rihanna',
#     'jtimberlake',
#     'KingJames',
#     'neymarjr',
# ]
