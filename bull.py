import os
import re
import pandas as pd
from datetime import date
from datetime import timedelta

today = date.today().strftime("%y%m%d")
yesterday = date.today() - timedelta(1)
yesterday = yesterday.strftime("%y%m%d")

files = os.listdir("D:\\Temp")

telegrams = []
for f in files:
    if re.search(today, f) or re.search(yesterday, f):
        print(f)
        telegrams.extend(open("D:\\Temp\\" + f, 'r').read().replace('\n', ' ').split('='))

indexes = ['Ветлуга', 'Шахунья', 'Красные Баки', 'Воскресенское', 'Семенов', 'Волжская Гмо', 'Дзержинск', \
'Нижний Новгород', 'Нижний Новгород (АМСГ)', 'Лысково', 'Павлово', 'Выкса', 'Дальнее Константиново', 'Арзамас', \
'Сергач', 'Лукоянов', 'Большое Болдино']

bull = pd.DataFrame(columns=["t max","t min","t ср", "ос день", "ос ночь", "ветер д", "ветер н", "t почвы", "t 2cm"], index=indexes)

def replace_sign(t):
    t = re.sub('^00|^0', '+' ,t)
    t = re.sub('^10|^1', '-' ,t)
    return t

for i in telegrams:
    if len(i) > 2:
        i = re.sub('^\s+', '' ,i)
        index = re.findall('^\w+\s\w+\s\(\w+\)|^\w+\s\w+|^\w+', i)
        t_max = re.findall('333\s1\w{,4}', i)
        if len(t_max) > 0:
            bull.at[index, "t max"] = replace_sign(t_max[0][-4:])
        t_min = re.findall('333\s2\w{,4}', i)
        if len(t_min) > 0:
            bull.at[index, "t min"] = replace_sign(t_min[0][-4:])
        t_med = re.findall('555\s50\w{,4}|555\s51\w{,4}', i)
        if len(t_med) > 0:
            bull.at[index, "t ср"] = replace_sign(t_med[0][-4:])
        wind_d = re.findall('15:00.+\s53\w{,3}', i)
        if len(wind_d) > 0:
            bull.at[index, "ветер д"] = wind_d[0][-2:]
        wind_n = re.findall('03:00.+\s53\w{,3}', i)
        if len(wind_n) > 0:
            bull.at[index, "ветер н"] = wind_n[0][-2:]
        prec_d = re.findall('15:00.+\s6\w{,3}2', i)
        if len(prec_d) > 0:
            bull.at[index, "ос день"] = prec_d[0][-4:-1]
        prec_n = re.findall('03:00.+\s6\w{,3}2', i)
        if len(prec_n) > 0:
            bull.at[index, "ос ночь"] = prec_n[0][-4:-1]
        t_gr = re.findall('333\s\w+\s31\w{,3}|333\s\w+\s30\w{,3}', i)
        if len(t_gr) > 0:
            bull.at[index, "t почвы"] = replace_sign(t_gr[0][-3:])
        cm = re.findall('555\s52\w{,3}', i)
        if len(cm) > 0:
            bull.at[index, "t 2cm"] = replace_sign(cm[0][-3:])
            
bull.to_html("bull.html")