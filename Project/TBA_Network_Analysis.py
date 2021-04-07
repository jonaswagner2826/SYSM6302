# -*- coding: utf-8 -*-
"""
TBA_network_analysis is a module for generating and analyzing FRC match data

Created on Mon Mar 29 07:57:38 2021

@author: Jonas
"""

# Nessicary Packages
import numpy as np
import networkx as nx
import itertools
import TBA_database_access as tba

# tbaNetwork class
class TBA_Network:
    def __init__(self, year = -1, event = -1,
                 nodeType = 'team', edgeType = 'match',
                 nodeMeta = ['nickname', 'name', 'state_prov', 'country'],
                 edgeMeta = ['match_key', 'event_key', 'scores', 'teams',
                             'winning_alliance', 'alliancePartners',
                             'comp_level', 'match_number']):
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
                self.nodeData = tba.getEventTeamsInfo(event)
                print('Event Superseding year')
                self.event = [event]
                self.year = event[0:4]
            elif year != -1:
                self.nodeData = tba.getTeamsInfo(year)
                print('All events of ', year,' included')
                self.event = tba.getEventKeys(self.year)
        else:
            print('Node type not coded yet')
        
        # nodeKeys assignment
        self.nodeKeys = list(self.nodeData.keys())
        
        # MultGraph definition
        self.G = nx.MultiGraph(year = self.year,
                               event = self.event,
                               nodeType = self.nodeType,
                               edgeType = self.edgeType,
                               nodeMeta = self.nodeMeta,
                               edgeMeta = self.edgeMeta)
        
        
        # Generate Nodes from team keys
        self.G.add_nodes_from(self.nodeKeys)
        # Generate meta Data
        self.nodeMetaData = dict()
        for key in self.nodeKeys:
            data = dict()
            for meta in self.nodeMeta:
                data[meta] = self.nodeData[key][meta]
            self.nodeMetaData[key] = data
        # Assign node attributes
        nx.set_node_attributes(self.G, self.nodeMetaData)
        
        # Edge Keys and Data
        # edgeKeys = list() # Keys and data don't line up with each edge
        edgeData = dict() # Keys and data don't line up with each edge
        if edgeType == 'match' and nodeType == 'team':
            for event in self.event:
                print('Event:', event)
                eventMatchData = tba.getEventMatchData(event)
                for match in eventMatchData:
                    edgeData.update({match['key']: match})
            self.edgeData = edgeData
            self.edgeKeys = list(edgeData.keys())
                
        
        
        
        
        

        #     # node and nodeKeys refer to individual teams
        #     for node in self.nodeKeys:
        #         # teamMatchData is a list of all matchs a team plays (event or year)
        #         teamMatchData = tba.getTeamMatchData(node, year, event)
        #         for match in teamMatchData:
        #             # This is for every match key (ovoid repeat)
        #             if match['key'] not in edgeKeys:
        #                 # Save match key and data for TBA_network data
        #                 edgeKeys.append(match['key'])
        #                 edgeData[match['key']] = match
        #     self.edgeKeys = edgeKeys
        #     self.edgeData = edgeData
        
        
        
            
            # Generate Edges
            edgeTuples = list()
            # for matchKey, matchData in [self.edgeData.keys(), self.edgeData.values()]:
            for matchKey in self.edgeKeys:
                matchData = self.edgeData[matchKey]
                # data = dict()
                # for meta in edgeMeta:
                #     if meta == 'teams':
                #         teams = MatchTeams(matchData)
                #     # get score data using 
                #     elif meta == 'scores':
                #         data['scores'] = MatchScores(matchData)
                #     # Winning alliance sometimes doesn't show up...
                #     elif meta == 'winning_alliance':
                #         if matchData[meta] != '':
                #             data[meta] = matchData[meta]
                #         elif MatchScores(matchData)['red'] > MatchScores(matchData)['blue']:
                #             data[meta] = 'red'
                #         elif MatchScores(matchData)['red'] < MatchScores(matchData)['blue']:
                #             data[meta] = 'blue'
                #         else:
                #             data[meta] = 'tie?' # should question...
                #     elif meta ==  'alliancePartners':
                #         pass # Assume this is always included in init
                #     elif meta == 'match_key':
                #         pass # Assume this is always included in init
                #     else:
                #         data[meta] = matchData[meta]
                teams = MatchTeams(matchData)
                data = {'scores' : MatchScores(matchData),
                        'comp_level' : matchData['comp_level'],
                        'match_number' : matchData['match_number'],
                        # 'match_key' : matchData['match_key'], included as index (key) of tuples
                        'event_key' : matchData['event_key']
                        }
                # Winning Alliance....
                if matchData['winning_alliance'] != '':
                    data['winning_alliance'] = matchData['winning_alliance']
                elif MatchScores(matchData)['red'] > MatchScores(matchData)['blue']:
                    data['winning_alliance'] = 'red'
                elif MatchScores(matchData)['red'] < MatchScores(matchData)['blue']:
                    data['winning_alliance'] = 'blue'
                else:
                    data['winning_alliance'] = 'tie?'
                
                'comp_level', 'match_number' 'match_key', 'event_key'
                for team1, team2 in itertools.combinations(
                        teams['red'] + teams['blue'], 2):
                    if ((team1 in teams['red'] and team2 in teams['red']) 
                        or (team1 in teams['blue'] and team2 in teams['blue'])):
                        data['alliancePartners'] = True
                    else:
                        data['alliancePartners'] = False
                    edgeTuples.append((team1, team2, matchKey, data))
            self.edgeTuples = edgeTuples
            
        else:
            print('Only match/team coded')
        
        # Add edges to graph
        self.G.add_edges_from(self.edgeTuples)
        
        # Projection Graphs # running these takes a lot of comp time
        # self.G_default = self.GraphProjections() #Default Projection
        
        
    
    # Projection Graphs
    def GraphProjections(self, alliancePartners = 0, weightCalc = 'default'):
        """
        GRAPHPROJECTIONS generates a projection of the nx.multigraph as
        nx.graphs with defined edge weights.

        Parameters
        ----------
        alliancePartners : int, optional
            Alliance Partners (1), Opponents (-1) or All(0). The default is 0.
        weightCalc: str, optional
            Calculation settings:
                ('default')     - Total Matches (Default)
                ('MarginSum')   - Win Margin Sum 
                ('MarginSub')   - Win Margin Subtractive (if opponents subtract)
                ('MarginSubAvg')- Win Margin Subtractive Average (if opponents subtract)
                ('MarginSumAvg')- Win Margin Sum Average
                ('ScoreSum')    - Score of Alliance (or Max) Sum
                ('ScoreSub')    - Score of Alliances Subtractive
                ('ScoreAvg')    - Score of Alliances (or avg of each) Average

        Returns
        -------
        G_projection : nx.graph
            graph projection.

        """
        
        #Create Matches
        G_projection = nx.Graph(alliancePartners = alliancePartners,
                                weightCalc = weightCalc)
        # All Matchs
        if alliancePartners == 0:
            G_projection_tuples = list()
            for team1, team2 in itertools.combinations(self.G.nodes(),2):
                if self.G.has_edge(team1, team2):    
                    G_projection_tuples.append(
                        (team1, team2, self.WeightCalc(team1, team2, weightCalc)))
            G_projection.add_weighted_edges_from(G_projection_tuples)
        # AlliancePartners Network
        elif alliancePartners == 1:
            pass # Need to eliminate edges where they are not partners
        # Opponents Network
        elif alliancePartners == -1:
            pass #need to eliminate all edges where teams are partners
       
        return G_projection
    

    # Calculations for Convinence
    def WeightCalc(self, team1, team2, weightCalc):
        if weightCalc == 'default':
            return self.G.number_of_edges(team1,team2)
        else:
            print('not coded yet')
    
    
    
    
    # Output parameters
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
    
    
    
    
# Helpful functions
def MatchTeams(matchData):
    """
    Returns a dictionary of teams in red or blue alliances given match data
    """
    matchTeams = dict()
    matchTeams['red'] = matchData['alliances']['red']['team_keys']
    matchTeams['blue'] = matchData['alliances']['blue']['team_keys']
    return matchTeams


def MatchScores(matchData):
    """
    Returns a dictionary of scores for red or blue alliances given match data
    """
    matchScores = dict()
    matchScores['red'] = matchData['alliances']['red']['score']
    matchScores['blue'] = matchData['alliances']['blue']['score']
    return matchScores