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
    event = '2018cmpmi'
    
    ## Build Network
    tic = time.time()
    if year_network:
        network_name = year
        tbaNetwork = TBA_Network(year = year)
    elif event_network:
        network_name = event
        tbaNetwork = TBA_Network(event = event)
        
    toc = time.time()
    print('Build Time =', toc - tic)


# dseq = tbaNetwork.DegreeSequence(projection = 'matches')#projection = 'partners')
# ddist = tbaNetwork.DegreeDist('matches')

# tbaNetwork.PlotDDist(projection = 'partners')
# dseq_score = tbaNetwork.DegreeSequence(projection='allianceScore')
# centrality_score = tbaNetwork.Centrality(
#                                          projection = 'default',
#                                          print_top_nodes =20,
#                                          mode = 'eigenvector',
#                                          )
# centrality_test = tbaNetwork.Centrality('frc2826', projection = 'allianceScore')


# nx.draw(tbaNetwork.GraphProjections(
#                                     alliancePartners=0,
#                                     qual_elim_only=1))
# 

projName = 'default_elim'

# fig, ax = plt.subplots(figsize = [100,100])
tbaNetwork.DrawGraph(projName)#'default_qual', layout = 'circular')
# plt.saveFig('fig/' + 'NetworkPlot_' + network_name + '_' + projName)

