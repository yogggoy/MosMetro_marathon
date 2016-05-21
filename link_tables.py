#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pars import parser

link = r'data\wiki\metro.txt'
table = parser(link)

def link_tables(link_action, link_stasion):
    '''
    # NEW patch = [№_line, name_line, №_station, name_station, action/color]
    '''
    patch = {}
    action = {
        'выход':'r',            # red
        'проезд':'b',           # blue
        'разворот':'#BE00BE',   # pink
        'пересадка':'#FFFF4B'}  # yellow

    ya_action = open(link_action, 'r')
    ya_station = open(link_stasion, 'r')

    for i in range(1,455):  #455
        l = ya_station.readline()[:-1]
        stroka = l.split('.')    # ветка, название станции
        for j in table:
            if (stroka[0].lower() == table[j][1].lower() and
               stroka[1].lower() == table[j][3].lower()):
                patch[i] = table[j][0:4]
                break
        else:
            print ('!!! ERROR: СТАНЦИЯ или ВЕТКА не найдена. lines:',i)
            print (r'action.txt line №',i,':',l)
            break

        l = ya_action.readline()[:-1]
        if l in action:
            patch[i].append(action[l])
        else:
            print('!!! ERROR: ДЕЙСТВИЯ не совпадают. lines:', i)
            break

    ya_action.close()
    ya_station.close()
    
    return patch

def self_test(patch):
    st_closed = [x for x in range(1,201)]
    st_open = []

    for i in range(1, 455):
        if patch[i][2] in st_closed:
            st_closed.remove(patch[i][2])
        if patch[i][2] not in st_open:
            st_open.append(patch[i][2])

    if len(st_closed)>0 or len(st_open)<200:
        print('WARNING: Что-то пошло не так.',
               'Число посещенных станций не корректно')
        print('число не открытых локаций : ', len(st_closed))
        print('число открытых локаций    : ', len(st_open))

if __name__ == "__main__":
    link_action = r'data\yandex\action.txt'
    link_stasion = r'data\yandex\station.txt'
    patch = link_tables(link_action, link_stasion)
    
    self_test(patch)
    for i in patch:
        print(i, patch[i])