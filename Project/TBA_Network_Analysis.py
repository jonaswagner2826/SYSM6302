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
from os import path
import matplotlib.pyplot as plt
import time

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
                 self.filename += str(event)
             elif year != -1:
                 self.filename += str(year)
        else:
             print('Node type not coded yet')
        # If network exists it is read in here
        if path.exists(self.filename + '.gml'): 
            # (if error happens generate from scratch)
            print('Reading network from file: ' + self.filename + '.gml'
                  + '\n' + '(may take up to 1 min to load)')
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
    def GetProjection(self, projection = 'none', qual_elim_only = 0):
        """
        Get specific projection based on the name.

        Parameters
        ----------
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches

        Returns
        -------
        G : TYPE
            DESCRIPTION.

        """
        if projection != 'none':
            print('Getting Projection:', projection)
            alliancePartners = 0
            weightCalc = 'default'
            qual_elim_only = 0
            # Seperate by qual/elim
            if projection[-5:] in {'_qual', '_elim'}:
                if projection[-5:] == '_qual': qual_elim_only = -1
                elif projection[-5:] == '_elim': qual_elim_only = 1
                projection = projection[0:-5]
            # Seperate by weight/alliancePartners
            if projection in {'match','matches','default'}:
                pass # Default values
            elif projection in {'partners'}:
                alliancePartners = 1
            elif projection in {'opponents'}:
                alliancePartners = -1
            elif projection in {'allianceScore'}:
                alliancePartners = 1
                weightCalc = 'score'
            elif projection in {'exists', 'score', 'default'}:
                weightCalc = projection
            else:
                print('using default projection')
            G = self.GraphProjections(alliancePartners,
                                      weightCalc,
                                      qual_elim_only)
        else:
            G = self.G
        return G
    
    
    
    def GraphProjections(self, alliancePartners = 0,
                         weightCalc = 'default',
                         qual_elim_only = 0,
                         NodeMeta = ['nickname', 'name', 'state_prov', 'country'],
                         ):
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
                ('score')       - alliance score if parnters, total of both if all matches (error if opponents)
                # ('MarginSum')   - Win Margin Sum 
                # ('MarginSub')   - Win Margin Subtractive (if opponents subtract)
                # ('MarginSubAvg')- Win Margin Subtractive Average (if opponents subtract)
                # ('MarginSumAvg')- Win Margin Sum Average
                # ('ScoreSum')    - Score of Alliance (or Max) Sum
                # ('ScoreSub')    - Score of Alliances Subtractive
                # ('ScoreAvg')    - Score of Alliances (or avg of each) Average
        qual_elim_only : int
            Indication of if a match type should be restricted
                -1 = include only quals
                0 = include all matches
                1 = include only elims

        Returns
        -------
        G_projection : nx.graph
            graph projection.

        """
        
        # Projection Name
        attrName = 'G_' + weightCalc
        if alliancePartners != 0:
            if alliancePartners == 1:
                attrName += '_partners'
            elif alliancePartners == -1:
                attrName += '_opponents'
        if qual_elim_only != 0:
            if qual_elim_only == -1:
                attrName += '_quals'
            elif qual_elim_only == 1:
                attrName += '_elims'
        
        projectionFilename = self.filename + '_' + attrName[2:] + '.gml'
        # Test and load if exists
        if hasattr(self, attrName):
            return getattr(self, attrName)
        elif path.exists(projectionFilename):
            # If network exists it is read in here
            #       (if error happens generate from scratch)
            print('Reading network from file: ' 
                  + self.filename + '_' + attrName[2:] + '.gml')
            tic = time.time()
            setattr(self, attrName,
                    nx.read_gml(projectionFilename))
            print('Completed in ', str(time.time() - tic), ' s')
            print('---------')
            return getattr(self, attrName)
        # Generate projection if it doesn't exist
        else:
            print('Generating new projection:')
            # Initialize Graph object
            G_projection = nx.Graph(alliancePartners = alliancePartners,
                                    weightCalc = weightCalc,
                                    qual_elim_only = qual_elim_only)
            
            # Edge Tuple Generation
            G_projection_tuples = list()
            for team1, team2 in itertools.combinations(self.G.nodes(),2):
                if self.G.has_edge(team1, team2):
                    weight = self.WeightCalc(team1, team2,
                                             alliancePartners = alliancePartners,
                                             weightCalc = weightCalc,
                                             qual_elim_only = qual_elim_only)
                    if weight >= 1:
                        G_projection_tuples.append((team1, team2, weight))
                        
            # Generate Edges
            G_projection.add_weighted_edges_from(G_projection_tuples)
            
            # Insert attributes
            for nodeMeta in NodeMeta:
                nx.set_node_attributes(G_projection,
                                       nx.get_node_attributes(self.G, nodeMeta),
                                       nodeMeta)
                # for team in G_projection.nodes():
                #     G_projection[team][attrName] = Attr[team]
            
            # Save Projection Graph
            print('Saving Projection to: ', projectionFilename)
            nx.write_gml(G_projection, projectionFilename)
            
            # Set as attribute
            setattr(self, attrName, G_projection)
            
            return G_projection
    

    # Calculations for Convinence
    def WeightCalc(self, team1, team2, alliancePartners, weightCalc,
                   qual_elim_only = 0):
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
                exists = 1 if connection exists
                score = alliance score if parnters, total of both if all matches
                    (error if opponents)
        qual_elim_only : int
            Indication of if a match type should be restricted
                -1 = include only quals
                0 = include all matches
                1 = include only elims


        Returns
        -------
        float (or int)
            The caclulated weight between nodes.

        """
        
        matches = self.G[team1][team2]
        keys = list(matches)
        # Qual/Elim
        if alliancePartners != 0:
            if alliancePartners == 1:
                keys = [key for key in keys if
                        {matches[key]['alliancePartners']} <= {'blue','red'}]
            elif alliancePartners == -1:
                keys = [key for key in keys if
                        {matches[key]['alliancePartners']} <= {'opponent'}]


        # Comp Level        
        if qual_elim_only != 0:            
            if qual_elim_only == 1:
                keys = [key for key in keys if
                        {matches[key]['comp_level']} <= {'qf','sf','f'}]
            elif qual_elim_only == -1:
                keys = [key for key in keys if
                        {matches[key]['comp_level']} <= {'qm'}]
        # No matches?
        if len(keys) == 0: return 0
        
        # Calcuation based on setting
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
                    if matches[key]['alliancePartners'] not in ['red', 'blue']: continue
                    weight += matches[key]['scores'][matches[key]['alliancePartners']]
            else:
                print('not coded for this')
            
            return weight
        
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

    # Centrality Metrics
    def Centrality(self, node = -1, projection = 'none',
                   mode = 'degree',
                   print_top_nodes = -1):
        """
        

        Parameters
        ----------
        node : str, optional
            node specific centrality (pass key). The default is -1.
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches
        mode : TYPE, optional
            Centrality calculation type. The default is 'degree'.
        print_top_nodes : int, optional
            How many of the tope nodes to be printed.
            The default is -1 = none printed

        Returns
        -------
        centrality_vector
            Vector (or single value) of the nodes centralities

        """
        
        G = self.GetProjection(projection = projection)
        
        if mode == 'degree':
            centrality_vector = nx.degree_centrality(G)
        elif mode == 'eigenvector':
            centrality_vector = nx.eigenvector_centrality(G)
        elif mode == 'katz':
            centrality_vector = nx.katz_centrality_numpy(G)
        else:
            print('mode not coded yet')
        
        if print_top_nodes > 0:
            cent_list = sorted([(n,d) for n, d in centrality_vector.items()],
                              reverse=True, # Highest degree at top
                              key = lambda x: x[1], # Sort based on degree
                              )
            print(str(mode) + ' centrality')
            print('----------------------')
            for i in range(min(int(print_top_nodes),len(cent_list))):
                n, score = cent_list[i]
                print('  %i. %s (%1.4f)' % (i+1,n,score))
                #print '  %i. %s' % (i+1,G.node_object(idx))
            print('----------------------')
        
        if node == -1:
            return centrality_vector
        else:
            return centrality_vector[node]
    
    def Diameter(self, projection = 'none',
                 qual_elim_only = 0):
        """
        

        Parameters
        ----------
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches

        Returns
        -------
        diameter : int

        """
        
        G = self.GetProjection(projection = projection,
                               qual_elim_only = qual_elim_only)
        
        try:
            diameter = nx.diameter(G)
        except:
            diameter = '\infty'
        
        return diameter
    
    # Network Structure Dists
    def DegreeSequence(self, projection = 'none'):
        """
        DEGREESEQUENCE returns a sorted list with team keys and degreese

        Parameters
        ----------
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches
        

        Returns
        -------
        DegreeSequence : list of tuples
            Sequence of degrees with tuples of team names and degrees

        """

        G = self.GetProjection(projection = projection)
        
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
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches
             
        Returns
        -------
        DegreeDist : list of int
            Degree distribution of the degree of each node

        """
        degSeq = self.DegreeSequence(projection = projection)
        degSeq = sorted([d for n, d in degSeq], reverse=True)
        
        ddist = np.zeros(int(max(degSeq) + 1))
        for k in degSeq:
            ddist[k] += 1

        return ddist
    
    # Ploting and Analysis Functions
    def PlotDDist(self, projection = 'none'):
        """
        

        Parameters
        ----------
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches

        Returns
        -------
        None.

        """
        dseq = self.DegreeSequence(projection = projection)
        dseq = sorted([d for n, d in dseq], reverse=True)
        ddist = self.DegreeDist(projection = projection)
       
        cdist = [ddist[k:].sum()  for k in range(len(ddist))] 
        
        kmin = int(0.9 * min(dseq)) # not all the way to zero
        kmax = int(max(dseq))
        
        # Assign Values for Ploting
        xvalues = range(kmin,kmax);
        barheights = ddist[kmin:kmax] # Degree Dist
        yvalues = cdist[kmin:kmax]; # Cumulative Dist
        
        fig, axes = plt.subplots(2,1,sharex=True)
        
        # Plot 
        axes[0].bar(xvalues,barheights, width=0.8, bottom=0, color='b')
        # plt.autoscale('True')
        
        # Plot cdist
        axes[1].loglog(xvalues,yvalues)
        plt.grid(True)
        
        # Title and labels
        axes[1].set_xlabel('Degree')
        
        axes[0].set_title('Network: '
                          + self.filename[17:] + '\n'
                          + ' Projection: '
                          + projection)
        
        # Save Fig
        plt.savefig('fig/' + 'DegreeDist_' 
                    + self.filename[17:] + '_' + str(projection))
        
    # Visualization
    def DrawGraph(self, projection = 'none',
                  layout = -1, ax = -1,
                  with_labels = True,
                  node_size = 200,
                  font_size = 5,
                  linewidths = 0.8,
                  figsize = [10,10]):
        """
        Draw a simple projection of using built in commands

        Parameters
        ----------
        projection : str, optional
            Specific projection to be used. The default is 'none'.
                default = match = matches = default calc w/ all alliance partners
                partners = default calc with only partners
                allianceScore = score calc with alliance partners
                + _qual = only qual matches
                + _elim = only elim matches
        layout : str, optional
            

        Returns
        -------
        ax : axis that the plot is saved in

        """
        
        if str(ax) == str(-1):
            fig, ax = plt.subplots(figsize = figsize)
            saveFig = True
        else:
            saveFig = False

        G = self.GetProjection(projection = projection)
        
        if str(layout) == str(-1): pos = nx.spring_layout(G)
        elif str(layout) == 'random': pos = nx.random_layout(G)
        elif str(layout) == 'shell': pos = nx.shell_layout(G)
        elif str(layout) == 'spring': pos = nx.spring_layout(G)
        elif str(layout) == 'circular': pos = nx.circular_layout(G)
        
        print('Generating Network Plot:', str(projection))
        
        nx.draw(G, pos = pos, ax = ax,
                with_labels = with_labels,
                node_size = node_size,
                font_size = font_size,
                linewidths = linewidths,
                )
        
        ax.set_title('Network: '
                        + self.filename[17:] + '\n'
                        + ' Projection: '
                        + projection)
        
        # Save Fig
        if saveFig:
            plt.savefig('fig/' + 'NetworkPlot_'
                        + self.filename[17:]
                        + '_' + str(projection))
    
    
    


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

