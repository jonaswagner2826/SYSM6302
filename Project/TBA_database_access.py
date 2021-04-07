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
    return getTBA('events/' + str(year) + '/keys')

def getEventTeamsKeys(event):
    return getTBA('event/' + event + '/teams/keys')

def getEventTeamsInfo(event):
    data = getTBA('event/' + event + '/teams')
    return {item['key']:item for item in data} #converts to dict

def getEventMatchKeys(event):
    return getTBA('event/' + event + '/matches/keys')

def getEventMatchData(event):
    return getTBA('event/' + event + '/matches')


# Team Specific Queries
def getTeamInfo(team, year = -1):
    return getTBA('team/' + 'frc' + str(team))
    

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
    return 


def getTeamsInfo(year = -1, pageNum = -1, maxPages = 20):
    if year == -1:
        year = ''
    else:
        year = (str(year) + '/')
    if pageNum != -1:
        data = getTBA('teams/' + year + str(pageNum))
    else:
        data = list()
        for pageNum in range(maxPages):
            data.extend(getTBA('teams/' + year + str(pageNum)))
    return {item['key']:item for item in data} #converts to dict

  

def getTeamEventKeys(team, year = -1):
    if year == -1:
        year = ''
    else:
        year = (str(year) + '/')
    return getTBA('team/' + 'frc' + str(team) + '/events/' + year + 'keys')


def getTeamMatchKeys(team, year = -1, event = -1):
    if year != -1 and event != -1:
        print('Event key superciding year')
    
    if type(team) != str:
        team = 'frc' + str(team)
    
    if event != -1:
        keys = getTBA('team/' + str(team) + '/event/' + event 
                      + '/matches/keys')
    elif year != -1:
        keys = getTBA('team/' + str(team) + '/matches/' + str(year)
                      + '/keys')
    return keys

def getTeamMatchData(team, year = -1, event = -1):
    if year != -1 and event != -1:
        print('Event key superciding year')
    
    if len(team) < 4:
        team = 'frc' + team
    if event != -1:
        data = getTBA('team/' + str(team) + '/event/' + event 
                      + '/matches')
    elif year != -1:
        data = getTBA('team/' + str(team) + '/matches/' + str(year))
    return data


# Match Specific Queries
def getMatchInfo(key, simple = True):
    if simple == True:
        matchInfo = getTBA('match/' + key + '/simple')
    else:
        matchInfo = getTBA('match/' + key)
    return matchInfo

