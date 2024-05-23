from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import pandas as pd

tabela = pd.read_csv('tabela_unica.csv', delimiter=',', encoding='utf-8')

termo = input("digite o termo que deseja pesquisar: ")

limite = 83


linhas_correspondentes = []

for index, row in tabela.iterrows():
    correspondencia = fuzz.ratio(termo.lower(), row['titulo'].lower())
    if correspondencia > limite:
        linhas_correspondentes.append(row)

resultado = pd.DataFrame(linhas_correspondentes)

if resultado.empty:
    print("Nenhum resultado encontrado. Realizando uma nova busca...")
    linhas_correspondentes.clear()
    for index, row in tabela.iterrows():
        palavras_titulo = row['titulo'].replace('-',' ').lower().split()
        for palavra in palavras_titulo:
            correspondencia = fuzz.ratio(termo.lower(), palavra)
            if correspondencia > limite:
                linhas_correspondentes.append(row)
                break
    
    resultado = pd.DataFrame(linhas_correspondentes)

if resultado.empty:
    print("Nenhum resultado encontrado após a nova busca.")

topicos = {
    'TEXTO 1': ['titulo','texto_definicao1', 'fonte_definicao1','texto_tratamento', 'fonte_tratamento','texto_prevencao', 'fonte_prevencao','texto_publicoalvo',  'fonte_publicoalvo',  'acesso em'],
    'TEXTO 2': ['texto_definicao2', 'fonte_definicao2', 'tambem_chamado'],
    'TEXTO 3': ['texto_definicao3', 'fonte_definicao3'],
    'VIDEOS': [ 'fonte_video', 'titulo_video1', 'video1', 'titulo_video2', 'video2', 'titulo_video3', 'video3',  'acesso em'],
    'LINKS EXTRAS': ['fonte_link1','paragrafo1','link1', 'fonte_link2','paragrafo2','link2', 'fonte_link3','paragrafo3','link3']
}

for index, row in resultado.iterrows():
    for topico, colunas in topicos.items():
        if not row[colunas].isnull().all():
            print(f"\n====================={topico}:==================\n")
            for col in colunas:
                if pd.notnull(row[col]):
                    print(f"  {row[col]}")
                    if col == 'link1' or col == 'link2' or col == 'link3' or col == 'fonte_video':
                        print()
            print("\n--------------------------------------------------\n")

