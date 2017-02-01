#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
parse the raw data from wiki, to complete table
"""
import re

lines_list = {
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

def parser(raw_patch):
    '''
    make pars from wiki data, and return dict 'table' with format: 
    table[i] = [№_line, name_line, №_st, name_st, x_st, y_st, (link)]
    # внимание!! при построении графа - добавить ребро на развилку
    # между Киевской и Студенческой
    '''
    table = {}
    num_st = 0
    # f = open(raw_patch, 'r')
    with  open(raw_patch, 'r') as f:
        for i in range(1850):
            l = f.readline()[:-1]
            if re.match(r'\|-', l):
                if num_st:
                    table[num_st] = [num_line, name_line, num_st, name_st, x, y]
                num_st = num_st+1
            if re.match(r'\| style', l):
                num_line = int(re.findall(r'/цвет линии\|(\d+)', l)[0])
                name_line = lines_list[num_line][2]
            if re.match(r'\| {{coord', l):
                name_st = re.findall(r'name=(.*)\|nogoogle', l)[0]
                name_st = re.sub(r' [(].*', '', name_st)
                name_st = re.sub(r'ё', 'е', name_st)
                x, y = re.findall(r'(\d{2}.\d{4})', l)

        line_prev = 0
        for i in range(1, len(table)+1):
            if table[i][0] == line_prev:
                if (i != 141)&(i != 74): # разрывы на ветках
                    table[i].append(i-1)
            line_prev = table[i][0]
            if i == 80:
                table[i].append(91)     # замыкание кольцевой

    # f.close()
    return table

if __name__ == "__main__":
    patch = r'data\wiki\metro.txt'
    table = parser(patch)

    for i in range(1, len(table)+1):
        print(table[i])

    pars = open('pars.txt', 'w')     # save to
    for i in table:
        pars.write(str(table[i])+'\n')
    pars.close()