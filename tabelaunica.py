import pandas as pd 
from sqlalchemy import create_engine
import os 
import datetime

def connection():
    try:
        engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

def dici_e_sus():
    ts = 0
    cont=0
    data = datetime.datetime.now()
    # extrai o dia, mês e ano
    dia = data.day
    mes = data.month
    ano = data.year
    # cria a string de data
    data_str = f'Acesso em: {dia}/{mes}/{ano}'
    try:
        df_sus=pd.read_sql_table('sus2', con=connection())
    except Exception as e:
        print(e)
    try:
        df_dici=pd.read_sql_table('dici_teste', con=connection())
    except Exception as e:
        print(e)
    try:
        df_sus_yt=pd.read_sql_table('youtube_sus', con=connection())
    except Exception as e:
        print(e)
    try:
        df_dici_yt=pd.read_sql_table('youtube_dici', con=connection())
    except Exception as e:
        print(e)
    try:
        df_anatomia_yt=pd.read_sql_table('youtube_anatomia', con=connection())
    except Exception as e:
        print(e)
    try:
        df_links=pd.read_sql_table('links', con=connection())
    except Exception as e:
        print(e)
    dicionario = {}
    k = 0
    #termos em que há a correspondência entre os dataframes
    try:
        for i in range(len(df_sus)):
            for j in range(len(df_dici)):
                if df_sus['dici_teste_id'][i] == df_dici['id_true'][j]:
                    for c in range(len(df_sus_yt)):
                        if df_sus['id'][i] == df_sus_yt['dici_teste_id'][c]:
                            if ts == 0:
                                url1 = df_sus_yt['url'][c]
                                titulo_vd_1 = df_sus_yt['titulo'][c]
                            elif ts == 1:
                                url2 = df_sus_yt['url'][c]
                                titulo_vd_2 = df_sus_yt['titulo'][c]
                            elif ts == 2:
                                url3 = df_sus_yt['url'][c]
                                titulo_vd_3 = df_sus_yt['titulo'][c]
                            ts+=1
                    ts = 0
                    for l in range(len(df_links)):
                        if df_sus['titulo'][i].lower() == df_links['Titulo'][l].lower():
                            if cont ==0:
                                link1=df_links['Link'][l]
                                paragrafo1=df_links['Parágrafo'][l]
                                fonte=df_links['Fonte'][l]
                            elif cont ==1:
                                link2=df_links['Link'][l]
                                paragrafo2=df_links['Parágrafo'][l]
                                fonte2=df_links['Fonte'][l]
                            elif cont ==2:
                                link3=df_links['Link'][l]
                                paragrafo3=df_links['Parágrafo'][l]
                                fonte3=df_links['Fonte'][l]
                            cont+=1
                    if(cont==0):
                        link1 = None
                        link2 = None
                        link3 = None
                        fonte = None
                        fonte2 = None
                        fonte3 = None
                        paragrafo1 = None
                        paragrafo2 = None
                        paragrafo3 = None
                    cont = 0

                    dicionario = {
                        'titulo': df_dici['title'][j],
                        'texto_definicao1': df_sus['texto'][i],
                        'texto_tratamento': df_sus['texto_tratamento'][i],
                        'texto_prevencao': df_sus['texto_prevencao'][i],
                        'texto_publicoalvo': df_sus['texto_publicoalvo'][i],
                        'fonte_definicao1': df_sus['fonte'][i],
                        'fonte_publicoalvo': df_sus['fonte'][i],   
                        'fonte_prevencao': df_sus['fonte'][i],
                        'fonte_tratamento': df_sus['fonte'][i], 
                        'texto_definicao2': df_dici['full-summary'][j],
                        'tambem_chamado':df_dici['also-called'][j],
                        'fonte_definicao2': df_dici['Fonte'][j],
                        'texto_definicao3': None,
                        'fonte_definicao3': None,
                        'video1': url1,
                        'titulo_video1': titulo_vd_1,
                        'video2': url2,
                        'titulo_video2': titulo_vd_2,
                        'video3': url3,
                        'titulo_video3': titulo_vd_3,
                        'fonte_video': df_sus_yt['fonte'][c],
                        'link1': link1,
                        'link2': link2,
                        'link3': link3,
                        'paragrafo1': paragrafo1,
                        'paragrafo2': paragrafo2,
                        'paragrafo3': paragrafo3,
                        'fonte_link1': fonte,
                        'fonte_link2': fonte2,
                        'fonte_link3': fonte3,
                        'acesso em': data_str
                    }
                    k = 1
            #termos em que não há correspondência entre os dataframes
            if(k == 0):
                for c in range(len(df_sus_yt)):
                        if df_sus['id'][i] == df_sus_yt['dici_teste_id'][c]:
                            if ts == 0:
                                url1 = df_sus_yt['url'][c]
                                titulo_vd_1 = df_sus_yt['titulo'][c]
                            elif ts == 1:
                                url2 = df_sus_yt['url'][c]
                                titulo_vd_2 = df_sus_yt['titulo'][c]
                            elif ts == 2:
                                url3 = df_sus_yt['url'][c]
                                titulo_vd_3 = df_sus_yt['titulo'][c]
                            ts+=1
                ts = 0
                for l in range(len(df_links)):
                    if df_sus['titulo'][i].lower() == df_links['Titulo'][l].lower():
                        if cont ==0:
                            link1=df_links['Link'][l]
                            paragrafo1=df_links['Parágrafo'][l]
                            fonte=df_links['Fonte'][l]
                        elif cont ==1:
                            link2=df_links['Link'][l]
                            paragrafo2=df_links['Parágrafo'][l]
                            fonte2=df_links['Fonte'][l]
                        elif cont ==2:
                            link3=df_links['Link'][l]
                            paragrafo3=df_links['Parágrafo'][l]
                            fonte3=df_links['Fonte'][l]
                        cont+=1
                if(cont ==0):
                    link1 = None
                    link2 = None
                    link3 = None
                    fonte = None
                    fonte2 = None
                    fonte3 = None
                    paragrafo1 = None
                    paragrafo2 = None
                    paragrafo3 = None
                cont = 0
                dicionario = {
                   'titulo': df_sus['titulo'][i],
                    'texto_definicao1': df_sus['texto'][i],
                    'texto_tratamento': df_sus['texto_tratamento'][i],
                    'texto_prevencao': df_sus['texto_prevencao'][i],
                    'texto_publicoalvo': df_sus['texto_publicoalvo'][i],
                    'fonte_definicao1': df_sus['fonte'][i],
                    'fonte_publicoalvo': df_sus['fonte'][i],   
                    'fonte_prevencao': df_sus['fonte'][i],
                    'fonte_tratamento': df_sus['fonte'][i], 
                    'texto_definicao2': None,
                    'tambem_chamado': None,
                    'fonte_definicao2': None,
                    'texto_definicao3': None,
                    'fonte_definicao3': None,
                    'video1': url1,
                    'titulo_video1': titulo_vd_1,
                    'video2': url2,
                    'titulo_video2': titulo_vd_2,
                    'video3': url3,
                    'titulo_video3': titulo_vd_3,
                    'fonte_video': df_sus_yt['fonte'][c],
                    'link1': link1,
                    'link2': link2,
                    'link3': link3,
                    'paragrafo1': paragrafo1,
                    'paragrafo2': paragrafo2,
                    'paragrafo3': paragrafo3,
                    'fonte_link1': fonte,
                    'fonte_link2': fonte2,
                    'fonte_link3': fonte3,
                    'acesso em': data_str
                }
                insere(dicionario)
                dicionario = {}
            if(k == 1):
                insere(dicionario)
                dicionario = {}
                k = 0
    except Exception as e:
        print(e)
    #verificação dos termos da base de dados medline
    try:
        for i in range(len(df_dici)):
            for j in range(len(df_sus)):
                if df_dici['id_true'][i] == df_sus['dici_teste_id'][j]:
                    k = 1
            if(k == 0):
                for c in range(len(df_dici_yt)):
                        if df_dici['id_true'][i] == df_dici_yt['dici_teste_id'][c]:
                            if ts == 0:
                                url1 = df_dici_yt['url'][c]
                                titulo_vd_1 = df_dici_yt['titulo'][c]
                            elif ts == 1:
                                url2 = df_dici_yt['url'][c]
                                titulo_vd_2 = df_dici_yt['titulo'][c]
                            elif ts == 2:
                                url3 = df_dici_yt['url'][c]
                                titulo_vd_3 = df_dici_yt['titulo'][c]
                            ts+=1
                ts = 0
                for l in range(len(df_links)):
                    if df_dici['title'][i].lower() == df_links['Titulo'][l].lower():
                        if cont == 0:
                            link1=df_links['Link'][l]
                            paragrafo1=df_links['Parágrafo'][l]
                            fonte=df_links['Fonte'][l]
                        elif cont ==1:
                            link2=df_links['Link'][l]
                            paragrafo2=df_links['Parágrafo'][l]
                            fonte2=df_links['Fonte'][l]
                        elif cont ==2:
                            link3=df_links['Link'][l]
                            paragrafo3=df_links['Parágrafo'][l] 
                            fonte3=df_links['Fonte'][l]
                        cont+=1
                if(cont ==0):
                    link1 = None
                    link2 = None
                    link3 = None
                    fonte = None
                    fonte2 = None
                    fonte3 = None
                    paragrafo1 = None
                    paragrafo2 = None
                    paragrafo3 = None
                cont = 0
                dicionario = {
                    'titulo': df_dici['title'][i],
                    'texto_definicao1': None,
                    'texto_tratamento': None,
                    'texto_prevencao': None,
                    'texto_publicoalvo': None,
                    'fonte_definicao1': None,
                    'fonte_publicoalvo': None,   
                    'fonte_prevencao': None,
                    'fonte_tratamento': None, 
                    'texto_definicao2': df_dici['full-summary'][i],
                    'tambem_chamado':df_dici['also-called'][i],
                    'fonte_definicao2': df_dici['Fonte'][i],
                    'texto_definicao3': None,
                    'fonte_definicao3': None,
                    'video1': url1,
                    'titulo_video1': titulo_vd_1,
                    'video2': url2,
                    'titulo_video2': titulo_vd_2,
                    'video3': url3,
                    'titulo_video3': titulo_vd_3,
                    'fonte_video': df_dici_yt['fonte'][c],
                    'link1': link1,
                    'link2': link2,
                    'link3': link3,
                    'paragrafo1': paragrafo1,
                    'paragrafo2': paragrafo2,
                    'paragrafo3': paragrafo3,
                    'fonte_link1': fonte,
                    'fonte_link2': fonte2,
                    'fonte_link3': fonte3,
                    'acesso em': data_str
                }
                insere(dicionario)
                dicionario = {}
            if(k == 1):
                k = 0
                print(f"O termo: {df_dici['title'][i]} já está na tabela unica")
    except Exception as e:
        print(e)
    #Aedcionamos aqui os termos da tabela de termos de anatomia
    try:
        df_anatomia = pd.read_sql_table('anatomia', con=connection())
    except Exception as e:
        print(e)
    try:
        for i in range(len(df_anatomia)):
            for c in range(len(df_anatomia_yt)):
                    if df_anatomia['id_true'][i] == df_anatomia_yt['anatomia_id'][c]:
                        if ts == 0:
                            url1 = df_anatomia_yt['url'][c]
                            titulo_vd_1 = df_anatomia_yt['titulo'][c]
                        elif ts == 1:
                            url2 = df_anatomia_yt['url'][c]
                            titulo_vd_2 = df_anatomia_yt['titulo'][c]
                        elif ts == 2:
                            url3 = df_anatomia_yt['url'][c]
                            titulo_vd_3 = df_anatomia_yt['titulo'][c]
                        ts+=1
            ts = 0
            for l in range(len(df_links)):
                if df_anatomia['titulo'][i].lower() == df_links['Titulo'][l].lower():
                    if cont ==0:
                        link1=df_links['Link'][l]
                        paragrafo1=df_links['Parágrafo'][l]
                        fonte=df_links['Fonte'][l]
                    elif cont ==1:
                        link2=df_links['Link'][l]
                        paragrafo2=df_links['Parágrafo'][l]
                        fonte2=df_links['Fonte'][l]
                    elif cont ==2:
                        link3=df_links['Link'][l]
                        paragrafo3=df_links['Parágrafo'][l]
                        fonte3=df_links['Fonte'][l]
                    cont+=1
            if(cont ==0):
                link1 = None
                link2 = None
                link3 = None
                fonte = None
                fonte2 = None
                fonte3 = None
                paragrafo1 = None
                paragrafo2 = None
                paragrafo3 = None
            cont = 0
            dicionario = {
                'titulo': df_anatomia['titulo'][i],
                'texto_definicao1':None,
                'texto_tratamento': None,
                'texto_prevencao': None,
                'texto_publicoalvo': None,
                'fonte_definicao1': None,
                'fonte_publicoalvo': None,   
                'fonte_prevencao': None,
                'fonte_tratamento': None, 
                'texto_definicao2': None,
                'tambem_chamado':None,
                'fonte_definicao2': None,
                'texto_definicao3': df_anatomia['texto'][i],
                'fonte_definicao3': df_anatomia['fonte'][i],
                'video1': url1,
                'titulo_video1': titulo_vd_1,
                'video2': url2,
                'titulo_video2': titulo_vd_2,
                'video3': url3,
                'titulo_video3': titulo_vd_3,
                'fonte_video': df_anatomia_yt['fonte'][c],
                'link1': link1,
                'link2': link2,
                'link3': link3,
                'paragrafo1': paragrafo1,
                'paragrafo2': paragrafo2,
                'paragrafo3': paragrafo3,
                'fonte_link1': fonte,
                'fonte_link2': fonte2,
                'fonte_link3': fonte3,
                'acesso em': data_str
            }
            insere(dicionario)
            dicionario = {}
    except Exception as e:
        print(e)

def insere(dicionario):
    try:
        if os.path.exists('tabela_unica.csv'):
            df = pd.read_csv('tabela_unica.csv')
        else:
            df = pd.DataFrame(columns=['titulo', 'texto_definicao1', 'texto_tratamento', 'texto_prevencao', 'texto_publicoalvo', 'fonte_definicao1', 'fonte_publicoalvo', 'fonte_prevencao', 'fonte_tratamento', 'texto_definicao2', 'fonte_definicao2', 'tambem_chamado', 'texto_definicao3', 'fonte_definicao3', 'video1', 'titulo_video1', 'video2', 'titulo_video2', 'video3', 'titulo_video3', 'fonte_video', 'link1', 'link2', 'link3','paragrafo1','paragrafo2','paragrafo3','fonte_link1', 'fonte_link2', 'fonte_link3', 'acesso em'])
    except Exception as e:
        print(e)
    df.loc[len(df)] = dicionario
    df.to_csv('tabela_unica.csv', index=False)
    try:
        df.to_sql('tabela_unica',con=connection(),if_exists='replace',index=False)
    except Exception as e:
        print(e)
                
if __name__ == '__main__':
    connection()
    dici_e_sus()