import numpy as np
import networkx as nx
import requests

# Module with functions for accessing TBA database
import TBA_database_access as tba

# TBA_Network Class Import
from TBA_Network_Analysis import TBA_Network

# Debuging tools
import time


# eventKeys2015 = tba.getTBA('events/2015/keys')

# for event in eventKeys2015:
#     teams = tba.getTBA('event/' + event + '/teams/keys')

# team =2826
# teamMatchKeys = tba.getTeamMatchKeys(team,2015)

# teamInfo = tba.getTeamInfo(team)


# teams = tba.getTeamsKeys()

year = '2015'
event = '2015hop'
## Build Network
"""
Notes on timing of graph build:
    - Regular event (hopper sub-division) around 20 sec w/ projection 10 w/out
    ... After adjustments... < 1 sec!!!!
    - Full season (2015) (gave up on it...)
    ... timming probably messed up by mining... idk by how much though
    ... idk yet not done (bottleneck is probably api speed... 0.2 ish Mbps download at full)
    ... curretly it is pulling 6 times for each match!!!!
    ... could also be ram I guess... it's up to 75% usage... but isn't using more then brave...
    - Full Season (2015) after redoing the structure of the requests (event based instead of node based)
    ... 66 sec!!!! awesome!
"""
tic = time.time()
# tbaNetwork = TBA_Network(year = year)
tbaNetwork = TBA_Network(event = event)
toc = time.time()
print('Build Time =', toc - tic)


filename = 'TBA_Network_' + str(tbaNetwork.year)
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
