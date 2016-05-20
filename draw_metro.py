#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import rcParams
import matplotlib.pyplot as plt 
import networkx as nx
import re

rcParams['figure.figsize'] = (10, 10)
rcParams['figure.subplot.left'] = 0.05
rcParams['figure.subplot.right'] = 0.95
rcParams['figure.subplot.bottom'] = 0.05
rcParams['figure.subplot.top'] = 0.95
rcParams['figure.subplot.wspace'] = 0
rcParams['figure.subplot.hspace'] = 0
rcParams['axes.grid'] = True

#==============================================================================
table = {}      # table = [№_st, branch, X, Y, name, (direct)]
n_station = 0
f = open(r'data\wiki\metro.txt', 'r')       # data raw from wikipedia

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
        name = re.sub(r' [(].*','', name)
        name = re.sub(r'ё','е', name)
        name = re.sub(r'Ё','Е', name)
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
ya_action = open(r'data\yandex\action.txt', 'r')
ya_station = open(r'data\yandex\station.txt', 'r')

patch = {}    # [№_station, №_branch, name_branch, name_station, action/color]
action = {
    'выход':'r',            # red
    'проезд':'b',           # blue
    'разворот':'#BE00BE',   # pink
    'пересадка':'#FFFF4B'}  # yellow

branch_list = {
    1  :[[], '#EE2E22', 'Сокольническая'            ],
    2  :[[], '#47B85E', 'Замоскворецкая'            ],
    3  :[[], '#0077BF', 'Арбатско-Покровская'       ],
    4  :[[], '#1AC1F3', 'Филевская'                 ],
    5  :[[], '#884E35', 'Кольцевая'                 ],
    6  :[[], '#F48232', 'Калужско-Рижская'          ],
    7  :[[], '#8D479B', 'Таганско-Краснопресненская'],
    8  :[[], '#FECB2F', 'Калининская'               ],
    9  :[[], '#A0A2A3', 'Серпуховско-Тимирязевская' ],
    10 :[[], '#B3D345', 'Люблинско-Дмитровская'     ],
    11 :[[], '#78CCCD', 'Каховская'                 ],
    12 :[[], '#ABBFE0', 'Бутовская'                 ]}

for i in range(1, 455):  #455
    line = ya_station.readline()[:-1]
    stroka = line.split('.')    # ветка, название станции
    for j in table:
        if stroka[1].lower() == table[j][4].lower():
            patch[i] = [table[j][0]]
            break
    else:
        print ('!!! ERROR: имена СТАНЦИЙ не совпадают. lines:', i)
    for j in branch_list:
        if stroka[0].lower() == branch_list[j][2].lower():
            patch[i].append(j)
            break
    else:
        print('!!! ERROR: имена ВЕТОК не совпадают. lines:', i)
    patch[i].extend(stroka)
    line = ya_action.readline()[:-1]
    if line in action:
        patch[i].append(action[line])
    else:
        print('!!! ERROR: ДЕЙСТВИЯ не совпадают. lines:', i)

ya_action.close()
ya_station.close()
#==============================================================================

# table[i] = [№_station, №_branch, X, Y, name_station, (direct)]
# patch[i] = [№_station, №_branch, name_branch, name_station, action/color]
G=nx.Graph()
pos = {}
labels = {}

for i in table:
    pos[i] = (float(table[i][3]), float(table[i][2]))
    G.add_node(i)
    if len(table[i])==6:
        G.add_edge(table[i][0], table[i][5], weight=int(table[i][1]) )
G.add_edge(76, 73, weight=4)
for b in branch_list:
    branch_list[b][0] = [(u, v) for (u, v, d) in G.edges(data=True)
                                if d['weight'] == b]

# patch[i] = [№_station, №_branch, name_branch, name_station, action/color]
st_closed = [x+1 for x in range(200)]
st_open = []

for i in range(1, 455):
    plt.axis('on')
    plt.axis([37.3, 37.9, 55.5, 55.95])
    for b in branch_list:
        nx.draw_networkx_edges(G, pos, edgelist=branch_list[b][0],
                            edge_color=branch_list[b][1], width=2)
    if patch[i][0] in st_closed:
        st_closed.remove(patch[i][0])
    if patch[i][0] not in st_open:
        st_open.append(patch[i][0])
    nx.draw_networkx_nodes(G, pos, alpha=0.75, node_size=50,
                            node_color='w', linewidths=0.5,
                            node_shape='p', nodelist=st_closed)
    nx.draw_networkx_nodes(G, pos, alpha=0.75, node_size=50,
                            node_color='g', linewidths=0.5,
                            node_shape='p', nodelist=st_open)
    nx.draw_networkx_nodes(G, pos, alpha=0.75, node_size=45,
                            node_color=patch[i][4], linewidths=1,
                            node_shape='p', nodelist=[patch[i][0]])
                            # so^>v<dph8

    st_name = patch[i][3]
    plt.text (pos[patch[i][0]][0], pos[patch[i][0]][1]+0.003,
            st_name, family='Poiret One', size=17)
    plt.text ( 37.32, 55.52,
            st_name, family='Poiret One', size=20)            
    title = patch[i][2]
    plt.title(title,family='Cambria', size='30', color='k')
    plt.savefig(r'frames\metro'+str(i)+'.png')
    if i< 454:
        plt.clf()
print(st_closed)

plt.show()


