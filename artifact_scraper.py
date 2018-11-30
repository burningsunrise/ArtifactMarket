import urllib.request, json, datetime
import time

url_prefix = "https://steamcommunity.com/market/search/render/?search_descriptions=0&category_583950_Rarity%5B%5D="
url_suffix = "&sort_dir=desc&appid=583950&norender=1&count=500"
url_common = "tag_Rarity_Common"
url_uncommon = "tag_Rarity_Uncommon"
url_rare = "tag_Rarity_Rare"


# Lists
common_name = []
common_sell_price = []
common_card_hash = []
common_sale_listings =[]
uncommon_name = []
uncommon_sell_price = []
uncommon_card_hash = []
uncommon_sale_listings = []
rare_name = []
rare_sell_price = []
rare_card_hash = []
rare_sale_listings = []


def main():
    # commons
    with urllib.request.urlopen(url_prefix + url_common + url_suffix) as url:
        data = json.loads(url.read().decode())

        print("Commons")
    # relevant data name, sale_prince, sell_listings (how many), sell_price, sell_price_text, hash_name
    for commons in data['results']:
        print(commons['name'] + ' $' + str(commons['sell_price']/100))
        common_name.append(commons['name'])
        common_sell_price.append(commons['sell_price']/100)
        common_card_hash.append(commons['hash_name'])
        common_sale_listings.append(commons['sell_listings'])

    # uncommons
    with urllib.request.urlopen(url_prefix + url_uncommon + url_suffix) as url:
        data = json.loads(url.read().decode())

        print('\nUncommons')
    for uncommons in data['results']:
        print(uncommons['name'] + ' $' + str(uncommons['sell_price']/100))
        uncommon_name.append(uncommons['name'])
        uncommon_sell_price.append(uncommons['sell_price']/100)
        uncommon_card_hash.append(uncommons['hash_name'])
        uncommon_sale_listings.append(uncommons['sell_listings'])

    # rares
    with urllib.request.urlopen(url_prefix + url_rare + url_suffix) as url:
        data = json.loads(url.read().decode())
        
        print('\nRares')
    for rares in data['results']:
        print(rares['name'] + ' $' + str(rares['sell_price']/100))
        rare_name.append(rares['name'])
        rare_sell_price.append(rares['sell_price']/100)
        rare_card_hash.append(rares['hash_name'])
        rare_sale_listings.append(rares['sell_listings'])

try:
    while True:
        print("Started polling data!")
        main()
        time.sleep(30)
except KeyboardInterrupt:
    print("Stopped polling data!")