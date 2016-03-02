__author__ = 'marcusmorgenstern'
__mail__ = ''

import os


def mkdir(path):
    if os.path.exists(path):
        return
    os.makedirs(path)
