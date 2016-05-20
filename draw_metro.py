#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import rcParams
import matplotlib.pyplot as plt 
import networkx as nx
import re

rcParams['figure.figsize'] = (10,10)
rcParams['figure.subplot.left'] = 0.05
rcParams['figure.subplot.right'] = 0.95
rcParams['figure.subplot.bottom'] = 0.05
rcParams['figure.subplot.top'] = 0.95
rcParams['figure.subplot.wspace'] = 0
rcParams['figure.subplot.hspace'] = 0

table = {}      # table = [№_st, branch, X, Y, name, (direct)]
n_station = 0
f = open('data\wiki\metro.txt','r')       # data raw from wikipedia
for i in range(1850):
    line = f.readline()[:-1]
    if re.match(r'\|-', line):
        if n_station:
            table[n_station] = [n_station, branch, x_st, y_st, name]
        n_station = n_station+1
    if re.match(r'\| style', line):
        branch = re.findall(r'/цвет линии\|(\d+)', line)[0]
    if re.match(r'\| {{coord', line):
        name = re.findall(r'name=(.*)\|nogoogle', line)[0]
        x_st, y_st = re.findall(r'(\d{2}.\d{4})', line)

branch_prev = 0
for i in table:
    if table[i][1] == branch_prev:
        if (i != 141) & (i != 74):
            table[i].append(i-1)
    branch_prev = table[i][1]
    if i == 80:
        table[i].append(91)

f.close()
#==============================================================================

# table[i] = [№_st, branch, X, Y, name, (direct)]
G=nx.Graph()
pos = {}
labels = {}
branch_list = {
    'Sokolnicheskaya'   :[[], '#EE2E22', 1],
    'Zamoskworetskaya'  :[[], '#47B85E', 2],
    'Arbats_Pokrovsk'   :[[], '#0077BF', 3],
    'Filyovskaya'       :[[], '#1AC1F3', 4],
    'Kolcevaya'         :[[], '#884E35', 5],
    'Kaluzhsk_Rizhsk'   :[[], '#F48232', 6],
    'Tagansk_Krasnopr'  :[[], '#8D479B', 7],
    'Kalininskaya'      :[[], '#FECB2F', 8],
    'Serpux_Timiryaz'   :[[], '#A0A2A3', 9],
    'Lublinskaya'       :[[], '#B3D345', 10],
    'Kaxovskaya'        :[[], '#78CCCD', 11],
    'Butovskaya'        :[[], '#ABBFE0', 12]}

for i in table:
    pos[i] = (float(table[i][3]), float(table[i][2]))
    labels[i] = table[i][4]
    G.add_node(i)
    if len(table[i])==6:
        G.add_edge(table[i][0], table[i][5], weight=int(table[i][1]) )
G.add_edge(76, 73, weight=4)

for b in branch_list:
    branch_list[b][0] = [(u,v) for (u,v,d) in G.edges(data=True)
                                if d['weight'] == branch_list[b][2]]

for i in branch_list:
    nx.draw_networkx_edges(G,pos,edgelist=branch_list[i][0],
                            edge_color=branch_list[i][1], width=2)

nx.draw_networkx_nodes(G,pos,alpha=0.5,node_size=50,node_color='w')

labels_n = {10:labels[10]}
nx.draw_networkx_labels(G,pos,labels=labels_n,
                    font_size=15,font_color='k',font_family='Poiret One')

plt.plot()
plt.figure(1, figuresize=(8,8))
plt.axis('on')
plt.axis([37.3, 37.9, 55.5, 55.95])
plt.grid(True)
plt.title('Московское метро',family='Cambria',size='30')    # настроить вывод названия линии
plt.savefig('metro.png')
plt.show()
