import csv
import re

import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

URL_BASE = "https://www.biologyonline.com/dictionary/"

def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        print("Erro ao fazer a req")
        print(e)
        
def parsing(resposta_html: str) -> BeautifulSoup:
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as error:
        print('Erro ao fazer o parsing HTML')
        print(error)
        
def extrair_dados(soup: BeautifulSoup):
    try:
        div_title = soup.find('div', class_="header")
        div = soup.find('div', class_="article-content")
        texto_html = str(div)  # Get all HTML inside the div
        match = re.search(r'<p>(.*?)</p>', texto_html, re.DOTALL | re.IGNORECASE)
        if match:
            texto = BeautifulSoup(match.group(1), 'html.parser').get_text()
        else:
            texto = ''
        titulo = div_title.find('h1').text
        traducao_texto = traducao(texto)
        traducao_titulo = traducao(titulo)
        return traducao_texto, traducao_titulo
    except Exception as error:
        print('Erro ao extrair dados')
        print(error)
        return '', ''
def extrair_dados(soup: BeautifulSoup):
    try:
        div = soup.find('div', class_="entry-content")
        print(div)
        paragrafo = div.find_all('p')
        print(paragrafo)
        texto = paragrafo.text.replace('\n','').replace('\r','').replace('\t','') # Parse the first part as HTML and get the text
        print(texto)
        return texto
    except Exception as error:
        print('Erro ao extrair dados')
        print(error)
        return '', ''
        
def traducao(palavra):
    palavra_traduzida = GoogleTranslator(source='en', target='pt').translate(palavra).lower()
    return palavra_traduzida

def criar_csv():
    with open('dados2.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Termo", "Parágrafo", "Data_acesso", "Fonte", "Link", "Titulo"])

def salvar_dados_csv(titulo, texto, palavra, url):
    with open('dados2.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([palavra, texto, "Acesso em maio de 2024", "Site BiologyOnline", url, titulo])
        
def ler_termos_do_csv():
    termos = []
    with open('palavras.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            termos.append(row[0])
    return termos


if __name__ == "__main__":
    criar_csv()
    titulos = ler_termos_do_csv()
    for palavra in titulos:
        palavra = "cancer"
        URL_PESQUISA = URL_BASE + palavra
        print(URL_PESQUISA)
        resposta_busca = request_url(URL_PESQUISA)
        print(resposta_busca)
        if resposta_busca:
            print("ok1")
            soup_busca = parsing(resposta_busca)
            if soup_busca:
                print("ok2")
                texto = extrair_dados(soup_busca)
                titulo = palavra
                print(texto, titulo, palavra, URL_PESQUISA)
                salvar_dados_csv(titulo, texto, palavra, URL_PESQUISA)

