#!/usr/bin/python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib.request, json, datetime
import pprint
from collections import Counter

# Lists
market_name = []
sell_price = []
card_hash = []
sale_listings =[]


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

def get_market_data():
    global market_name
    global sell_price
    global card_hash
    global sale_listings
    url_prefix = "https://steamcommunity.com/market/search/render/?search_descriptions=0&category_583950_Rarity%5B%5D="
    url_suffix = "&sort_dir=desc&appid=583950&norender=1&count=500"
    url_common = "tag_Rarity_Common"
    url_uncommon = "tag_Rarity_Uncommon"
    url_rare = "tag_Rarity_Rare"
    # commons
    with urllib.request.urlopen(url_prefix + url_common + url_suffix) as url:
        data = json.loads(url.read().decode())

    # relevant data name, sale_prince, sell_listings (how many), sell_price, sell_price_text, hash_name
    for commons in data['results']:
        market_name.append(commons['name'])
        sell_price.append(commons['sell_price']/100)
        card_hash.append(commons['hash_name'])
        sale_listings.append(commons['sell_listings'])

    # uncommons
    with urllib.request.urlopen(url_prefix + url_uncommon + url_suffix) as url:
        data = json.loads(url.read().decode())

    for uncommons in data['results']:
        market_name.append(uncommons['name'])
        sell_price.append(uncommons['sell_price']/100)
        card_hash.append(uncommons['hash_name'])
        sale_listings.append(uncommons['sell_listings'])

    # rares
    with urllib.request.urlopen(url_prefix + url_rare + url_suffix) as url:
        data = json.loads(url.read().decode())

    for rares in data['results']:
        market_name.append(rares['name'])
        sell_price.append(rares['sell_price']/100)
        card_hash.append(rares['hash_name'])
        sale_listings.append(rares['sell_listings'])

def main():
    print("Welcome to the pricer!\n")
    compare = input("Use your steam invetory as a base? (Y/n): ")
    if compare.lower() != 'n' or compare.lower() != 'no':
        steam_inventory = input("Give me your steam name: ")

    if len(steam_inventory) != 0:
        with urllib.request.urlopen('https://steamcommunity.com/id/'+steam_inventory+'/inventory/json/583950/2') as url:
            inventory_data = json.loads(url.read().decode())
    desc_name =[]
    for data in inventory_data['rgDescriptions']:
        desc_name.append(data)

    rg_name = []
    for data in inventory_data['rgInventory']:
        rg_name.append(data)

    # inventory shit
    inventory_name = []
    inventory_hash = []
    inventory_classid = []
    for i in range(len(inventory_data['rgDescriptions'])):
        inventory_name.append(inventory_data['rgDescriptions'][desc_name[i]]['name'])
        inventory_hash.append(inventory_data['rgDescriptions'][desc_name[i]]['market_hash_name'])
        inventory_classid.append(inventory_data['rgDescriptions'][desc_name[i]]['classid'])

    rg_classid = []
    for i in range(len(inventory_data['rgInventory'])):
        rg_classid.append(inventory_data['rgInventory'][rg_name[i]]['classid'])


    count_rgclassid = dict(Counter(rg_classid))
    inventory_deck = dict(zip(inventory_classid, inventory_name))

    final_inventory = {}
    for k,v in count_rgclassid.items():
        if k in inventory_deck:
            final_inventory[inventory_deck[k]] = v




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

    get_market_data()
    
    dict_with_ints = dict((k,int(v)) for k,v in deck.items())

    compared_decks = {x: dict_with_ints[x] - final_inventory[x] for x in dict_with_ints if x in final_inventory}

    for key,value in dict_with_ints.items():
        if key in compared_decks:
            pass
        else:
            compared_decks[key] = value

    finalized_deck = { k:v for k, v in compared_decks.items() if v > 0} # removes all False values, might want to change to if v != 0 or v > 0
    total = 0
    for i in range(len(card_hash)):
        if card_hash[i] in heroes and card_hash[i] not in inventory_hash:
            print(market_name[i] + '=$' + str(sell_price[i]))
            total += float(sell_price[i])
        if market_name[i] in finalized_deck:
            print(market_name[i] + ' x' + str(finalized_deck[market_name[i]]) + '=$' + str(round(float(finalized_deck[market_name[i]]) * float(sell_price[i]), 2)) + ' | SINGLE PRICE=$' + str(sell_price[i]))
            total += round(float(finalized_deck[market_name[i]]) * float(sell_price[i]),2)
        


    print('=================')
    print("Total Deck Cost: " + str(total))

if __name__ == "__main__":
    main()