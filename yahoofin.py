import os
from datetime import date
from datetime import timedelta
from collections import OrderedDict
from bs4 import BeautifulSoup as bs
import requests
import time

def ticks(*args):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    t_dict = OrderedDict()

    for i in (args):
        if i not in {'wti', 'gold', 'sz', 'wheat', 'ss', 'cop'}:
            url = 'https://finance.yahoo.com/quote/^' + i + '/history'
        else:
            commodities = {'wti': 'CL=F', 'gold': 'GC=F', 'wheat': 'KE=F', 'sz': '399001.SZ', 'ss': '000001.SS', 'cop': 'HG=F'}
            url = 'https://finance.yahoo.com/quote/' + commodities[i] + '/history'
            
        response = requests.get(url, headers=headers).text
        parsed_html = bs(response, 'lxml')
        #print(parsed_html)
        t = parsed_html.find('fin-streamer', {'class': 'livePrice yf-1i5aalm'}).text.replace(',', '')
        print(t)
        f = open("gspc.txt", "w", encoding="utf-8")
        f.write(response)
        f.close()
        #t_dict[i] = float(t)

    return t_dict
    
print(ticks('wti'))
