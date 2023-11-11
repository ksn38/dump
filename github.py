import requests
import json
import time


#followers = [i['login'] for i in json.loads(requests.get('https://api.github.com/users/ksn38/followers?per_page=100').text)]
#following = [i['login'] for i in json.loads(requests.get('https://api.github.com/users/ksn38/following?per_page=100').text)]

followers = []

i = 0
while(True):
    followers_req = requests.get('https://api.github.com/users/ksn38/followers?page=' + str(i)).text
    if len(followers_req) > 3:
        followers.extend([i['login'] for i in json.loads(followers_req)])
        i += 1
    else:
        break

following = []

i = 0
while(True):
    following_req = requests.get('https://api.github.com/users/ksn38/following?page=' + str(i)).text
    if len(following_req) > 3:
        following.extend([i['login'] for i in json.loads(following_req)])
        i += 1
    else:
        break

unfollow = set(following) - set(followers)
follow = (set(followers) - set(following))

for i in unfollow:
    if i != "ArtemOnigiri":
        print('-', i)

for i in follow:
	if i != "anaselgarhy":
		print('+', i)
