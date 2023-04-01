from bs4 import BeautifulSoup
from urllib import parse
from typing import Dict
import datetime as dt
import pandas as pd
import user_agent
import requests
    
def transform_symbol_to_yahoo_url(symbol: str) -> str:
    
    if '=' not in list(symbol):
        quoted_symbol = parse.quote(symbol)
    else:
        quoted_symbol = symbol
    url = f'https://finance.yahoo.com/quote/{quoted_symbol}?p={quoted_symbol}&.tsrc=fin-srch'    
    
    return url

def format_change(change: str):
    
    change_nmb = float(change)
    if change_nmb > 0:
        change_fmt = f'+{round(change_nmb, 2)}%'
    else:
        change_fmt = f'{round(change_nmb, 2)}%'
        
    return change_fmt
        

def format_price(price: str, symbol: str):
        
    price_nmb = round(float(price), 2)
    price_fmt = "{:,}".format(price_nmb)\
        .replace(',','$$$$')\
        .replace('.',',')\
        .replace('$$$$', '.')
    
    if symbol == 'BTC-USD' or \
       symbol == 'CL=F' or \
       symbol == 'GC=F' or \
       symbol == 'ETH-USD':
           
        price_fmt = f'USD {price_fmt}'
        
    elif symbol == '^BVSP' or \
        symbol == '^GSPC':
        price_fmt = f'{price_fmt} pts'
        
    else: # 'BRL=X'
        price_fmt = f'R$ {price_fmt}'
        
    return price_fmt

def format_arrow_test(change: str):
    
    change = float(change)
    if change == 0:
        test = 'white_bar'
    elif change > 0:
        test = 'green'
    else: # change < 0
        test = 'red'
        
    return test
    
def format_image(symbol: str):
    
    if symbol == '^BVSP' or \
        symbol == '^GSPC' or \
        symbol == 'BRL=X':
        image = 'image1'
        
    else:
        image = 'image3'
        
    return image
    
def get_price_and_change_from_request(symbol: str) -> Dict[str, str]:
    
    url = transform_symbol_to_yahoo_url(symbol)
    response = requests.get(url, headers={'user-agent' : user_agent.generate_user_agent()})
    soup = BeautifulSoup(response.content, 'html.parser')
    list_data = [x for x in soup.find_all('fin-streamer', {'data-symbol' : symbol})]

    price = list_data[0]['value']
    change = list_data[2]
        
    if 'data-pricehint' in change.attrs and change['data-pricehint'] == '2':
        change = str(float(change['value']) * 100)
    
    else:
        change = change['value']

    return {'price' : format_price(price, symbol),
            'change' : format_change(change),
            'image' : format_image(symbol),
            'test' : format_arrow_test(change)}


def format_index_data() -> pd.DataFrame:

    list_symbol = ['^BVSP', '^GSPC', 'BRL=X', 'BTC-USD', 'ETH-USD', 'CL=F', 'GC=F']
    dict_index = {}
    for symbol in list_symbol:
        dict_index[symbol] = get_price_and_change_from_request(symbol)
    
    data = pd.DataFrame(dict_index).T
    
    return data
