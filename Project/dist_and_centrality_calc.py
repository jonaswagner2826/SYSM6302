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


Projections = ['default', 'partners', 'opponents', 'allianceScore']
Qual_elim_only = [-1, 0, 1]
CentralityModes = ['degree', 'eigenvector', 'katz']
print_top_nodes = 10

print('---------------------------------------------------------------------')
try: print('Full network diamter = ', tbaNetwork.Diameter())
except: print('Diameter error... not fully connected components')
print('---------------------------------------------------------------------')
for projection in Projections:
    for qual_elim_only in Qual_elim_only:
        print('---------------------------------------------------------')
        print('projection = ' + projection + '  &  ' +
              'qual_elim_only = ' + str(qual_elim_only))
        
        print('---------------------------------------------------------')
        tbaNetwork.PlotDDist(projection = projection,
                             qual_elim_only = qual_elim_only)
        print('Diameter = ', tbaNetwork.Diameter(projection=projection,
                                                 qual_elim_only=qual_elim_only,
                                                 ))        
        print('----------------------------------------------')
        for mode in CentralityModes:
            tbaNetwork.Centrality(projection = projection,
                                  qual_elim_only = qual_elim_only,
                                  mode = mode,
                                  print_top_nodes = print_top_nodes)
        


