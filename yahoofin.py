import os
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup as bs
import requests
import re

urli = 'https://finance.yahoo.com/markets/world-indices/'
urlt = 'https://finance.yahoo.com/markets/bonds/'
regi = '\" data-field=\"regularMarketPrice\" data-trend=\"none\" data-pricehint=\"2\" data-value=\"\d*\.\d*\" active'
regt = '\" data-field=\"regularMarketPrice\" data-trend=\"none\" data-pricehint=\"4\" data-value=\"\d*\.\d*\" active'
        
def ticks(url, reg, *args):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    
    d = dict()
    response = requests.get(url, headers=headers).text

    for i in (args):
        x = re.findall(i + reg, response)
        if i != '000001.SS':
            d[str.lower(i)] = float(re.findall('\d+\.\d+', str(x))[0])
        else:
            d['ss'] = float(re.findall('\d+\.\d+', str(x))[0])

    return d

def trec():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    d = dict()
    
    response = requests.get('https://tradingeconomics.com/commodities', headers=headers).text
    parsed_html = bs(response, 'lxml')
    
    for i in ('CL1:COM', 'W 1:COM', 'HG1:COM', 'XAUUSD:CUR'):
        t = parsed_html.find('tr', {'data-symbol': i}).text
        t = ' '.join(t.split())
        name = re.findall('^\w+', t)
        val = re.findall('\d+\.\d+', t)[0]
        if name[0] != 'Crude':
            d[str.lower(name[0])] = float(val)
        else:
            d['wti'] = float(val)

    return d
    
t_dict = dict()    
t_dict.update(ticks(urli, regi, 'GSPC', 'IXIC', 'RUT', 'VIX', 'GDAXI', 'BVSP', '000001.SS', 'BSESN'))
t_dict.update(ticks(urlt, regt, 'TNX'))
t_dict.update(trec())
print(t_dict)
