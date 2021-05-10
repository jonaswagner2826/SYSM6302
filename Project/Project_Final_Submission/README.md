# Network Analysis of FRC Matches
## SYSM 6302 - Final Project
## Author: Jonas Wagner

## Project Overview
In this project multiple networks will be created and analyzed on match data between FRC teams for multiple events for various years of competition. In each network graph, a team will be represented by nodes and individual matches will be included as edges between teams that competed in the match.

## Data Source:
FRC Match Data 2003-2018
The Blue Alliance Database: [https://www.thebluealliance.com/]
Accessed through The Blue Alliance APIv3 with a custom TBA_Database_Access.py module

## 2015 Season Network Overview
### Description:
The first network constructed is the one for an entire 2015 season. It is a mult-graph with each node being a team competing in the seasons and mult-edge connections are each match interaction between teams (alliances or opponents), while graph projections takes mult-edges with weigtings based on the mult-edges between nodes.

### Mult-graph Details
Nodes: 2,935 Teams
Mult-Edges: 195,152 Matches
Degree Assortativity: 0.358
Agerage Degree: 132.98
Density: 0.04532

### Default Projection Details
Nodes: 2,909 Teams
Edges: 106,889 Matches
Components: 1
Diameter: 4
Clustering Coefficient: 0.635
Degree Assortativity: 0.296
Agerage Degree: 73.49
Density: 0.02527

## Code Details
### TBA_database_access.py
This module includes many functions nessicary for interacting with the TBA Database APIv3 and return the appropriete data in python readable formats. This includes many functions that also make quireying for particular data easy.

### TBA_network_Analysis.py
This module includes a the TBA_Network class to generate network objects that contain a mult-graph and projections. The class also has methods to use to analyze the entire network or individual projections, including calculating network metrics, finding and ploting degree sequences/distributions, and visualizing the networks.

### graph_visualize.py
This script is used to visualize multiple networks or projections with the TBA_Network methods. This allowed for a more streamlined method of generating drawings of networks together for comparrision.

### dist_and_centrality_calc.py
This script is used to calculate network metrics and find/plot degree distributions for multiple networks or projections.

### test.py
This is the primary script used to test and execute the generation and analysis of networks using the TBA_Network Class.


