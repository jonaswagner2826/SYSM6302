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
                 edgeMeta = ['event']):
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
                self.year = event[0:4]
            elif year != -1:
                self.nodeKeys = tba.getTeamsKeys(year)
                self.nodeData = tba.getTeamsInfo(year)
        else:
            print('Node type not coded yet')
        
        
        # MultGraph definition
        self.G = nx.MultiGraph(year = self.year,
                               event = self.event,
                               nodeType = self.nodeType,
                               edgeType = self.edgeType,
                               nodeMeta = self.nodeMeta,
                               edgeMeta = self.edgeMeta)
        
        # Edge Keys and Data
        edgeKeys = list()
        edgeData = dict()
        if edgeType == 'match' and nodeType == 'team':
            # Generate Nodes from team keys
            # attributes = zip(self.nodeKeys, self.nodeData.values())
            self.G.add_nodes_from(self.nodeKeys)
            self.G = nx.set_node_attributes(self.G, self.nodeData)
            # node and nodeKeys refer to individual teams
            for node in self.nodeKeys:
                # teamMatchData is a list of all matchs a team plays (event or year)
                teamMatchData = tba.getTeamMatchData(node, year, event)
                for match in teamMatchData:
                    # This is for every match key (ovoid repeat)
                    if match['key'] not in edgeKeys:
                        # Save match key and data for TBA_network data
                        edgeKeys.append(match['key'])
                        edgeData[match['key']] = match
                        # G.
            self.edgeKeys = edgeKeys
            self.edgeData = edgeData
        else:
            print('Only match/team coded')
        

        
        
        
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
    
    
    def TeamKeys(self):
        if self.nodeType == 'team':
            return self.nodeKeys
        else:
            return -1 #not coded yet
        
    def MatchKeys(self):
        if self.edgeType == 'match':
            return self.edgeKeys
        else:
            return -1 #not coded yet
        
    