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
import numpy as np
import os.path
from os import path
import matplotlib.pyplot as plt

## TBA_Network class ------------------------------------------------------
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
        edge type (only programmed for matches as edges).
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
                             'comp_level', 'match_number'],
                 filename_base = 'Data/TBA_Network_',
                 ):
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
        filename_base: str, optional
            The base filename with subfolders and underscore included.
            The default is 'TBA_Network_'
        """
        # Explicet Parameters
        self.year = year
        self.event = event
        self.nodeType = nodeType
        self.edgeType = edgeType
        self.nodeMeta = nodeMeta
        self.edgeMeta = edgeMeta
        self.filename = filename_base
                
        # Node Keys and Data
        if nodeType == 'team':
             if event != -1:
                 print('Event Superseding year')
                 self.event = [event]
                 self.year = event[0:4]
                 self.filename += str(self.event)
             elif year != -1:
                 self.filename += str(self.year)
        else:
             print('Node type not coded yet')
        # If network exists it is read in here
        if path.exists(self.filename + '.gml'): 
            # (if error happens generate from scratch)
            print('Reading network from file: ' + self.filename + '.gml')
            self.G = nx.read_gml(self.filename + '.gml')
            
        # Generate new network 
        else:
            print('Generating new graph: ' + self.filename)
            # Node Keys and Data
            print('Collecting Node Data')
            if event != -1:
                self.nodeData = tba.getEventTeamsInfo(event)
            elif year != -1:
                self.nodeData = tba.getTeamsInfo(year)
                self.event = tba.getEventKeys(self.year)

            # nodeKeys assignment
            self.nodeKeys = list(self.nodeData.keys())
            
            # MultGraph definition
            print('Defining Multgraph')
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
            
            # Edge Keys and Graph Generation
            print('Getting Edge info and Generating Graph')
            if edgeType == 'match' and nodeType == 'team':
                edgeData = dict()
                for event in self.event:
                    print('Event:', event)
                    eventMatchData = tba.getEventMatchData(event)
                    for match in eventMatchData:
                        edgeData.update({match['key']: match})
                self.edgeData = edgeData
                self.edgeKeys = list(edgeData.keys())
    
                # Generate Edges
                # edgeTuples = list()
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
                    
                    # 'comp_level', 'match_number' 'match_key', 'event_key'
                    for team1, team2 in itertools.combinations(
                            teams['red'] + teams['blue'], 2):
                        # if ((team1 in teams['red'] and team2 in teams['red']) 
                        #     or (team1 in teams['blue'] and team2 in teams['blue'])):
                        #     data['alliancePartners'] = True
                        
                        if {team1, team2} <= set(teams['red']):
                            data['alliancePartners'] = 'red'
                        elif {team1, team2} <= set(teams['blue']):
                            data['alliancePartners'] = 'blue'
                        else:
                            data['alliancePartners'] = 'opponents'
    
                        # Add edges to graph
                        self.G.add_edges_from([(team1, team2, matchKey, data)])
                        
                # Save Network to file
                print('Writing to gml file: ' + self.filename + '.gml')
                nx.write_gml(self.G, self.filename + '.gml')          
            else:
                print('Only match/team coded')
        
        # Projection Graphs (Generated and saved as attributes)
        print('Generating Projections')
        self.GraphProjections() #Default Projection
        
        
    
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
                ('exists')      - Weight = 1
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
        
        # Don't recreate if exists
        attrName = 'G_' + weightCalc + str(alliancePartners)
        if alliancePartners != 0:
            if alliancePartners == 1:
                attrName += '_partners'
            elif alliancePartners == -1:
                attrName += '_opponents'
        if hasattr(self, attrName):
            return getattr(self, attrName)
        elif path.exists(self.filename + attrName[2:] + '.gml'):
            # If network exists it is read in here
            #       (if error happens generate from scratch)
            print('Reading network from file: ' 
                  + self.filename + attrName[2:] + '.gml')
            setattr(self, attrName,
                    nx.read_gml(self.filename + attrName[2:] + '.gml'))
            return getattr(self, attrName)
        else:
            # Initialize Graph object
            G_projection = nx.Graph(alliancePartners = alliancePartners,
                                    weightCalc = weightCalc)
            
            # Edge Tuple Generation
            G_projection_tuples = list()
            for team1, team2 in itertools.combinations(self.G.nodes(),2):
                if self.G.has_edge(team1, team2):
                    weight = self.WeightCalc(team1, team2,
                                             alliancePartners, weightCalc)
                    if weight >= 1:
                        G_projection_tuples.append((team1, team2, weight))
                        
            # Generate Edges
            G_projection.add_weighted_edges_from(G_projection_tuples)
            
            # Save Projection Graph
            setattr(self, attrName, G_projection)
            return G_projection
    

    # Calculations for Convinence
    def WeightCalc(self, team1, team2, alliancePartners, weightCalc):
        """
        WEIGHTCALC returns a weighting between two nodes dependent on calc method.

        Parameters
        ----------
        team1 : str (node_key)
        team2 : str (node_key)
        alliancePartners : int
            Indication of if a partners restriction should be included
            -1 = include opponents
            0 = include all matches
            1 = include partners
        weightCalc : str
            Method to be used to calculate the weight between two nodes.
            default = total number of edges (matchs in common)
            default_partners = number of matchs together as partners
            default_opponents = number of matches together as opponents
            exists = 1 if connection exists
            score = alliance score if parnters, total of both if all matches
                (error if opponents)

        Returns
        -------
        float (or int)
            The caclulated weight between nodes.

        """
        
        matches = self.G[team1][team2]
        
        if alliancePartners != 0:
            if alliancePartners == 1:
                keys = [key for key in list(matches) if
                        {matches[key]['alliancePartners']} <= {'blue','red'}]
            elif alliancePartners == -1:
                keys = [key for key in list(matches) if
                        {matches[key]['alliancePartners']} <= {'opponent'}]
        else:
            keys = list(matches)
                  
        if len(keys) == 0: return 0
        
        if weightCalc == 'default':
            return len(keys)
        elif weightCalc == 'exists':
            if len(keys) >= 1:
                return 1
            else:
                return 0
        elif weightCalc == 'score':
            weight = 0
            if alliancePartners == 0:
                for key in keys:
                    weight += matches[key]['scores']['red']
                    weight += matches[key]['scores']['blue']
            elif alliancePartners == 1:
                for key in keys:
                    weight += matches[key]['scores'][
                        matches[key]['alliancePartners']]
            else:
                print('not coded for this')
            
            return weight
        
        else:
            print('not coded yet')    


    # Save and Import Network
    def ImportGML(filename):
        pass




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
    
    
    # Centrality Metrics
    def DegreeSequence(self, projection = 'none'):
        """
        DEGREESEQUENCE returns a sorted list with team keys and degreese

        Parameters
        ----------
        projection : str, optional
            Network Projection to use. The default is 'none', meaning all edges
            

        Returns
        -------
        DegreeSequence : list of tuples
            Sequence of degrees with tuples of team names and degrees

        """

        if projection != 'none':
            alliancePartners = 0
            weightCalc = 'default'
            if projection in {'match','matches','default'}:
                pass # Default values
            elif projection in {'partners'}:
                alliancePartners = 1
            elif projection in {'oponents'}:
                alliancePartners = -1
            elif projection in {'allianceScore'}:
                alliancePartners = 1
                weightCalc = 'score'
            else:
                print('using default projection')
            G = self.GraphProjections(alliancePartners, weightCalc)
        else:
            G = self.G
        
        return sorted([(n,d) for n, d in G.degree()],
                      reverse=True, # Highest degree at top
                      key = lambda x: x[1], # Sort based on degree
                      )
    
    
    def DegreeDist(self, projection = 'none'):
        """
        DEGREEDIST returns a list of the degree distribution

        Parameters
        ----------
        projection : str, optional
            What network projection to use.
            The default is 'none' (meaning all edges).
             
        Returns
        -------
        DegreeDist : list of int
            Degree distribution of the degree of each node

        """
        degSeq = self.DegreeSequence(projection)
        degSeq = sorted([d for n, d in degSeq], reverse=True)
        
        ddist = np.zeros(int(max(degSeq) + 1))
        for k in degSeq:
            ddist[k] += 1

        return ddist
        
    
    
    # Ploting and Analysis Functions
    def PlotDDist(self, projection = 'none'):
        
        ddist = self.DegreeDist(projection)
       
        cdist = [ddist[k:].sum()  for k in range(len(ddist))] 
        
        
        
        # Assign Values for Ploting
        xvalues = range(len(ddist));
        barheights = ddist # Degree Dist
        yvalues = cdist; # Cumulative Dist
        
        fig, axes = plt.subplots(2,1,sharex=True)
        
        axes[0].bar(xvalues,barheights, width=0.8, bottom=0, color='b')
        plt.autoscale('True')
        
        # Plot cdist
    #     plt.subplot(212)
        axes[1].loglog(xvalues,yvalues)
        plt.grid(True)
        
        # axes[0].set_title([titleAdd,'kmin = ', str(kmin),alphaValue])
        
        
        
    
    
    


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