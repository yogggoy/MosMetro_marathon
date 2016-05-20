#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
parse the raw data from wiki, to complete table
"""

import re

table = {}      # table[i] = [№_st, branch, X, Y, name, (direct)]
n_station = 0

f = open(r'data\wiki\metro.txt','r')       # data raw
pars = open('pars.txt','w')     # save to

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
# добавление ребер!! добавить ребро между Киевской и Студенческой
for i in table:
    if table[i][1] == branch_prev:
        if (i != 141) & (i != 74):
            table[i].append(i-1)
    branch_prev = table[i][1]
    if i == 80:
        table[i].append(91)
    pars.write(str(table[i])+'\n')

f.close()
pars.close()