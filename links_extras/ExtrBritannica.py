import csv
import time

import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import pandas as pd

URL_BASE = "https://www.britannica.com/science/"

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
        div = soup.find('div', class_="reading-channel")
        paragrafos = div.find('p')  # Extrair o primeiro parágrafo
        texto = ' '.join([p.text for p in paragrafos])
        traducao_texto = traducao(texto)
        return traducao_texto
    except Exception as error:
        print('Erro ao extrair dados')
        print(error)
        
        
def traducao(palavra):
    palavra_traduzida = GoogleTranslator(source='en', target='pt').translate(palavra).lower()
    return palavra_traduzida

def criar_csv():
    with open('dados.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Termo", "Parágrafo", "Data_acesso", "Fonte", "Link"])

# -*- coding: iso-8859-1 -*-

def salvar_dados_csv(titulo, texto, url):
    with open('dados.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([titulo, texto, "Acesso em maio de 2024", "Enciclopédia Britânica", url])
        
def salvar_termo_nf_csv(titulo):
    with open('dados_nf.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([titulo])
        
def extrair_termos():
    df = pd.read_csv('dados.csv', delimiter=';')
    termos = df['Termo'].tolist()
    return termos

def traduzir_termos():
    df = pd.read_csv('dados.csv', delimiter=';')
    
    df['Titulo'] = df['Titulo'].astype(str)
        
    for i, row in df.iterrows():
        termo = row['Termo']
        traducao = GoogleTranslator(source='en', target='pt').translate(termo)
        df.at[i, 'Titulo'] = traducao
    df.to_csv('dados.csv', index=False, sep=';')
        

if __name__ == "__main__":
        criar_csv()
        lista_termos = ['animais-peconhentos' 'acidentes-por-abelhas' 'acidentes-ofidicos' 'anomalias-congenitas' 'arenavirus' 'aguas-vivas-e-caravelas' 'aedes-aegypti' 'brucelose-humana' 'burnout' 'candidiase-sistemica' 'acidentes-por-escorpioes' 'acidentes-por-lagartas' 'coccidioidomicose' 'covid-19' 'criptococose' 'cromoblastomicose' 'arboviroses' 'ame' 'Câncer de Penis' 'bcg' 'doacao-de-leite' 'doacao-de-sangue' 'doenca-de-haff' 'Doenças de Transmissão Hídrica e Alimentar' 'Doenças Diarreicas' 'dtpa' 'dt' 'dtp' 'esporotricose-humana' 'esteatose-hepatica' 'febre-amarela' 'esquistossomose' 'febre-do-mayaro' 'febre-maculosa' 'febre-tifoide' 'febre-do-nilo-ocidental' 'feohifomicose' 'febre-do-oropouche' 'fimose' 'fusariose' 'gripe-influenza' 'enchentes' 'epicovid-19' 'geo-helmintiase' 'epidermolise-bolhosa' 'hantavirose' 'hidatidose-humana' 'ist' 'leishmaniose-visceral' 'hpv' 'insolacao' 'lt' 'leptospirose' 'infarto' 'influenza-aviaria' 'htlv' 'micetomas' 'micoses-endemicas' 'lean-nas-emergencias' 'pentavalente' 'microcefalia' 'peste' 'mpox' 'poliomielite' 'mucormicose' 'pcdt' 'pics' 'oncocercose' 'rotavirus' 'saude-unica' 'pense' 'seguranca-do-paciente' 'sifilis-congenita' 'sindrome-da-rubeola-congenita' 'tetano-acidental' 'sindrome-de-burnout' 'tetano-neonatal' 'shu' 'sus' 'tracoma' 'transplantes' 'samu-192' 'Saúde da pessoa com deficiência' 'triscosporonose' 'variola-dos-macacos' 'trombose' 'vigitel' 'uma-so-saude' 'upa-24h']
        for palavra in lista_termos:                       
            palavra_traduzida = GoogleTranslator(source='pt', target='en').translate(palavra).lower().replace(' ', '-')
            URL_PESQUISA = URL_BASE + palavra_traduzida
            resposta_busca = request_url(URL_PESQUISA)
            if resposta_busca:
                soup_busca = parsing(resposta_busca)
                if soup_busca:
                    texto = extrair_dados(soup_busca)
                    print(texto)
                    salvar_dados_csv(palavra_traduzida, texto, URL_PESQUISA)
            else:
                salvar_termo_nf_csv(palavra_traduzida)
        traduzir_termos()