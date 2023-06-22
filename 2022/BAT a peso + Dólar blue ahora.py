from bs4 import BeautifulSoup as BS
from requests import get
from pyinputplus import inputFloat


amount = inputFloat('Introduce la cantidad de BATs: ')
bat_html = BS(get('https://www.coingecko.com/en/coins/basic-attention-token').text, 'lxml')
bat_price = float(bat_html.find_all(class_='no-wrap')[0].text[1:])
dolar_blue_html = BS(get('https://dolarhoy.com/').text, 'lxml')
dolar_blue_price = float(dolar_blue_html.find_all(class_='val')[1].text[1:])
bat_to_ars = round(bat_price * dolar_blue_price * amount, 1)
input(f"""
1 BAT: US$ {bat_price}
1 Dolar blue: AR$ {dolar_blue_price}\n
{amount} BAT/s equivale/n a {bat_to_ars} pesos argentinos.
""")
