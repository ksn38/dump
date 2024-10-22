import requests
import re
import pandas as pd
import webbrowser
import os


title = []
date = []
url = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def mave(*args):
    for i in args:
        print(i)
        response = requests.get(i, headers=headers).text

        l3 = re.findall('[А-я]+.+?\d{4}-\d{2}-\d{2}', str(response))

        for j in l3:
            t = re.findall('^.+?,\"', j)[0][:-3]
            if len(t) < 1000:
                if t[:7] == 'Подкаст':
                    t = re.findall('listenings.+', j)
                    t = re.findall(',\"[А-я].+?\"', str(t))
                    
                    if len(t) > 0:
                        title.append(t[0][2:-1])
                        date.append(j[-10:])
                        url.append(i)
                else:
                    title.append(t)
                    date.append(j[-10:])
                    url.append(i)
            
def podbean(*args):
    for i in args:
        print(i)
        response = requests.get(i, headers=headers).text

        l3 = re.findall('name\":\"[^\"]+?\",\"datePublished\":\"\d{4}-\d{2}-\d{2}', str(response))

        for j in l3:
            if j[7] == '\\':
                title.append(re.findall('\":.+?\"', j)[0][3:-1].encode('utf-8').decode('unicode-escape'))
            else:
                title.append(re.findall('\":.+?\"', j)[0][3:-1])
            date.append(j[-10:])
            url.append(i)
            
mave('https://skillboxcode.mave.digital/', 'https://introvertnakuhne.mave.digital/', 'https://gostudy.mave.digital/', \
'https://economicsoutloud.mave.digital/', 'https://mlpodcast.mave.digital/', 'https://krasnayakomnata.mave.digital/')
podbean('https://learnpython.podbean.com/', 'https://podcast.itbeard.com/', 'https://www.podbean.com/podcast-detail/2y4gr-6dda/Radiolab-Podcast', \
        'https://www.podbean.com/podcast-detail/4u7eq-182c10/The-Rachman-Review-Podcast', \
        'https://www.podbean.com/podcast-detail/2dcw3-5d2c8/Археология-Podcast', \
        'https://www.podbean.com/podcast-detail/g574s-69566/Цитаты-Свободы-Podcast', \
        'https://www.podbean.com/podcast-detail/832bf-5fab8/Newочём-Podcast')
df = pd.DataFrame({"title": title, "date": date, "url": url}).sort_values('date', ascending=False)
df.head(30).to_html("podcasts.html", encoding="utf-8", index=False, render_links=True)

if os.name == "posix":
    webbrowser.open('/home/ksn38/dump/podcasts.html')
