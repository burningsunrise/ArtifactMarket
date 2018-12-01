#!/usr/bin/python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request, json, datetime

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

print("Welcome to the pricer!\n")
deck_list = input("Give me that deck!: ")
raw_html = simple_get(deck_list)

html = BeautifulSoup(raw_html, 'html.parser')

names = html.findAll("div", {'class': 'cardName'}, text=True)
card_counts = html.findAll("div", {'class': 'cardCount'}, text=True)
hash_names = html.findAll("div", {"class" : lambda L: L and L.startswith('hero color')})

name = []
count = []
heroes = []
for name_text in names:
    name.append(name_text.text)

for card_count in card_counts:
    count.append(card_count.text.split('x')[1])

for hash_name in hash_names:
    heroes.append("1" + hash_name.get('id').split('card')[1])

deck = dict(zip(name, count))

with urllib.request.urlopen("https://pareidolia.vision/artifact/card_data.php") as url:
    data = json.loads(url.read().decode())

total = 0
for cards in data:
    if cards['hash_name'] in heroes:
        print(cards['name'] + '=$' + cards['sell_price'])
        total += float(cards['sell_price'])
    if cards['name'] in deck:
        print(cards['name'] + ' x' + deck[cards['name']] + '=$' + str(round(float(deck[cards['name']]) * float(cards['sell_price']), 2)) + ' | SINGLE PRICE=$' + cards['sell_price'])
        total += round(float(deck[cards['name']]) * float(cards['sell_price']),2)

print('=================')
print("Total Deck Cost: " + str(total))
