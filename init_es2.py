import os, sys, pdb
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

"""
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)
"""
# plt1 ========================================================================
#aPs = np.array([1, 2, 3, 4, 5, 6, 7, 8])
#cPs = np.array([1, 2, 3, 4]) #dummy while don't have child data
#hthreshold = 3000 #ms

# plt2 ========================================================================
aPs = np.array([9, 10, 11, 12, 13, 14, 15, 16, 17])
cPs = np.array([1, 2, 3, 4])
dPath = '../experiment/output-from-test-rooms'
otherPath1 = '../designMaterials'
paths = [dPath, otherPath1]
cartoonNames = ['rugrats', 'busyWorld']
