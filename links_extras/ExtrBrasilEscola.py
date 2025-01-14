import csv
import re

import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

URL_BASE = "https://brasilescola.uol.com.br/biologia/"

def request_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
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
        div = soup.find('div', class_="texto-conteudo")
        paragrafo = div.find_all('p')[1]
        texto = paragrafo.text.replace('\n','').replace('\r','').replace('\t','') # Parse the first part as HTML and get the text
        titulo = soup.find('h1', class_="titulo-interna mb-4").text
        return texto, titulo
    except Exception as error:
        print('Erro ao extrair dados')
        print(error)
        return '', ''
        
def traducao(palavra):
    palavra_traduzida = GoogleTranslator(source='en', target='pt').translate(palavra).lower()
    return palavra_traduzida

def criar_csv():
    with open('dados6.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Termo", "Parágrafo", "Data_acesso", "Fonte", "Link", "Titulo"])

def salvar_dados_csv(titulo, texto, palavra, url):
    with open('dados6.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([palavra, texto, "Acesso em maio de 2024", "Site Brasil Escola", url, titulo])
        
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
        palavra_traduzida = traducao(palavra)
        URL_PESQUISA = URL_BASE + palavra_traduzida + ".htm"
        resposta_busca = request_url(URL_PESQUISA)
        if resposta_busca:
            soup_busca = parsing(resposta_busca)
            if soup_busca:
                texto, titulo = extrair_dados(soup_busca)
                print(texto, titulo, URL_PESQUISA)
                salvar_dados_csv(titulo, texto, palavra, URL_PESQUISA)

