import pandas as pd
from sqlalchemy import create_engine
from thefuzz import fuzz
import numpy as np

#Conexão com o banco de dados
def connection():
    try:
        engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

#Função que lê as tabelas do banco de dados e compara caso haja semelhança entre os termos para que possamos adcionar a chave estrangeira
#OBS: Se a semelhança for maior que 83% o termo será adcionado
#Sempre que possível, as definições serão retiradas do bd do medline plus. Por isso, devemos colocar a chave estrangeira para verificar isso ocorre ou não. Lembre-se que esta tabela poderá funcionar como fonte de informação sobre tratamentos, prevenções, público alvo e conceituação
def ler_tabelas():
    try:
        df_dici = pd.read_sql_table('dici_teste',con = connection())
        df_sus = pd.read_sql_table('sus2',con=connection())
    except Exception as e:
        print(e)
    try: 
        # Inicialize a nova coluna com valores Null. Isso é feito por meio da função np.nan, que seta os valores como sendo null
        df_sus['dici_teste_id'] = np.nan
    except Exception as e:
        print(e)
    f = 0
    cont=0
    while f < len(df_sus):
        medida = 83
        titulo1 = 'Erro'
        titulo2 = 'Erro'
        for i in range(0,len(df_dici)):
                if fuzz.ratio(df_dici['title'].iloc[i],df_sus['titulo'].iloc[f]) > medida:
                    medida = fuzz.ratio(df_dici['title'].iloc[i],df_sus['titulo'].iloc[f])
                    titulo1 = df_dici['title'].iloc[i]
                    titulo2 = df_sus['titulo'].iloc[f]
                    id = df_dici['id_true'].iloc[i]
        if(medida > 83):
            # Se a medida for maior que 83, atribua o id da tabela dici_teste à nova coluna. Reparece que em ambas recebem o valor de sua linha e coluna. Isso funcionará como uma chave estrangeira em nosso código
            df_sus.loc[f, 'dici_teste_id'] = id
        #Adciona a nova coluna ao código
        df_sus.to_sql('sus2',con=connection(),if_exists='replace',index=False)
        if(titulo1 != 'Erro' and titulo2 != 'Erro'):
            print(titulo1,id)      
            cont+=1
        f+=1
    print('Total de termos encontrados:',cont)

if __name__ == '__main__':
    connection()
    ler_tabelas()
    