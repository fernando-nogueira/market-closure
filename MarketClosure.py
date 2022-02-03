import re
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
import PIL
import time
import os

path = str(os.getcwd()).replace("\\","/")
# Pegar o dia de hoje, checar se for segunda descontar 3 dias, se for outro dia descontar 1, criando a variável 'ontem'
today = dt.datetime.today()
if today.strftime('%A') == "Monday":
   yesterday = today - dt.timedelta(days=3)
else:
    yesterday = today - dt.timedelta(days=1)
date = [yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')]

# Lista de Ativos
    # Ibovespa, S&P500 e BRL-USD
    # Top 3 stocks positivo e top 3 stocks negativo
    # BTC-USD, ETH-USD, Brent Oil e Gold

assets = ['^BVSP', '^GSPC', 'BRL=X', 'BTC-USD', 'ETH-USD', 'CL=F', 'GC=F']

# 'sinal x,xx %' - Todos os retornos
# 'valor + pts(sem casa decimal)' - Ibov e S&P500
# 'R$ valor (2 casas decimais) ' - Real
# 'USD valor (2 casas decimais) '- Bitcoin/Ethereum/Ouro/Petróleo

def assets_data(asset, date):
    df = pdr.get_data_yahoo(asset, start=date[0], end=date[1])
    if asset[0] == '^':
        price = int(df['Close'].iloc[1])
    else:
        price = round(round(df['Close'].iloc[1], 2),2)
    returns = round(((price / df['Close'].iloc[0]) - 1) * 100, 2)
    if returns > 0:
        signal = '+'
    else:
        signal = ''
    returns = signal + str(returns).replace(".", ",")
    if asset[0] == '^':
        price = f"{price:,d}".replace(",", ".")
    else: 
        price = '{:,.2f}'.format(price).replace(",",".")
        price = list(price)
        price[-3] = ','
        price = ''.join(price)
        #str(price).replace(".", ",")
    return {'price':price,'returns':returns}


price_ibov =  assets_data(assets[0], date)['price'] + ' pts'
change_ibov = assets_data(assets[0], date)['returns'] + '%'

price_sp =  assets_data(assets[1], date)['price'] + ' pts'
change_sp = assets_data(assets[1], date)['returns'] + '%'

price_dolar = 'R$ ' + assets_data(assets[2], date)['price']
change_dolar = assets_data(assets[2], date)['returns'] + '%'

price_btc = 'USD ' + assets_data(assets[3], date)['price']
change_btc = assets_data(assets[3], date)['returns'] + '%'

price_eth = 'USD ' + assets_data(assets[4], date)['price']
change_eth = assets_data(assets[4], date)['returns'] + '%'

price_oil = 'USD ' + assets_data(assets[5], date)['price']
change_oil = assets_data(assets[5], date)['returns'] + '%'

price_gold = 'USD ' + assets_data(assets[6], date)['price']
change_gold = assets_data(assets[6], date)['returns'] + '%'

# Fontes não funcionando
montserrat_giant = ImageFont.truetype("Montserrat-Regular.otf", 70)
montserrat_extrabold = ImageFont.truetype("Montserrat-ExtraBold.otf", 70)
montserrat_small = ImageFont.truetype("Montserrat-Regular.otf", 60)

# Biblioteca PIL
image = Image.open(path + '/Template/image.png')
image2 = Image.open(path + '/Template/image2.png')
image3 = Image.open(path + '/Template/image3.png')
arrow_green = Image.open(path + '/Template/green_arrow.png')
arrow_red = Image.open(path + '/Template/red_arrow.png')
nothing = Image.open(path + '/Template/nothing.png')
white_bar = Image.open(path + '/Template/white_bar.png')

draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)
draw3 = ImageDraw.Draw(image3)

def arrow_green_red_test(change_name):
	if list(change_name)[0] == '+':
		x = arrow_green
		return x
	elif list(change_name)[0] == '-':
		x = arrow_red
		return x
	else:
		x = white_bar
		return x
arrow_ibov = arrow_green_red_test(change_ibov)
arrow_sp = arrow_green_red_test(change_sp)
arrow_dolar = arrow_green_red_test(change_dolar)
arrow_btc = arrow_green_red_test(change_btc)
arrow_eth = arrow_green_red_test(change_eth)
arrow_gold = arrow_green_red_test(change_gold)
arrow_oil = arrow_green_red_test(change_oil)

# Imagem 1

# Preços
draw.text(xy=(325,705), text = price_ibov, fill = (30, 63, 116), font = montserrat_small)
draw.text(xy=(320,1020), text = price_sp, fill = (30, 63, 116), font = montserrat_small)
draw.text(xy=(320,1340), text = price_dolar, fill = (30, 63, 116), font = montserrat_small) 

# Changes
draw.text(xy=(710,660), text = change_ibov, fill = (30, 63, 116), font = montserrat_small)
draw.text(xy=(710,975), text = change_sp, fill = (30, 63, 116), font = montserrat_small)
draw.text(xy=(710,1295), text = change_dolar, fill = (30, 63, 116), font = montserrat_small)

image.paste(arrow_ibov,(950,660), arrow_ibov) 
image.paste(arrow_sp,(950,975), arrow_sp)
image.paste(arrow_dolar,(950,1295), arrow_dolar)

# Imagem 3

# Preços
draw3.text(xy=(275,460), text = price_btc, fill = (30, 63, 116), font = montserrat_small)
draw3.text(xy=(275,685), text = price_eth, fill = (30, 63, 116), font = montserrat_small)
draw3.text(xy=(275,1150), text = price_gold, fill = (30, 63, 116), font = montserrat_small)
draw3.text(xy=(275,1370), text = price_oil, fill = (30, 63, 116), font = montserrat_small)

# Changes
draw3.text(xy=(730,420), text = change_btc, fill = (30, 63, 116), font = montserrat_small)
draw3.text(xy=(730,645), text = change_eth, fill = (30, 63, 116), font = montserrat_small) 
draw3.text(xy=(730,1115), text = change_gold, fill = (30, 63, 116), font = montserrat_small)
draw3.text(xy=(730,1325), text = change_oil, fill = (30, 63, 116), font = montserrat_small)
# Setas
image3.paste(arrow_btc,(945,420), arrow_btc)
image3.paste(arrow_eth,(945,635), arrow_eth)
image3.paste(arrow_gold,(945,1115), arrow_gold)
image3.paste(arrow_oil,(945,1325), arrow_oil)


#################################################################################################
url = 'https://economia.uol.com.br/cotacoes/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

#  Local aonde esta todas as informações de "maiores altas" e "maiores baixas"
uol = ([my_tag.text for my_tag in soup.find_all('section', class_ = "stock-rankings")])
# Devemos agora transformar essa list em string. Essa lista contém todas as informações da seção do 
# ranking de ações (Nome, Preço e Variação).
str_into_list = re.sub("\s", " ", str(uol).strip())

# Esta outra lista, contém o nome de TODOS os ativos do site.
stocks = ([my_tag.text for my_tag in soup.find_all('td', class_ = "title")])

# Na ordem, apartir do nº 12 aparece as ações em alta.
high_stock1 = stocks[12]
high_stock2 = stocks[13]
high_stock3 = stocks[14]

# Na ordem, apartir do nº  aparece as ações em baixa.
low_stock1 = stocks[17]
low_stock2 = stocks[18]
low_stock3 = stocks[19]

# Porém ao pegar essas ações, todas vem com o atributo ".SA" no final, por isso criei uma função para tirar esses ".SA"
def getting_out_SA(number):
	x = stocks[number]
	y = x.replace(".SA","")
	return str(y)

# Agora vamos criar os mesmos nomes das ações, porém limpos (sem o '.SA' no final)
# Ações em alta
clean_high_stock1 = getting_out_SA(12)
clean_high_stock2 = getting_out_SA(13)
clean_high_stock3 = getting_out_SA(14)

#Ações em baixa
clean_low_stock1 = getting_out_SA(17)
clean_low_stock2 = getting_out_SA(18)
clean_low_stock3 = getting_out_SA(19)

# Com isso temos os nomes das 6 ações.
# O próximo passo é conseguir os dados das variações
# Nesse caso os dados vem tão embaralhado, que é difícil explicar o que é feito para limpar e consegui-los
# Vamos criar uma função para automatizar o processo
# Exemplo + / - 1,50% ou + / - 1,5%, ex: +1,50%
# Não sei se já aconteceu de uma ação variar 3 dígitos do índice IBOVESPA (e acho muito difícil acontecer), 
# mas por segurança, farei também um statement if no caso de ex: "+123,45%".

def cleaning_stocks_changes(name_of_stock):
	cleaning_process1 = str_into_list.replace("R$"," ")
	cleaning_process2 = str(cleaning_process1).split(name_of_stock)
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
	
# Com essa função criada, agora podemos criar as variáveis de "change", das ações.
# Change/ Variação das 3 maiores altas
change_high_stock1 = cleaning_stocks_changes(high_stock1)
change_high_stock2 = cleaning_stocks_changes(high_stock2)
change_high_stock3 = cleaning_stocks_changes(high_stock3)

#Change/ Variação das 3 maiores baixas

change_low_stock1 = cleaning_stocks_changes(low_stock1)
change_low_stock2 = cleaning_stocks_changes(low_stock2)
change_low_stock3 = cleaning_stocks_changes(low_stock3)

def stress_test_change_high(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		return change_stockn
	else:
		change_stockn2 = ' ' 
		return change_stockn2

def stress_test_change_low(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		return change_stockn
	else:
		change_stockn2 = ' ' 
		return change_stockn2

def stress_test_ticket_high(ticket_stockn, change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		return ticket_stockn
	else:
		ticket_stockn = ' '
		return ticket_stockn

def stress_test_ticket_low(ticket_stockn, change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		return ticket_stockn
	else:
		ticket_stockn = ' '
		return ticket_stockn

real_change1 = stress_test_change_high(change_high_stock1)
real_change2 = stress_test_change_high(change_high_stock2)
real_change3 = stress_test_change_high(change_high_stock3)
real_change4 = stress_test_change_low(change_low_stock1)
real_change5 = stress_test_change_low(change_low_stock2)
real_change6 = stress_test_change_low(change_low_stock3)

real_ticket1 = stress_test_ticket_high(clean_high_stock1, change_high_stock1)
real_ticket2 = stress_test_ticket_high(clean_high_stock2, change_high_stock2)
real_ticket3 = stress_test_ticket_high(clean_high_stock3, change_high_stock3)
real_ticket4 = stress_test_ticket_low(clean_low_stock1, change_low_stock1)
real_ticket5 = stress_test_ticket_low(clean_low_stock2, change_low_stock2)
real_ticket6 = stress_test_ticket_low(clean_low_stock3, change_low_stock3)

def arrow_green_or_not(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '+':
		x = arrow_green
		return x
	else:
		x = nothing
		return x
def arrow_red_or_not(change_stockn):
	change_stockn2 = list(change_stockn[0])
	if change_stockn2[0] == '-':
		x = arrow_red
		return x
	else:
		x = nothing
		return x

# Teste lógico para possíveis dias atípicos
green_or_not1 = arrow_green_or_not(change_high_stock1)
green_or_not2 = arrow_green_or_not(change_high_stock2)
green_or_not3 = arrow_green_or_not(change_high_stock3)
red_or_not1 = arrow_red_or_not(change_low_stock1) 
red_or_not2 = arrow_red_or_not(change_low_stock2) 
red_or_not3 = arrow_red_or_not(change_low_stock3) 

# Nomes
draw2.text(xy=(215,508), text = real_ticket1, fill = (255, 255, 255), font = montserrat_extrabold)
draw2.text(xy=(215,659), text = real_ticket2, fill = (255, 255, 255), font = montserrat_extrabold)
draw2.text(xy=(215,811), text = real_ticket3, fill = (255, 255, 255), font = montserrat_extrabold)
draw2.text(xy=(215,1207), text = real_ticket4, fill = (255, 255, 255), font = montserrat_extrabold)
draw2.text(xy=(215,1360), text = real_ticket5, fill = (255, 255, 255), font = montserrat_extrabold)
draw2.text(xy=(215,1510), text = real_ticket6, fill = (255, 255, 255), font = montserrat_extrabold)

# Changes
draw2.text(xy=(550,508), text = real_change1, fill = (255, 255, 255), font = montserrat_giant)
draw2.text(xy=(550,659), text = real_change2, fill = (255, 255, 255), font = montserrat_giant)
draw2.text(xy=(550,811), text = real_change3, fill = (255, 255, 255), font = montserrat_giant)
draw2.text(xy=(550,1207), text = real_change4, fill = (255, 255, 255), font = montserrat_giant)
draw2.text(xy=(550,1360), text = real_change5, fill = (255, 255, 255), font = montserrat_giant)
draw2.text(xy=(550,1510), text = real_change6, fill = (255, 255, 255), font = montserrat_giant) 

# High
image2.paste(green_or_not1,(850,508), green_or_not1)  
image2.paste(green_or_not2,(850,659), green_or_not2)
image2.paste(green_or_not3,(850,811), green_or_not3)

# Low
image2.paste(red_or_not1,(850,1207), red_or_not1)
image2.paste(red_or_not2,(850,1360), red_or_not2)
image2.paste(red_or_not3,(850,1510), red_or_not3)

time.sleep(10)
image.show()
image2.show()
image3.show()

image.save(path + '/Story/1.png')
image2.save(path + '/Story/2.png')
image3.save(path + '/Story/3.png')