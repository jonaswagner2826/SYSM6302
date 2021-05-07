# -*- coding: utf-8 -*-
"""
Created on Tue May  4 19:38:33 2021

@author: Jonas
"""

# This script does specific calculations to generate degree distributions 
# and other basic things

runFromScratch = True

if runFromScratch:

    import numpy as np
    import networkx as nx
    import requests
    import collections
    import matplotlib.pyplot as plt
    
    # Module with functions for accessing TBA database
    import TBA_database_access as tba
    
    # TBA_Network Class Import
    from TBA_Network_Analysis import TBA_Network
    import TBA_Network_Analysis as tba_na
    
    # other tools
    import time



layout = 'spring'

year_network = False
event_network = True

# network_keys = list()
# for year in range(2003,2020):
#     key = str(year) + 'cmp'
#     if year >= 2017:
#         network_keys.append(key + 'tx')
#         if year == 2017:
#             network_keys.append(key + 'mo')
#         else:
#             network_keys.append(key + 'mi')
#     else:
#         network_keys.append(key)
# print(network_keys)
network_keys = ['2015hop']

proj_base = ['default']#, 'partners', 'opponents', 'allianceScore']
proj_tail = ['','_qual','_elim']

num_keys = len(network_keys)
num_proj = len(proj_base) * len(proj_tail)



plt.rcParams.update({'font.size':20})
plt.rc('figure', titlesize = 50)
if num_proj == 1:
    fig, axes = plt.subplots(4, 5, figsize = [35,25])
    fig.suptitle('Eienstien Matches 2003-2019')
elif num_keys == 1:
    fig, axes = plt.subplots(3,1, figsize = [10,20])
    fig.suptitle('2015 Hopper Sub-Division')
else:
    fig, axes = plt.subplots(num_proj, num_keys, figsize = [5*num_keys,5*num_proj])


t = 0
k = 0
for i, key in enumerate(network_keys):
    ## Build Network
    print('Building: ', key)
    tic = time.time()
    if year_network: tbaNetwork = TBA_Network(year = key)
    elif event_network: tbaNetwork = TBA_Network(event = key)
    toc = time.time()
    print('Build Time =', toc - tic)
    
    if num_proj == 1:
        if t == int(num_keys/4):
            t = 0
            k += 1
        j = i - k * int(num_keys/4)
        t += 1
        print(k,j)
        tbaNetwork.DrawGraph(projection = proj_base[0] + proj_tail[0],
                                 layout = layout,
                                 ax = axes[k,j],
                                 )
    elif num_keys == 1:
        for j, base in enumerate(proj_base):
            for k, tail in enumerate(proj_tail):
                ax = axes[j*len(proj_tail) + k]
                tbaNetwork.DrawGraph(projection = base + tail,
                                     layout = layout,
                                     ax = ax,
                                     )
                ax.set_title('Projection: ' + base + tail)
                
    else:
        for j, base in enumerate(proj_base):
            for k, tail in enumerate(proj_tail):
                tbaNetwork.DrawGraph(projection = base + tail,
                                     layout = layout,
                                     ax = axes[i*len(proj_base)*len(proj_tail),
                                               j*len(proj_tail) + k],
                                     )
            

# fig.savefig('fig/' + 'NetworkPlot_' + 'cmp_2003_2019')


# fig.savefig('fig/' + 'NetworkPlot_' + '2015hop')


# print('---------------------------------------------------------------------')
# for projection in Projections:
#     for qual_elim_only in Qual_elim_only:
#         print('---------------------------------------------------------')
#         print('projection = ' + projection + '  &  ' +
#               'qual_elim_only = ' + str(qual_elim_only))
        
#         print('---------------------------------------------------------')
#         tbaNetwork.PlotDDist(projection = projection,
#                              qual_elim_only = qual_elim_only)
#         print('Diameter = ', tbaNetwork.Diameter(projection=projection,
#                                                  qual_elim_only=qual_elim_only,
#                                                  ))
#         print('----------------------------------------------')
#         for mode in CentralityModes:
#             tbaNetwork.Centrality(projection = projection,
#                                   qual_elim_only = qual_elim_only,
#                                   mode = mode,
#                                   print_top_nodes = print_top_nodes)
        


