#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pars import parser

link = r'data\wiki\metro.txt'
table = parser(link)

def link_tables(link_action, link_stasion):
    '''
    make pars MetroMarafon-path, and return dict 'path' with format: 
    # path = [№_line, name_line, №_station, name_station, action/color]
    '''
    path = {}
    action = {
        'выход':'r',            # red
        'проезд':'b',           # blue
        'разворот':'#BE00BE',   # pink
        'пересадка':'#FFFF4B'}  # yellow

    ya_action = open(link_action, 'r')
    ya_station = open(link_stasion, 'r')

    for i in range(1,455):  #455
        l = ya_station.readline()[:-1]
        stroka = l.split('.')    # 'ветка', 'название станции'
        for j in table:
            if (stroka[0].lower() == table[j][1].lower() and
               stroka[1].lower() == table[j][3].lower()):
                path[i] = table[j][0:4]
                break
        else:
            print ('!!! ERROR: СТАНЦИЯ или ВЕТКА не найдена. lines:')
            print (r'action.txt line №',i,':',l)
            break

        l = ya_action.readline()[:-1]
        if l in action:
            path[i].append(action[l])
        else:
            print('!!! ERROR: ДЕЙСТВИЯ не совпадают. lines:', i, '-', l)
            break

    ya_action.close()
    ya_station.close()

    return path

def self_test(path):
    st_closed = [x for x in range(1,201)]
    st_open = []

    for i in range(1, 455):
        if path[i][2] in st_closed:
            st_closed.remove(path[i][2])
        if path[i][2] not in st_open:
            st_open.append(path[i][2])

    if len(st_closed)>0 or len(st_open)<200:
        print('WARNING: Что-то пошло не так.',
               'Число посещенных станций не корректно')
        print('число не открытых локаций : ', len(st_closed))
        print('число открытых локаций    : ', len(st_open))

if __name__ == "__main__":
    link_action = r'data\yandex\action.txt'
    link_stasion = r'data\yandex\station.txt'
    path = link_tables(link_action, link_stasion)
    
    self_test(path)
    for i in path:
        print(i, path[i])