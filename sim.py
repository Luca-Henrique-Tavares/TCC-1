import pandas as pd
from simpledbf import Dbf5
from sqlalchemy import create_engine

# Ler o arquivo DBF
dbf = Dbf5('DO23OPEN.dbf')

# Converter para DataFrame
df = dbf.to_dataframe()

# Conectar ao banco de dados SQL
engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')

# Escrever o DataFrame em uma tabela SQL
df.to_sql('sim', con=engine, if_exists='replace', index=False)