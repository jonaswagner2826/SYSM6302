# -*- coding: utf-8 -*-
"""
Created on Tue May  4 19:38:33 2021

@author: Jonas
"""

# This script does specific calculations to generate degree distributions 
# and other basic things

runFromScratch = True
generateNewGraphs = True

if runFromScratch:

    import numpy as np
    import networkx as nx
    import requests
    import collections
    import matplotlib.pyplot as plt
    
    # Module with functions for accessing TBA database
    import TBA_database_access as tba
    
    # TBA_Network Class Import
    from TBA_Network_Analysis import TBA_Network
    import TBA_Network_Analysis as tba_na
    
    # Debuging tools
    import time
    import pandas as pd


if generateNewGraphs:
    year_network = False
    event_network = True
    
    year = '2015'
    event = '2015wimi'
    
    ## Build Network
    tic = time.time()
    if year_network: tbaNetwork = TBA_Network(year = year)
    elif event_network: tbaNetwork = TBA_Network(event = event)
    toc = time.time()
    print('Build Time =', toc - tic)


Projections = ['default']#, 'default_qual', 'default_elim']#, 'partners', 'opponents', 'allianceScore']
CentralityModes = ['degree', 'eigenvector', 'katz']
print_top_nodes = 10


sameAxis = True
if sameAxis:
    fig, Axes = plt.subplots(2*len(Projections),1,
                             # sharex = True,
                             figsize = [15,30],
                             )
    fig.suptitle('Network: ' + tbaNetwork.filename[17:])
    fig.tight_layout(rect=[0, 0.03, 1, 0.98])




CentralityData = dict()
print('---------------------------------------------------------------------')
try: print('Full network diamter = ', tbaNetwork.Diameter())
except: print('Diameter error... not fully connected components')
print('---------------------------------------------------------------------')
for i, projection in enumerate(Projections):
    print('---------------------------------------------------------')
    print('projection = ' + projection)
    
    print('---------------------------------------------------------')
    if sameAxis: axes = Axes[2*i:2*i+2]
    else: axes = -1
    tbaNetwork.PlotDDist(projection = projection, axes = axes)
    
    axes[0].set_title('Projection: ' + projection)
    

    
    print('Diameter = ', tbaNetwork.Diameter(projection=projection)  )      
    print('----------------------------------------------')
    tempDict = dict()
    for mode in CentralityModes:
        tempDict[mode] = tbaNetwork.Centrality(projection = projection,
                                               mode = mode,
                                               print_top_nodes = print_top_nodes)
    CentralityData[projection] = tempDict
    
if sameAxis: fig.savefig('fig/' + 'DegreeDist_' + tbaNetwork.filename[17:])


