from bs4 import BeautifulSoup
from typing import Dict, List
import pandas as pd
import requests


def request_high_and_low_html() -> BeautifulSoup:
    
    url = 'https://economia.uol.com.br/cotacoes/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def extract_high_and_low_stocks(soup: BeautifulSoup) -> Dict[List, str]:
    
    # Esta lista, contém o nome de TODOS os ativos do site.
    stocks = ([my_tag.text for my_tag in soup.find_all('td', class_ = "title")])
    
    # Na ordem, apartir do nº 12 aparece as ações em alta
    h_stocks = [x for x in stocks[12:15]]
    
    # Na ordem, apartir do nº  aparece as ações em baixa.
    l_stocks = [x for x in stocks[17:20]]
    
    return {'high' : h_stocks,
            'low' : l_stocks}
  
def extract_stock_change(stock: str, soup: BeautifulSoup):
    
    string_list = str([my_tag.text.replace('\s', '').strip() for my_tag\
        in soup.find_all('section', class_ = "stock-rankings")])
    
    cleaning_process1 = string_list.replace("R$"," ")
    cleaning_process2 = str(cleaning_process1).split(stock)

    change = cleaning_process2[1]
    if change[2] == '%':
        return change[0:2] + ',00%'
    if change[3] == '%':
        return change[0:3] + ',00%'
    if change[5] == '%':
        return change[0:6]
    elif change[6] == '%':
        return change[0:7]
    elif change[7] == '%':
        return change[0:8]
    else:
        return change[0] + change[1] + change[2] + change[3] + '0' +change [4] + change[5] 

def test_change_high(change_stockn):
    # função para testar e corrigir parâmetro
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		return change_stockn
	else:
		change_stockn2 = ' ' 
		return change_stockn2

def test_change_low(change_stockn):
    # função para testar e corrigir parâmetro
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		return change_stockn
	else:
		change_stockn2 = ' ' 
		return change_stockn2

def test_ticket_high(ticket_stockn, change_stockn):
    # função para testar e corrigir parâmetro
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		return ticket_stockn
	else:
		ticket_stockn = ' '
		return ticket_stockn

def test_ticket_low(ticket_stockn, change_stockn):
    # função para testar e corrigir parâmetro
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		return ticket_stockn
	else:
		ticket_stockn = ' '
		return ticket_stockn

def arrow_green_or_not(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		test = 'green'
		return test
	else:
		test = 'white_bar'
		return test

def arrow_red_or_not(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		test = 'red'
		return test
	else:
		test = 'white_bar'
		return test

def format_stocks_data() -> Dict[str, Dict[str, str]]:
    
    soup = request_high_and_low_html()
    dict_stocks = extract_high_and_low_stocks(soup)
    data = {}
    for position in dict_stocks:  
        for stock in dict_stocks[position]:
            stock_fmt = stock.split('.SA')[0]
            change = extract_stock_change(stock, soup)
            if position == 'low':
                stock_fmt = test_ticket_low(stock_fmt, change)
                test = arrow_red_or_not(change)
                data[stock_fmt] = {'change' : test_change_low(change), 
                                   'position' : position,
                                   'test' : test}
            else: # high
                test = arrow_green_or_not(change)
                stock_fmt = test_ticket_high(stock_fmt, change)
                data[stock_fmt] = {'change' : test_change_high(change), 
                                   'position' : position,
                                   'test' : test}
    
    data = pd.DataFrame(data).T
    
    return data

