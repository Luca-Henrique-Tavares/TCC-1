from googleapiclient.discovery import build
import pandas as pd
from sqlalchemy import create_engine
import os
import datetime as dat

#Há a conecção com a API do Youtube
def connection_yt():
    try: 
        key = 'AIzaSyCwLkFk1pC0pQqtxW3MTainR6FeqBQQ9DU'
        youtube=build('youtube','v3',developerKey=key)
        return youtube # no caso quando for ativada a função passrá a variável youtube
    except Exception as e:
        print(e)

#Há a conecção com o banco de dados
def connection():
    try:
        engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

#Função que lê o banco de dados, e após isso através da função pesquisa_yt é feita a pesquisa no youtube. 
#Obs: a pesquisa é feita com uma conexão com o banco de dados, pois como há uma limitação na api do youtube é necessário estabelecer de onde parou a última pesquisa
#Obs: nos testes até agora, sempre foram retornados no mínimo 3 vídeos pedidos no último termo pesquisado. Talvez seja necessário adotar uma funç~~ao que verifica que os últimos três elementos possuem o mesmo id. Caso contrário, o valor que deverá ser utilizado terá iloc[-2]
def read_anatomia():
    try:
        df_anat = pd.read_sql_table('anatomia',con = connection())
    except Exception as e:
        print(e)
    try:
        df_yt = pd.read_sql_table('youtube_anatomia',con = connection())
    except Exception as e:
        print(e)
    try: 
        df_yt
        i = df_yt['anatomia_id'].iloc[-1] # pega o último id do dataframe
        titulo = df_yt['titulo'].iloc[-1] # pega o último título do dataframe
    except NameError: #Caso não exista o dataframe, ele irá começar a pesquisa do zero, e retornará que não foi achado o dataframe
        i = 0
    while i < len(df_anat): # OBS: Caso seja menor que o tamanho do dataframe, ele irá parar de pesquisar. Obs, este i é o último id do dataframe do youtube, portanto isso inibe repetições o que é totalemente necessário para não haver repetições em uma api limitada ao uso
        id = df_anat['id_true'].iloc[i]
        titulo = df_anat['titulo'].iloc[i]
        pesquisa_yt(titulo,id)
        i+=1

#Função que faz a pesquisa no youtube, e após isso chama a função pandas
def pesquisa_yt(titulo,id):
    try:
        youtube=connection_yt()
        request = youtube.search().list(
            part='snippet', #mostra como será a separação dos termos encontrados
            q=titulo, #termo a ser pesquisado
            type='video', #tipo de pesquisa(no caso vídeo)
            maxResults=3, #quantidade máxima de resultados retornados
            relevanceLanguage='pt', #linguagem dos resultados
            regionCode='BR', #região da postagem dos vídeos
            order='relevance', #como ordernar pela pesquisa
            safeSearch='moderate', #nível de segurança da pesquisa, no caso ordenamos para moderado
            videoEmbeddable='true', #Obs: Apenas vídeos que podem ser incorporados em sites serão exibidos, ou seja, vídeos públicos, caso seja possível vê-lo apenas no site do youtube não aparecerá
            videoDuration='medium' #duração entre 4 e 20 minutos de vídeo
        )
        response = request.execute()
        for item in response['items']:
            titulo = item['snippet']['title']
            canal = item['snippet']['channelTitle']
            video_id = item['id']['videoId']
            url = f'https://www.youtube.com/watch?v={video_id}'
            pandas(url,titulo,canal,id)

    except Exception as e:
        print(e)

#Função que cria um dataframe e insere os dados no arquivo csv
def pandas(url,titulo,canal,id):
    try: 
        if os.path.exists('youtube_anat.csv'):
            df = pd.read_csv('youtube_anat.csv')
        else:
            df = pd.DataFrame(columns=['titulo', 'url','nome_do_canal','data', 'fonte','anatomia_id'])
    except Exception as e:
        print(e)

    data = dat.datetime.now()
    dia = data.day
    mes = data.month
    ano = data.year

    data_str = f'Acesso em: {dia}/{mes}/{ano}'# F string na qual a data é formada a partir de outras strings
    fonte = "Youtube"

    new_data = {
    'titulo': titulo,
    'nome do canal': canal,
    'url': url,
    'data': data_str,
    'fonte': fonte,
    'anatomia_id': id
    }

    df.loc[len(df)] = new_data # len df se refere a próxima linha vazia no dataframe, dessa forma localiza a próxima linha e o insere no dataframe
    df.to_csv('youtube_anat.csv', index=False)#cria o arquivo csv, passando o dataframe para csv e criando o arquivo
    inserir(df)

#Função que insere os dados no banco de dados
def inserir(df):
    try:
        df.to_sql('youtube_anatomia',con=connection(),if_exists='replace',index=False)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    connection()
    read_anatomia()