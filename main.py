import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'iphone'

def get_data(searchterm):
    url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={searchterm}&_sacat=0&LH_PrefLoc=1&LH_Auction=1&rt=nc&LH_Sold=1&LH_Complete=1'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('£','').replace('$','').replace(',','').strip()),
            'solddate': item.find('div', {'class': 's-item__title--tag'}).find('span', {'class':'POSITIVE'}).text if item.find('div', {'class': 's-item__title--tag'}) is not None else None,
            'bids': item.find('span', {'class': 's-item__bids s-item__bidCount'}).text if item.find('span', {'class': 's-item__bids s-item__bidCount'}) is not None else None,
            'link': item.find('a', {'class': 's-item__link'})['href']
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)
