# -*- coding: utf-8 -*-
"""
TBA_network_analysis is a module for generating and analyzing FRC match data

Created on Mon Mar 29 07:57:38 2021

@author: Jonas
"""

# Nessicary Packages
import networkx as nx
import itertools
import TBA_database_access as tba

# TBA_Network class ------------------------------------------------------
class TBA_Network:
    """
    TBA_NETWORK is a class for creating and analyzing networks made up from
    FIRST Robotics Competition match data from The Blue Alliance.
    
    Atributes
    ---------
    year : str
        year of frc season.
    event : list of str
        list of event_keys for all events in network.
    nodeType : str
        node type (only programmed for teams as nodes).
    edgeType : str
        edge type (only programmed for matches as nodes).
    nodeMeta : list of str
        list of meta elements to be stored as node attibutes.
    edgeMeta : list of str
        list of meta elements to be stored as edge attibutes.
    nodeKeys : list of str
        list of keys for all the nodes in the network.
    edgeKeys : list of str
        list of keys for all the (meta-)edges in the network.
        (These edges are actually more like clusters... each is a match)
    nodeData : dict of dicts
        dictionary of all node attributes keyed by the nodeKeys.
    edgeData : dict of dicts
        dictionary of all edge attributes keyed by the nodeKeys.
        (These edges are actually more like clusters... each is a match)
    edgeTuples : list of tuples
        list containing tuples related to every node within a the network.
        (used to generate all the edges within the nx.MultiGraph)
    G : nx.MultiGraph
        nx.MultiGraph constructed with all the nodes and edges with the metadata
        stored as attributes.
    G_default : nx.Graph
        nx.Graph that is the default weighted undirected projection representing
        the total number of edges that connects them.
    
    Methods
    -------
    GraphProjections(self, alliancePartners = 0, weightCalc = 'default')
        Generates undirected weighted projections of the network with weighting
        calculated acording to specific parameters.
    WeightCalc(self, team1, team2, weightCalc)
        Function for detirmining the weighting between two nodes.
    TeamKeys(self)
        Method that returns a list of team keys
    MatchKeys(self)
        Method that returns a list of match keys
    
    ..... More need to be added for network analysis
    
    
    """
    
    def __init__(self, year = -1, event = -1,
                 nodeType = 'team', edgeType = 'match',
                 nodeMeta = ['nickname', 'name', 'state_prov', 'country'],
                 edgeMeta = ['match_key', 'event_key', 'scores', 'teams',
                             'winning_alliance', 'alliancePartners',
                             'comp_level', 'match_number']):
        """
        TBA_NETWORK constructor function. Creates a TBA_Network object
        constructed with TBA data acorrding to specific inputs
        
        Parameters
        ----------
        year : int or str, optional
            year specifier. The default is -1.
        event : str, optional
            event_key for a specific event. The default is -1.
        nodeType : str, optional
            type of parameter to be a node.
            The default is 'team'. (only default coded)
        edgeType : str, optional
            type of parameter to ba an edge.
            The default is 'match'. (only default coded)
        nodeMeta : str, optional
            meta data to be included as node atributes.
            The default is ['nickname', 'name', 'state_prov', 'country'].
        edgeMeta : str, optional
            meta data to be included as edge atrributes.
            The default is ['match_key', 'event_key', 'scores', 'teams',
                                'winning_alliance', 'alliancePartners',
                                'comp_level', 'match_number'].
        """
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
        edgeData = dict()
        if edgeType == 'match' and nodeType == 'team':
            for event in self.event:
                print('Event:', event)
                eventMatchData = tba.getEventMatchData(event)
                for match in eventMatchData:
                    edgeData.update({match['key']: match})
            self.edgeData = edgeData
            self.edgeKeys = list(edgeData.keys())

            # Generate Edges
            edgeTuples = list()
            for matchKey in self.edgeKeys:
                matchData = self.edgeData[matchKey]

                teams = MatchTeams(matchData)
                data = {'scores' : MatchScores(matchData),
                        'comp_level' : matchData['comp_level'],
                        'match_number' : matchData['match_number'],
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
        
        # Projection Graphs
        self.G_default = self.GraphProjections() #Default Projection
        
        
    
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
        """
        WEIGHTCALC returns a weighting between two nodes dependent on calc method.

        Parameters
        ----------
        team1 : str (node_key)
        team2 : str (node_key)
        weightCalc : str
            Method to be used to calculate the weight between two nodes.

        Returns
        -------
        float (or int)
            The caclulated weight between nodes.

        """
        if weightCalc == 'default':
            return self.G.number_of_edges(team1,team2)
        else:
            print('not coded yet')

    # Output parameters
    def TeamKeys(self):
        """
        Returns a list of the team keys
        """
        if self.nodeType == 'team':
            return self.nodeKeys
        else:
            return -1 #not coded yet
        
    def MatchKeys(self):
        """
        Returns a list of the match keys
        """
        if self.edgeType == 'match':
            return self.edgeKeys
        else:
            return -1 #not coded yet


## Helpful functions ---------------------------------------------------------
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

## Old Code
# this was for doing specific adjustments for metaData... got rid of it for 
# simplicity...
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