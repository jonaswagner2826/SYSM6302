import numpy as np
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


event = '2015cmp'
## Build Network
tic = time.time()
tbaNetwork = TBA_Network(event = event)
toc = time.time()
print('Build Time =', toc - tic)
    


# TBA_Network data explicit
G = tbaNetwork.G
nodeKeys = tbaNetwork.nodeKeys
nodeData = tbaNetwork.nodeData
edgeKeys = tbaNetwork.edgeKeys
edgeData = tbaNetwork.edgeData



# Test on meta data of TBA_Network Class
matchKey = edgeKeys[5]
matchData = edgeData[matchKey]

matchTeams = dict()
matchTeams['red'] = matchData['alliances']['red']['team_keys']
matchTeams['blue'] = matchData['alliances']['blue']['team_keys']
print('Match Teams:', matchTeams)

matchScores = dict()
matchScores['red'] = matchData['alliances']['red']['score']
matchScores['blue'] = matchData['alliances']['blue']['score']
print('Match Scores:', matchScores)


