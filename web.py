import requests
from bs4 import BeautifulSoup
import datetime as dat

data=dat.datetime.now()
dia=data.day
mes=data.month
ano=data.year
data=f'Acesso em: {dia}/{mes}/{ano}'
print(data)

link = "https://byjus.com/biology/"
requisicao = requests.get(link)
# print(requisicao.status_code,requisicao.text)
site = BeautifulSoup(requisicao.text, 'html.parser')
# print(site.prettify())
#print(site.title)