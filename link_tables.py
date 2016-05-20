#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

table = {}
n_station = 0

f = open('data\wiki\metro.txt','r')
ya_action = open('data\yandex\ction.txt','r')
ya_station = open('data\yandex\station.txt','r')

for i in range(1850):
    line = f.readline()[:-1]
    if re.match(r'\|-', line):
        if n_station:
            table[n_station] = [n_station, branch, '', '', name]
        n_station = n_station+1
    if re.match(r'\| style', line):
        branch = re.findall(r'/цвет линии\|(\d+)', line)[0]
    if re.match(r'\| {{coord', line):        
        name = re.findall(r'name=(.*)\|nogoogle', line)[0]
        name = re.sub(r' [(].*','', name)
        name = re.sub(r'ё','е', name)
        name = re.sub(r'Ё','Е', name)
#==============================================================================
# table[i] = [n_station, branch, '', '', name]
#                 _0_     _1_    2    3  _4_
patch = {}
action = {
    'выход':'r',
    'проезд':'b',
    'разворот':'#BE00BE',
    'пересадка':'#FFFF4B'}

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

for i in range(1,455):  #455
    line = ya_station.readline()[:-1]
    stroka = line.split('.')    # ветка, название станции
    for j in table:
        if stroka[1].lower() == table[j][4].lower():
            patch[i] = [table[j][0]]
            break
    else:
        print ('!!! ERROR: имена СТАНЦИЙ не совпадают. lines:',i)
    for j in branch_list:
        if stroka[0].lower() == branch_list[j][2].lower():
            patch[i].append(j)
            break
    else:
        print('!!! ERROR: имена ВЕТОК не совпадают. lines:',i)
    patch[i].extend(stroka)

    line = ya_action.readline()[:-1]

    if line in action:
        patch[i].append(action[line])
    else:
        print('!!! ERROR: ДЕЙСТВИЯ не совпадают. lines:',i)

for i in patch:
    print(patch[i])

f.close()
ya_action.close()
ya_station.close()