import numpy as np
import networkx as nx
import requests

# Module with functions for accessing TBA database
import TBA_database_access as tba

# TBA_Network Class Import
from TBA_Network_Analysis import TBA_Network

# Debuging tools
import time


year_network = True
event_network = False

year = '2015'
event = '2015hop'

## Build Network
tic = time.time()
if year_network: tbaNetwork = TBA_Network(year = year)
elif event_network: tbaNetwork = TBA_Network(event = event)
toc = time.time()
print('Build Time =', toc - tic)


filename = 'TBA_Network_' + str(tbaNetwork.year) + '.gml'
# TBA_Network data explicit
G = tbaNetwork.G
nx.write_gml(G, filename)
nodeKeys = tbaNetwork.nodeKeys
nodeData = tbaNetwork.nodeData
edgeKeys = tbaNetwork.edgeKeys
edgeData = tbaNetwork.edgeData




# Test on meta data of TBA_Network Class
matchKey = edgeKeys[7]
matchData = edgeData[matchKey]

matchTeams = dict()
matchTeams['red'] = matchData['alliances']['red']['team_keys']
matchTeams['blue'] = matchData['alliances']['blue']['team_keys']
print('Match Teams:', matchTeams)

matchScores = dict()
matchScores['red'] = matchData['alliances']['red']['score']
matchScores['blue'] = matchData['alliances']['blue']['score']
print('Match Scores:', matchScores)
