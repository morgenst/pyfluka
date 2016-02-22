__author__ = 'marcusmorgenstern'
__mail__ = ''

import os

def mkdir(path):
    if not os.path.exists(path):
        return
    os.path.makedirs(path)