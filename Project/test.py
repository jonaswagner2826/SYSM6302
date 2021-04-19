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


generateNewGraphs = True


if generateNewGraphs:

    year_network = False
    event_network = True
    
    year = '2015'
    event = '2015hop'
    
    ## Build Network
    tic = time.time()
    if year_network: tbaNetwork = TBA_Network(year = year)
    elif event_network: tbaNetwork = TBA_Network(event = event)
    toc = time.time()
    print('Build Time =', toc - tic)


# dseq = tbaNetwork.DegreeSequence(projection = 'matches')#projection = 'partners')
# ddist = tbaNetwork.DegreeDist('matches')

tbaNetwork.PlotDDist(projection = 'partners')








