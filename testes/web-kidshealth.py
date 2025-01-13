from bs4 import BeautifulSoup
import requests
from requests import Session
from deep_translator import GoogleTranslator
import pandas as pd
import os 
import datetime as dat

def req(url):
    try:
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            print('Erro ao fazer requisição')
    except Exception as e: 
        print("Falha ao fazer a requisição")
        print(e)

def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as e:
        print("Falha ao fazer o parsing")
        print(e)

def traducao():
    try:
        palavra = input("Digite a palavra que deseja pesquisar: ")
        tradutor_pt = GoogleTranslator(source= "pt", target= "en")
        palavra_trad = tradutor_pt.translate(palavra)
        return palavra_trad
    except Exception as e:
        print("Erro ao traduzir")
        print(e)

def encontrar_termo(soup):
    try:
        container2 = soup.find_all('article')
        for article in container2:
            #print(article.text)
            passar=article.text
            traduz_respostas(passar)
    except Exception as e:
        print("Erro ao encontrar valores")
        print(e)


def traduz_respostas(soup):
    traduz_texto = GoogleTranslator(source="en", target="pt")
    try:
        # divide o texto em partes de 5000 caracteres
        partes = [soup[i:i+4999] for i in range(0, len(soup), 5000)]
        traducoes = []
        for parte in partes:
            traducao = traduz_texto.translate(parte)
            traducoes.append(traducao)
        # junta todas as partes traduzidas
        traducao_final = ' '.join(traducoes)
        #print(traducao_final)
        basededados(traducao_final)
    except Exception as e:
        print(e)
    
def basededados(soup):
    id = 1
    texto = soup
    termo=input('Digite o termo da URL: ')
    titulo=input('Digite o título que ficará na base de dados: ')
    URL=f'https://byjus.com/biology/{termo}'
    data=dat.datetime.now()
    dia=data.day
    mes=data.month
    ano=data.year
    data=f'Acesso em: {dia}/{mes}/{ano}' # F string é uma string que possui a opção de escrever variáveis entre chaves e textos fora delas
    fonte='Byjus Biologia'

    # carrega o DataFrame existente se o arquivo CSV existir
    if os.path.exists('base3.csv'):
        df = pd.read_csv('base3.csv')
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(columns=['ID', 'titulo', 'texto', 'url', 'data', 'fonte'])
    else:
        with open ('base3.csv', 'w') as f:
            df = pd.DataFrame(columns=['ID', 'titulo', 'texto', 'url', 'data', 'fonte'])
            df.to_csv('base3.csv', index=False)#cria o arquivo csv, passando o dataframe para csv e criando o arquivo

    # verifica se a URL já existe no DataFrame
    if not df[df['url'] == URL].empty:
        print('URL já existe no DataFrame')
        return 
            
    # adiciona a nova linha ao DataFrame
    id = len(df) + 1 #Pega o tamanho do dataframe em linhas em add 1 ao id
    df.loc[len(df)] = [id, titulo, texto, URL, data, fonte]

    # salva o DataFrame no arquivo CSV
    df.to_csv('base2.csv', index=False)

    print(df)

if __name__ == "__main__":
    termo = traducao()
    URL = f'https://byjus.com/biology/{termo}'
    resposta_busca = req(URL)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            #print(soup_busca)
            encontrar_termo(soup_busca)



