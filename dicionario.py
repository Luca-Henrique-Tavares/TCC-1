import pandas as pd
from deep_translator import GoogleTranslator
import os 
import sqlalchemy
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

def conection():
    try:
        # Criar uma conexão com o banco de dados MySQL
        engine = sqlalchemy.create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

#Leitura da tabela do mysql
def ler_tabela():
    conection()
    global c
    try:
        df = pd.read_sql_table('dici', con=conection())
        full_sumary = df['full-summary'].iloc[c]
        id_true=df['id_true'].iloc[c]
        print(id_true)
        soup = BeautifulSoup(full_sumary, 'html.parser')
        soup=soup.text
        traducao(soup,id_true)
    except Exception as e:
        print(e)
#Nesse caso específico, há uma questão que havai termos no arquivo .xml como estando em tags (html), por isso foi necessário usar o BeautifulSoup para retirar essas tags, e após isso a função abaixo fará a tradução
#Neste caso ocorre a tradução do full-sumary
def traducao(texto, id):  
    try:
        tradutor_pt = GoogleTranslator(source= "en", target= "pt")
        # Verifica se o texto é muito longo
        if len(texto) > 5000:
            # Divide o texto em pedaços de 5000 caracteres
            pedacos = [texto[i:i+4999] for i in range(0, len(texto), 5000)]
            palavras = []
            for pedaco in pedacos:
                # Traduz cada pedaço e adiciona as palavras à lista
                palavra_trad = tradutor_pt.translate(pedaco)
                palavras.extend(palavra_trad.split()) #O comando extends adciona no final da lista os elementos. è similar ao comando append no java script, e o comando split transforma em uma lista
            # Junta as palavras em uma única string
            texto_traduzido = ' '.join(palavras)
        else:
            # Se o texto não é muito longo, traduz como antes
            texto_traduzido = tradutor_pt.translate(texto)
    except Exception as e:
        print(e)
    df = pd.read_sql_table('dici_teste', con=conection())
    #print(id)
    df.loc[df['id_true'] == id, 'full-summary'] = texto_traduzido
    # Salvar no banco de dados:
    df.to_sql('dici_teste', con=conection(), if_exists='replace', index=False)

#Neste caso ocorre a tradução do meta-desc
def traducao2 ():
    tradutor_pt = GoogleTranslator(source= "en", target= "pt")
    df = pd.read_sql_table('dici_teste', con=conection())
    meta_desc=df['meta-desc'].iloc[c]
    id = df['id_true'].iloc[c]
    try:
        if len(meta_desc) > 5000:
            pedacos = [meta_desc[i:i+4999] for i in range(0, len(meta_desc), 5000)]
            palavras = []
            for pedaco in pedacos:
                palavra_trad = tradutor_pt.translate(pedaco)
                palavras.extend(palavra_trad.split())
            texto_traduzido = ' '.join(palavras)
        else:
            texto_traduzido = tradutor_pt.translate(meta_desc)
    except Exception as e:
        print(e)
    df.loc[df['id_true'] == id, 'meta-desc'] = texto_traduzido #função loc seleciona linhas e colunas que deseja mudar. No caso a linha que tem o id_true igual a id, a coluna meta-desc terá seu valor alterado para texto_traduzido
    # Salvar no banco de dados:
    df.to_sql('dici_teste', con=conection(), if_exists='replace', index=False)
    print(id)

#Neste caso ocorre a tradução do title, related-topic, also-called e group
def traducao3():
    tradutor_pt=GoogleTranslator(source="en", target="pt")
    df=pd.read_sql_table('dici_teste', con=conection())
    title=df['title'].iloc[c]
    related_topic=df['related-topic'].iloc[c]
    also_called=df['also-called'].iloc[c]
    group=df['group'].iloc[c]
    id=df['id_true'].iloc[c]

    try:
        if(also_called==None):
            #print(id,'Também chamdo é vazio')#Caso o também chamado seja vazio, não faz nada
            print('')
        else:
            tambem_chamado=tradutor_pt.translate(also_called)
            df.loc[df['id_true']==id, 'also-called']=tambem_chamado
            df.to_sql('dici_teste',con=conection(),if_exists='replace',index=False)
    except Exception as e:
        print(e)
    try:
        if(related_topic==None):
            #print(id,'Tópicos relacionados também é Vazio') #Caso o tópico relacionado seja vazio, não faz nada
            print('')
        else:
            topico_relacionado=tradutor_pt.translate(related_topic)
            df.loc[df['id_true']==id, 'related-topic']=topico_relacionado
            df.to_sql('dici_teste',con=conection(),if_exists='replace',index=False)
    except Exception as e:
        print(e)

    try:
        titulo=tradutor_pt.translate(title)
        grupo=tradutor_pt.translate(group)
    except Exception as e:
        print(e)

    #Colocando dentro da tabela pandas
    df.loc[df['id_true']==id, 'title']=titulo
    df.loc[df['id_true']==id, 'group']=grupo

    #Salvando no banco de dados
    df.to_sql('dici_teste',con=conection(),if_exists='replace',index=False)
    print(id)

c=0
while c <1023:
    ler_tabela() #obs a linha 0 tem id true = 1
    traducao2()
    traducao3()
    c = c+1
    
         
