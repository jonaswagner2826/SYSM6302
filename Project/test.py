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
    else : tbaNetwork = tbaNetwork;
    toc = time.time()
    print('Build Time =', toc - tic)
    
    
    filename = 'TBA_Network_' + str(tbaNetwork.year) + '.gml'
    # TBA_Network data explicit
    G = tbaNetwork.G
    nx.write_gml(G, filename)
    # nodeKeys = tbaNetwork.nodeKeys
    # nodeData = tbaNetwork.nodeData
    # edgeKeys = tbaNetwork.edgeKeys
    # edgeData = tbaNetwork.edgeData
    # G_match = tbaNetwork.GraphProjections()





dseq = tbaNetwork.DegreeSequence(projection = 'allianceScore')#projection = 'partners')
print(dseq)





# degree_sequence = sorted([d for n, d in G_match.degree()], reverse=True)  # degree sequence
# degreeCount = collections.Counter(degree_sequence)
# deg, cnt = zip(*degreeCount.items())

# fig, ax = plt.subplots()
# plt.bar(deg, cnt, width = 5)







# # Test on meta data of TBA_Network Class
# matchKey = edgeKeys[7]
# matchData = edgeData[matchKey]

# matchTeams = dict()
# matchTeams['red'] = matchData['alliances']['red']['team_keys']
# matchTeams['blue'] = matchData['alliances']['blue']['team_keys']
# print('Match Teams:', matchTeams)

# matchScores = dict()
# matchScores['red'] = matchData['alliances']['red']['score']
# matchScores['blue'] = matchData['alliances']['blue']['score']
# print('Match Scores:', matchScores)








