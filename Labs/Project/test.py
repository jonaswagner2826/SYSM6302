import numpy as np
import requests

import TBA_database_access as tba


# eventKeys2015 = tba.getTBA('events/2015/keys')

# for event in eventKeys2015:
#     teams = tba.getTBA('event/' + event + '/teams/keys')

team = 171
teamEventKeys = tba.getTeamEventKeys(team)
