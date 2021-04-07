# -*- coding: utf-8 -*-
"""
TBA_database_access is a module with functions for requesting from TBA.

Created on Wed Feb 24 18:43:49 2021

@author: Jonas
"""
import requests

# Interaction with TBA database
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
    """
    Get all the keys of events over the course of a year

    Parameters
    ----------
    year : str (or int)

    Returns
    -------
    list of str (match_keys)

    """
    return getTBA('events/' + str(year) + '/keys')

def getEventTeamsKeys(event):
    """
    Get all the team keys that attend a particular event

    Parameters
    ----------
    event : str (event_key)

    Returns
    -------
    list of str (team_keys)

    """
    return getTBA('event/' + event + '/teams/keys')

def getEventTeamsInfo(event):
    """
    Get all the teams info from a particular event.

    Parameters
    ----------
    event : str (event_key)

    Returns
    -------
    dict of dicts
        dictionary of all the teams info keyed by the team_key (frc####)

    """
    data = getTBA('event/' + event + '/teams')
    return {item['key']:item for item in data} #converts to dict

def getEventMatchKeys(event):
    """
    Get all the match keys of a particular event

    Parameters
    ----------
    event : str (event_key)

    Returns
    -------
    list of str (match_keys)

    """
    return getTBA('event/' + event + '/matches/keys')

def getEventMatchData(event):
    """
    Get all the match data from a particular event.

    Parameters
    ----------
    event : str (event_key)

    Returns
    -------
    dict of dicts
        dictionary of all the match data keyed by the match_key

    """
    return getTBA('event/' + event + '/matches')


# Team Specific Queries
def getTeamInfo(team):
    """
    Get all the info of specific team.

    Parameters
    ----------
    team : str (or int)

    Returns
    -------
    dict
        dictionary of the teams info

    """
    return getTBA('team/' + 'frc' + str(team))
    

def getTeamsKeys(year = -1, pageNum = -1, maxPages = 20):
    """
    Get all the team keys from TBA given the year, page number and max pages to search

    Parameters
    ----------
    year : str (or int or -1) The default is -1.
    pageNum : str (or int or -1) The default is -1.
    maxPages : int The default is 20.

    Returns
    -------
    keys : list of str
        list of all the teams keys found

    """
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


def getTeamsInfo(year = -1, pageNum = -1, maxPages = 20):
    """
    Get Team Infor from multiple teams (from the general year search)
    
    Parameters
    ----------
    year : str (or int or -1) The default is -1.
    pageNum : str (or int or -1) The default is -1.
    maxPages : int The default is 20.

    Returns
    -------
    dict of dicts
        dictionary of dicts containing the team info keyed by the team_key

    """
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
    """
    Get all the keys of events a team attended

    Parameters
    ----------
    team : str (or int)
    year : str (or int or -1) The default is -1.

    Returns
    -------
    list of str (event_keys)

    """
    if year == -1:
        year = ''
    else:
        year = (str(year) + '/')
    return getTBA('team/' + 'frc' + str(team) + '/events/' + year + 'keys')


def getTeamMatchKeys(team, year = -1, event = -1):
    """
    Get all the match keys for a particular team

    Parameters
    ----------
    team : str (or int)
    year : str (or int or -1) The default is -1.
    event : str (or -1) The default is -1.

    Returns
    -------
    keys : list of str (match_keys)

    """
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
    """
    Get all the match data for a particular team

    Parameters
    ----------
    team : str (or int)
    year : str (or int or -1) The default is -1.
    event : str (or -1) The default is -1.

    Returns
    -------
    data : dict of dicts
        dict of dicts containg match data keyed by the match_key

    """

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
def getMatchData(key, simple = True):
    """
    Get the match data for a particular match

    Parameters
    ----------
    key : str (match_key)
    simple : bool, optional
        simple match data or not. The default is True.

    Returns
    -------
    matchData : dict
        dict containing all the match data

    """
    if simple == True:
        matchData = getTBA('match/' + key + '/simple')
    else:
        matchData = getTBA('match/' + key)
    return matchData

