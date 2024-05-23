import pandas as pd
from sqlalchemy import create_engine
import datetime

# Ler o arquivo CSV em um DataFrame do pandas
df = pd.read_csv('base.csv')
df2=pd.read_xml("dici.xml")
df3 = pd.read_csv('dados2.csv', delimiter=',')
print(df3.head())
print(df3.columns)
#df3=pd.read_excel("cid.xlsx")

#DF2 
# pega a data atual
data = datetime.datetime.now()

# extrai o dia, mês e ano
dia = data.day
mes = data.month
ano = data.year

# cria a string de data
data_str = f'Acesso em: {dia}/{mes}/{ano}'

#Criando Fonte:
Fonte = 'MedlinePlus'

# adiciona a coluna de data ao DataFrame
df2['Data'] = data_str
df2['Fonte'] = Fonte

# Cada tabela criada recebe o valor de um dataframe do pandas
tabela_df = pd.DataFrame(df)
tabela_df2 = pd.DataFrame(df2)
#tabela_df3 = pd.DataFrame(df3)

#print(tabela_df2.columns)
#print(tabela_df2["Data"])

#print(tabela_df3["Title"])

#print(tabela_df2.columns)
#print(tabela_df2["language"])

# Criar uma conexão com o banco de dados MySQL
try:
    engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
except Exception as e:
    print(e)

# Inserir o DataFrame no banco de dados
try:
    #df.to_sql('byjus', con=engine, if_exists='append', index=False)
    #df2.to_sql('dici', con=engine, if_exists='replace', index=False)
    df3.to_sql('links', con=engine, if_exists='replace', index=False)
except Exception as e:
    print(e)

#OBS:
#CÓDIGOS NECESSÁRIOS PARA SE MODIFICAR O MYSQL E RETIRAR DUPLICATAS EM ESPANHOL
#SET SQL_SAFE_MODE = 0;
#DELETE FROM `dici` WHERE `language` = 'Spanish';
#SELECT * from dici;