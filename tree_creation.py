import pandas as pd
import numpy as np

class Node:
    def __init__(self,data):
        self.data = data
        self.children = []