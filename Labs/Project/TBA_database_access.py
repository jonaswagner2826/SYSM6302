# -*- coding: utf-8 -*-
"""
TBA_database_access is a module with functions for requesting from TBA.

Created on Wed Feb 24 18:43:49 2021

@author: Jonas
"""
import requests
import json





def getTBA(url, baseURL = 'http://www.thebluealliance.com/api/v3/',
           header = {'X-TBA-Auth-Key': '7uiNdsPDiLnsKapBtr3IlZfb4wYGkvpPD9IpyCd5wxKt0f1KPVx8AzWkqadHeoy0'}):
    """
    Get the JSON from The Blue Alliance database for requested url extension.

    Parameters
    ----------
    url : string
        url request extension.
    baseURL : string, optional. Default is TBA API v3
    header: set of strings, optional. Default is just TBA auth key.

    Returns
    -------
    json
        Requested data from The Blue Alliance.

    """
    return requests.get(baseURL + url, headers = header).json()



# Event Specific Queries
def getEventKeys(year):
    return getTBA('events/' + year + '/keys')

def getEventTeamsKeys(event):
    return getTBA('event/' + event + '/teams/keys')

def getEventMatchKeys(event):
    return getTBA('event/' + event + '/matches/keys')



# Team Specific Queries
def getTeamsKeys(year = -1, pageNum = -1, maxPages = 20):
    if year == -1:
        year = ''
    else:
        year = (str(year) + '/')
    
    if pageNum != -1:
        keys = getTBA('teams/' + year + str(pageNum) + '/keys')
    else:
        keys = list()
        for pageNum in range(maxPages):
            keys.extend(getTBA('teams/' + year + str(pageNum) + '/keys'))
    return keys
    
def getTeamEventKeys(team, year = -1):
    if year == -1:
        year = ''
    else:
        year = (str(year) + '/')
    return getTBA('team/' + 'frc' + str(team) + '/events/' + year + 'keys')


def getTeamMatchKeys(team, year = -1, event = -1):
    if year != -1 and event != -1:
        print('Event key superciding year')
    
    if event != -1:
        keys = getTBA('team/' + 'frc' + str(team) + '/event/' + event 
                      + '/matches/keys')
    elif year != -1:
        keys = getTBA('team/' + 'frc' + str(team) + '/matches/' + str(year)
                      + '/keys')

    