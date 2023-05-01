import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = "https://www.kabum.com.br/escritorio/home-office/cadeira-de-escritorio"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
result = soup.find(id="listingCount")

if result is not None:
    b_tag = result.find('b')
    if b_tag is not None:
        quantidade_itens = b_tag.get_text().strip()

ultima_pagina = math.ceil(int(quantidade_itens)/20)
print(ultima_pagina)

dicionario_produtos = {'marca': [], 'preco': [], 'link': []}

paginas_teste = int(40)

for i in range(1, paginas_teste+1):
    url_pagina = f"https://www.kabum.com.br/escritorio/home-office/cadeira-de-escritorio?page_number={i}&page_size=20&facet_filters=&sort=most_searched"

    site = requests.get(url_pagina, headers=headers)

    soup = BeautifulSoup(site.content, 'html.parser')

    produtos = soup.find_all(class_=re.compile("productCard"))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile(
            'nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile(
            'priceCard')).get_text().strip()
        link = produto.find('a')['href']

    dicionario_produtos['marca'].append(marca)
    dicionario_produtos['preco'].append(preco)
    dicionario_produtos['link'].append(link)

    # print(marca, preco)

df = pd.DataFrame(dicionario_produtos)
df.to_excel('C:/Users/Master/Desktop/arquivoScrapping.xlsx')
