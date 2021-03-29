import numpy as np
import requests

import TBA_database_access as tba
from TBA_Network_Analysis import TBA_Network


# eventKeys2015 = tba.getTBA('events/2015/keys')

# for event in eventKeys2015:
#     teams = tba.getTBA('event/' + event + '/teams/keys')

# team =2826
# teamMatchKeys = tba.getTeamMatchKeys(team,2015)

# teamInfo = tba.getTeamInfo(team)


# teams = tba.getTeamsKeys()


singleEventNetwork = TBA_Network(event = '2015hop')

G = singleEventNetwork.G
nodeKeys = singleEventNetwork.nodeKeys
nodeData = singleEventNetwork.nodeData
edgeKeys = singleEventNetwork.edgeKeys
edgeData = singleEventNetwork.edgeData
