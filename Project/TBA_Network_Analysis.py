# -*- coding: utf-8 -*-
"""
TBA_network_analysis is a module for generating and analyzing FRC match data

Created on Mon Mar 29 07:57:38 2021

@author: Jonas
"""

# Nessicary Packages
import numpy as np
import networkx as nx
import TBA_database_access as tba

# tbaNetwork class
class TBA_Network:
    def __init__(self, year = -1, event = -1,
                 nodeType = 'team', edgeType = 'match',
                 nodeMeta = ['nickname', 'name', 'state_prov', 'country'],
                 edgeMeta = ['event', ]):
        # Event Conditioning
        if str(event) != str(-1):
            print('Event Superseding year')
            year = -1
        
        # Explicet Parameters
        self.year = year
        self.event = event
        self.nodeType = nodeType
        self.edgeType = edgeType
        self.nodeMeta = nodeMeta
        self.edgeMeta = edgeMeta
        
        # Node Keys and Data
        if nodeType == 'team':
            if event != -1:
                self.nodeKeys = tba.getEventTeamsKeys(event)
                self.nodeData = tba.getEventTeamsInfo(event)
            elif year != -1:
                self.nodeKeys = tba.getTeamsKeys(year)
                self.nodeData = tba.getTeamsInfo(year)
        else:
            print('Node type not coded yet')
        
        # Edge Keys and Data
        edgeKeys = list()
        edgeData = dict()
        if edgeType == 'match':
            if nodeType == 'team':
                for node in self.nodeKeys:
                    tempKeys = tba.getTeamMatchKeys(node, year, event)
                    for key in tempKeys:
                        if key not in edgeKeys:
                            edgeKeys.append(key)
                            edgeData[key] = tba.getMatchInfo(key)
                self.edgeKeys = edgeKeys
                self.edgeData = edgeData
            else:
                print('Only match/team coded')
        else:
            print('Only match/team coded')
        
        # MultGraph definition
        self.G = nx.MultiGraph(year = self.year,
                               event = self.event,
                               nodeType = self.nodeType,
                               edgeType = self.edgeType,
                               nodeMeta = self.nodeMeta,
                               edgeMeta = self.edgeMeta)
        
        # # Node Data
        # if nodeType == 'team':
        #     for key in nodeKeys:
        #         nodeData = tba.getMatchInfo(key)
        #     self.nodeData = nodeData
        # else:
        #     print('Only team nodes coded')
        
        # # Edge Data
        # edgeKeys
        # if edgeType == 'match':
        #     if nodeType == 'team':
        #         for node in nodeKeys:
        #             edgeKeys[node] = tba.getTeamMatchKeys(node, year, event)
        #     else:
        #         print('Only match/team coded')
        # else:
        #     print('Only match/team coded')
        
    