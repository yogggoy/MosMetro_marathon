#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from matplotlib import rcParams
import matplotlib.pyplot as plt
import networkx as nx
from pars import lines_list
from link_tables import link_tables, table
from progress_bar_cmd import bar

rcParams['figure.figsize'] = (10, 10)
rcParams['figure.subplot.left'] = 0.05
rcParams['figure.subplot.right'] = 0.95
rcParams['figure.subplot.bottom'] = 0.05
rcParams['figure.subplot.top'] = 0.95
rcParams['figure.subplot.wspace'] = 0
rcParams['figure.subplot.hspace'] = 0
rcParams['axes.grid'] = True

def draw_nodes(color, lw, n_list):
        nx.draw_networkx_nodes(G, pos, alpha=0.75, node_size=50,
                                node_color=color, linewidths=lw,
                                node_shape='p', nodelist=n_list)

def draw_legend(color, node, text=False):
    pos_label = {
        201:(37.71, 55.58),
        202:(37.71, 55.56),
        203:(37.71, 55.54),
        204:(37.71, 55.52)}
    if text:
        plt.text (pos_label[201][0]+0.02,
                pos_label[201][1]-0.0025,
                'выход', family='Poiret One', size=17)
        plt.text (pos_label[202][0]+0.02,
                pos_label[202][1]-0.0025,
                'проезд', family='Poiret One', size=17)
        plt.text (pos_label[203][0]+0.02,
                pos_label[203][1]-0.0025,
                'разворот', family='Poiret One', size=17)
        plt.text (pos_label[204][0]+0.02,
                pos_label[204][1]-0.0025,
                'пересадка', family='Poiret One', size=17)
    nx.draw_networkx_nodes(G, pos_label, alpha=1, node_size=85,
                            node_color=color, linewidths=1.5,
                            node_shape='p', nodelist=[node])


link_action = r'data\yandex\action.txt'
link_stasion = r'data\yandex\station.txt'
patch = link_tables(link_action, link_stasion)

#=============================================================================
# table[i] = [№_line, name_line, №_st, name_st, x_st, y_st, (link)]
# patch[i] = [№_line, name_line, №_station, name_station, action/color]

G=nx.Graph()
pos = {}

for i in table:
    G.add_node(i)
    if len(table[i])==7:
        G.add_edge(i, table[i][6], weight=table[i][0])
    pos[i] = (float(table[i][5]), float(table[i][4]))

G.add_edge(76, 73, weight=4)    # развилка
node_labels = [201,202,203,204] # легенда
G.add_nodes_from(node_labels)

for b in lines_list:
    lines_list[b][0] = [(u, v) for (u, v, d) in G.edges(data=True)
                                if d['weight'] == b]

st_closed = [x for x in range(1,201)]
st_open = []

try:
    os.mkdir("frames")
except:
    pass

frames = 455
for i in range(1, frames): #455
    bar(i, frames-1)
    if patch[i][2] in st_closed:
        st_closed.remove(patch[i][2])
    if patch[i][2] not in st_open:
        st_open.append(patch[i][2])

    plt.axis('on')
    plt.axis([37.3, 37.9, 55.5, 55.95])
    for b in lines_list:
        nx.draw_networkx_edges(G, pos, edgelist=lines_list[b][0],
                            edge_color=lines_list[b][1], width=2)

    draw_nodes('w', 0.5, st_closed)
    draw_nodes('g', 0.5, st_open)
    draw_nodes(patch[i][4], 1.0, [patch[i][2]])

    draw_legend('r', 201)
    draw_legend('b', 202)
    draw_legend('#BE00BE', 203)
    draw_legend('#FFFF4B', 204, True)

    plt.text (pos[patch[i][2]][0], pos[patch[i][2]][1]+0.003,
            patch[i][3], family='Poiret One', size=17)
    plt.text (37.32, 55.52,
            patch[i][3], family='Poiret One', size=20)
    plt.title(patch[i][1], family='Cambria', size='30', color='k')
    plt.savefig(r'frames\metro'+str(i)+'.png')
    if i< 454:
        plt.clf()

print('complete. now run `render_gif.py`')
plt.show()