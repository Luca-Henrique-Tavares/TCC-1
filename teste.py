from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import datetime as dat
import os
from sqlalchemy import create_engine

def connection():
    try:
        engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

def req(url):
    try:
        #print(url)
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

def econtrartermo(soup,num,url,titulo):
    texto_prevencao = ""
    texto_tratamento = ""   
    texto_publicoalvo = ""
    next_prevencao = False
    next_tratamento = False
    next_publicoalvo = False
    if(num==5): 
        try:
            container = soup.find_all('div', class_='row-content')
            for div in container:
                first_line = div.text #Pega o texto da div 
                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                if(next_prevencao == True):
                    print("Entrooooou")
                    texto_prevencao = f"Prevenção {first_line}"
                    next_prevencao = False
                if(next_tratamento == True):
                    texto_tratamento = f"Tratamento {first_line}"
                    next_tratamento = False
                if(next_publicoalvo == True):
                    texto_publicoalvo = f"Público Alvo {first_line}"
                    next_publicoalvo = False

                #No loop for abaixo são testados se os termos correspondem a alguma página que possua os temas: Tratamento, Prevenção ou Público Alvo. Caso em algum deles esteja em formato de lista, foram feitos códigos que pegam tais trechos
                for i in range(0,1):
                    try:
                        if(i == 0):
                            if len(words) > 1 and (words[0] == 'Tratamento'):
                                texto_tratamento = first_line
                                i += 1
                            elif len(words) > 2 and (words[0] == 'Diagnóstico' and words[1] == 'e' and words[2] == 'tratamento'):
                                texto_tratamento = first_line
                                i+=1 
                            elif len(words) == 1 and (words[0] == 'Tratamento'):
                                next_tratamento = True
                                i+=1
                            else:
                                i+=1
                        if(i==1):
                            if len(words) > 1 and (words[0] == 'Prevenção') : 
                                    print(0)
                                    texto_prevencao = first_line
                                    i+=1
                            elif len(words) == 1 and (words[0] == 'Prevenção'):
                                print(1,"Aquiii")
                                next_prevencao = True
                                i+=1
                            elif len(words) > 2 and (words[0] == 'Sintomas' and words[1] == 'e' and words[2] == 'Prevenção'):
                                print(3)
                                texto_prevencao = first_line
                                i+=1 
                            elif len(words) > 2 and (words[0] == 'Prevenção' and words[1] == 'e' and words[2] == 'Controle'):
                                print(4)
                                texto_prevencao = first_line
                                i+=1 
                            else:
                                i+=1
                        if(i==2):
                            if len(words) > 1 and (words[0] == 'Público') and (words[1] == "Alvo") : # caso o tamanho da lsita seja menor que 1 vamos tentar tratar a excessão
                                texto_publicoalvo = first_line
                            elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                next_publicoalvo = True
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        if(texto_tratamento == ""):
                            container = soup.find_all('div', class_='column col-md-6')
                            for div in container:
                                first_line = div.text #Pega o texto da div 
                                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                                if(next_tratamento == True):
                                    texto_tratamento = f"Tratamento {first_line}"
                                    next_tratamento = False
                                for i in range(0,1):
                                    if len(words) > 1 and (words[0] == 'Tratamento'):
                                        texto_tratamento = first_line
                                        i += 1
                                    elif len(words) > 2 and (words[0] == 'Diagnóstico' and words[1] == 'e' and words[2] == 'Tratamento'):
                                        texto_tratamento = first_line
                                        i+=1 
                                    elif len(words) == 1 and (words[0] == 'Tratamento'):
                                        next_tratamento = True
                                        i+=1
        if(texto_prevencao == ""):
                            container = soup.find_all('div', class_='column col-md-6')
                            for div in container:
                                first_line = div.text #Pega o texto da div 
                                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                                if(next_prevencao == True):
                                    texto_prevencao = f"Tratamento {first_line}"
                                    next_prevencao = False
                                for i in range(0,1):
                                    if len(words) > 1 and (words[0] == 'Prevenção') : 
                                        texto_prevencao = first_line
                                        i+=1
                                    elif len(words) == 1 and (words[0] == 'Prevenção'):
                                        next_prevencao = True
                                        i+=1
                                    elif len(words) > 2 and (words[0] == 'Sintomas' and words[1] == 'e' and words[2] == 'Prevenção'):
                                        texto_prevencao = first_line
                                        i+=1 
                                    elif len(words) > 2 and (words[0] == 'Prevenção' and words[1] == 'e' and words[2] == 'Controle'):
                                        texto_prevencao = first_line
                                        i+=1 
                                    else:
                                        i+=1
        if(texto_tratamento is not None):
            print(texto_tratamento)
        if(texto_prevencao is not None):
            print(texto_prevencao)
        if(texto_publicoalvo is not None):
            print(texto_publicoalvo)
           
    if(num == 4):
        try:
            container = soup.find_all('div', class_='row-content')
            tratamento = []
            for div in container:
                texto_div = div.text.split() if div.text else [] # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras. Caso esteja vazia o comando else a transforma em uma lista vazia
                if texto_div and texto_div[0] == "DISQUE": #Primeiro, if texto_div verifica se texto_div não está vazio. Se texto_div for uma lista vazia, então if texto_div será False e a condição if inteira será False, então o código dentro do bloco if não será executado. Se texto_div não for uma lista vazia, então if texto_div será True.
                    continue # caso seja disque e não esteja vazia, o código pulará para o append.
                tratamento.append(div.text)
            texto_tratamento = ' '.join(tratamento)  # Combina todas as strings de texto em uma única string
            #print(texto_tratamento)
            if(texto_tratamento == ""):
                container = soup.find('div', id='main')
                if container:
                    texto_tratamento = container.text
        except Exception as e:
            print(e)
        try:
            url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}"
            resposta_html = req(url)
            if resposta_html is not None:
                soup_busca = parsing(resposta_html)
                container = soup_busca.find_all('div', class_='row-content')
            else:
                print(f"Não há uma raíz para o termo {termo} na função de n = 4")
            for div in container:
                first_line = div.text #Pega o texto da div 
                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                if(next_prevencao == True):
                    texto_prevencao = f"Prevenção {first_line}"
                    next_prevencao = False
                if(next_publicoalvo == True):
                    texto_publicoalvo = f"Público Alvo {first_line}"
                    next_publicoalvo = False

                #No loop for abaixo são testados se os termos correspondem a alguma página que possua os temas: Tratamento, Prevenção ou Público Alvo. Caso em algum deles esteja em formato de lista, foram feitos códigos que pegam tais trechos
                for i in range(0,1):
                    try:
                        if(i==0):
                            if len(words) > 1 and (words[0] == 'Prevenção') : 
                                    texto_prevencao = first_line
                                    i+=1
                            elif len(words) == 1 and (words[0] == 'Prevenção'):
                                next_prevencao = True
                                i+=1
                            elif len(words) > 2 and (words[0] == 'Sintomas' and words[1] == 'e' and words[2] == 'Prevenção'):
                                texto_prevencao = first_line
                                i+=1 
                            elif len(words) > 2 and (words[0] == 'Prevenção' and words[1] == 'e' and words[2] == 'Controle'):
                                texto_prevencao = first_line
                                i+=1 
                            else:
                                i+=1
                        if(i==1):
                            if len(words) > 1 and (words[0] == 'Público') and (words[1] == "Alvo") : # caso o tamanho da lsita seja menor que 1 vamos tentar tratar a excessão
                                texto_publicoalvo = first_line
                            elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                next_publicoalvo = True
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        if(texto_prevencao == ""):
                            container = soup.find_all('div', class_='column col-md-6')
                            for div in container:
                                first_line = div.text #Pega o texto da div 
                                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                                if(next_prevencao == True):
                                    texto_prevencao = f"Tratamento {first_line}"
                                    next_prevencao = False
                                for i in range(0,1):
                                    if len(words) > 1 and (words[0] == 'Prevenção') : 
                                        texto_prevencao = first_line
                                        i+=1
                                    elif len(words) == 1 and (words[0] == 'Prevenção'):
                                        next_prevencao = True
                                        i+=1
                                    elif len(words) > 2 and (words[0] == 'Sintomas' and words[1] == 'e' and words[2] == 'Prevenção'):
                                        texto_prevencao = first_line
                                        i+=1 
                                    elif len(words) > 2 and (words[0] == 'Prevenção' and words[1] == 'e' and words[2] == 'Controle'):
                                        texto_prevencao = first_line
                                        i+=1 
                                    else:
                                        i+=1
    if(num == 3):
            try:
                container = soup.find_all('div', class_='row-content')
                prevencao = []
                for div in container:
                    texto_div = div.text.split() if div.text else [] # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras. Caso esteja vazia o comando else a transforma em uma lista vazia
                    if texto_div and texto_div[0] == "DISQUE": #Primeiro, if texto_div verifica se texto_div não está vazio. Se texto_div for uma lista vazia, então if texto_div será False e a condição if inteira será False, então o código dentro do bloco if não será executado. Se texto_div não for uma lista vazia, então if texto_div será True. PorquÊ DISQUE? Disque é a palavra que antecede a parte fora do texto e é padrão para todos os textos.
                        continue # caso seja disque e não esteja vazia, o código pulará para o append.
                    prevencao.append(div.text)
                texto_prevencao = ' '.join(prevencao)  # Combina todas4 as strings de texto em uma única string
                #print(texto_prevencao)
                if(texto_prevencao == ""):
                    container = soup_busca3.find('div', id='main')
                if container:
                    texto_prevencao = container.text
            except Exception as e:
                print(e)
            try:
                url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}"
                resposta_html = req(url)
                if resposta_html is not None:
                    soup_busca = parsing(resposta_html)
                    container = soup_busca.find_all('div', class_='row-content')
                else:
                    print(f"Não há uma raíz para o termo {termo} na função de n = 4")
                for div in container:
                    first_line = div.text #Pega o texto da div 
                    words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                    if(next_tratamento == True):
                        texto_tratamento = f"Tratamento {first_line}"
                        next_tratamento = False
                    if(next_publicoalvo == True):
                        texto_publicoalvo = f"Público Alvo {first_line}"
                        next_publicoalvo = False

                    #No loop for abaixo são testados se os termos correspondem a alguma página que possua os temas: Tratamento, Prevenção ou Público Alvo. Caso em algum deles esteja em formato de lista, foram feitos códigos que pegam tais trechos
                    for i in range(0,1):
                        try:
                            if(i == 0):
                                if len(words) > 1 and (words[0] == 'Tratamento'):
                                    texto_tratamento = first_line
                                    i += 1
                                elif len(words) > 2 and (words[0] == 'Diagnóstico' and words[1] == 'e' and words[2] == 'Tratamento'):
                                    texto_tratamento = first_line
                                    i+=1 
                                elif len(words) == 1 and (words[0] == 'Tratamento'):
                                    next_tratamento = True
                                    i+=1
                                else:
                                    i+=1
                            if(i==1):
                                if len(words) > 1 and (words[0] == 'Público') and (words[1] == "Alvo") : # caso o tamanho da lsita seja menor que 1 vamos tentar tratar a excessão
                                    texto_publicoalvo = first_line
                                elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                    next_publicoalvo = True
                        except Exception as e:
                            print(e)
            except Exception as e:
                    print(e)
            if(texto_tratamento == ""):
                                container = soup.find_all('div', class_='column col-md-6')
                                for div in container:
                                    first_line = div.text #Pega o texto da div 
                                    words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                                if(next_tratamento == True):
                                    texto_tratamento = f"Tratamento {first_line}"
                                    next_tratamento = False
                                for i in range(0,1):
                                    if len(words) > 1 and (words[0] == 'Tratamento'):
                                        texto_tratamento = first_line
                                        i += 1
                                    elif len(words) > 2 and (words[0] == 'Diagnóstico' and words[1] == 'e' and words[2] == 'Tratamento'):
                                        texto_tratamento = first_line
                                        i+=1 
                                    elif len(words) == 1 and (words[0] == 'Tratamento'):
                                        next_tratamento = True
                                        i+=1
    if(num ==2):
        try:
            container = soup.find('div',id='main')
            if container:
                texto_tratamento = container.text
                texto_prevencao = container.text
        except Exception as e:
            print(e)
    if(num == 1):
        try:
            url3 = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/prevencao"
            resposta_html3 = req(url3)
            if resposta_html3 is not None:
                soup_busca3 = parsing(resposta_html3)
            container = soup_busca3.find_all('div', class_='row-content')
            prevencao = []
            for div in container:
                texto_div = div.text.split() if div.text else [] # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras. Caso esteja vazia o comando else a transforma em uma lista vazia
                if texto_div and texto_div[0] == "DISQUE": #Primeiro, if texto_div verifica se texto_div não está vazio. Se texto_div for uma lista vazia, então if texto_div será False e a condição if inteira será False, então o código dentro do bloco if não será executado. Se texto_div não for uma lista vazia, então if texto_div será True. PorquÊ DISQUE? Disque é a palavra que antecede a parte fora do texto e é padrão para todos os textos.
                    continue # caso seja disque e não esteja vazia, o código pulará para o append.
                prevencao.append(div.text)
            texto_prevencao = ' '.join(prevencao)  # Combina todas as strings de texto em uma única string
            if(texto_prevencao == ""):
                container = soup_busca3.find('div', id='main')
                if container:
                    texto_prevencao = container.text
                #print(texto_prevencao)
        except Exception as e:
            print(e)
        try:
            container = soup.find_all('div', class_='row-content')
            tratamento = []
            for div in container:
                texto_div = div.text.split() if div.text else [] # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras. Caso esteja vazia o comando else a transforma em uma lista vazia
                if texto_div and texto_div[0] == "DISQUE": #Primeiro, if texto_div verifica se texto_div não está vazio. Se texto_div for uma lista vazia, então if texto_div será False e a condição if inteira será False, então o código dentro do bloco if não será executado. Se texto_div não for uma lista vazia, então if texto_div será True.
                    continue # caso seja disque e não esteja vazia, o código pulará para o append.
                tratamento.append(div.text)
            texto_tratamento = ' '.join(tratamento)
            if(texto_tratamento == ""):
                container = soup.find('div', id='main')
                if container:
                    texto_tratamento = container.text
                #print(texto_tratamento)
        except Exception as e:
            print(e)
    #pandas(url,titulo,texto_tratamento,texto_prevencao,texto_publicoalvo)

def pandas(url,titulo,texto_tratamento,texto_prevencao,texto_publicoalvo):
#INÍCIO DO PANDAS:
    data=dat.datetime.now()
    dia=data.day
    mes=data.month
    ano=data.year
    data=f'Acesso em: {dia}/{mes}/{ano}' # F string é uma string que possui a opção de escrever variáveis entre chaves e textos fora delas
    fonte = "Ministério da Saúde, Governo Federal"
    df = pd.DataFrame(columns=['titulo', 'texto_tratamento', 'texto_prevencao', 'texto_publicoalvo', 'url', 'data', 'fonte'])
    
    if os.path.exists('SUS.csv'):
    # Se o arquivo CSV já existe, o usa
        df = pd.read_csv('SUS.csv')
    else:
    # Se não, o criará
        df = pd.DataFrame(columns=['titulo', 'texto_tratamento', 'texto_prevencao', 'texto_publicoalvo', 'url', 'data', 'fonte'])
    
    new_data = {
    'titulo': titulo,
    'texto_tratamento': texto_tratamento,
    'texto_prevencao': texto_prevencao,
    'texto_publicoalvo': texto_publicoalvo,
    'url': url,
    'data': data,
    'fonte': fonte
    }

    df.loc[len(df)] = new_data # len df se refere a próxima linha vazia no dataframe, dessa forma localiza a próxima linha e o insere no dataframe
    df.to_csv('SUS.csv', index=False)#cria o arquivo csv, passando o dataframe para csv e criando o arquivo
    inserir(df)

# Inserção do DataFrame no banco de dados
def inserir(df):
    try:
        df.to_sql('sus2', con=connection(), if_exists='replace', index=False)
    except Exception as e:
        print(e)

            

# Há 3 possibilidades de casos de tratamento e prevenção, os quais listei abaixo. Nesse caso, para evitar o custo computacional, caso haja alguma aba para os dois, o código irá parar e mostrar que há uma aba para tratamento e prevenção. Caso contrário, ele irá verificar se há uma aba para tratamento e prevenção separadamente. Caso haja, ele irá mostrar que há uma aba para tratamento e prevenção. Caso contrário, ele irá mostrar que não há tratamento ou prevenção para o termo.
if __name__ == '__main__':
    # Sua lista de palavras como uma string
    words_string = "animais-peconhentos/acidentes-por-abelhas animais-peconhentos/acidentes-por-aranhas animais-peconhentos/acidentes-por-escorpioes animais-peconhentos/acidentes-por-lagartas animais-peconhentos/acidentes-ofidicos animais-peconhentos/aguas-vivas-e-caravelas aedes-aegypti aids-hiv amamentacao alzheimer anomalias-congenitas arboviroses arenavirus asma aspergilose ame avc bcg botulismo brucelose-humana burnout calendario-da-saúde calendario-de-vacinacao candidiase-sistemica catapora-varicela caxumba chikungunya cobreiro (herpes) coccidioidomicose cólera coqueluche covid-19 criptococose cromoblastomicose cancer-de-boca cancer-de-mama cancer-de-pele cancer-de-penis cancer-de-prostata dengue depressão depressao-pos-parto diabetes difteria doacao-de-leite doacao-de-sangue doenca-de-chagas doenca-de-creutzfeldt-jakob doenca-de-haff dda doencas-falciforme doencas-oculares drc dst dtha dt dtp dtpа ebola elefantíase enchentes epicovid-19 epidermolise-bolhosa ela esporotricose-humana esquistossomose esteatose-hepatica febre-amarela febre-do-mayaro febre-do-nilo-ocidental febre-do-oropouche febre-maculosa febre-tifoide feohifomicose fimose fusariose geo-helmintiase giardíase gravidez gripe-influenza guillain-barre hanseníase hantavirose hepatite-a hepatite-b hepatite-c hepatite-d hepatite-e herpes hidatidose-humana hipertensão histoplasmose hpv htlv ist insolacao imunizacaoo infarto influenza-aviaria lean-nas-emergencias leishmaniose-visceral lt leptospirose lupus malária meningite micetomas micoses-endemicas microcefalia mpox mucormicose oncocercose paracoccidioidomicose pense pentavalente peste poliomielite pcdt política-nacional-de-vigilância-em-saude pics raiva rotavirus rubeola salmonella samu-192 sarampo saude-da-crianca saude-da-pessoa-com-deficiencia saude-da-pessoa-idosa saude-do-adolescente saude-do-homem saude-do-viajante saude-mental saude-unica sindrome-congenita-associada-ao-zika seguranca-do-paciente sifilis sifilis-congenita sindrome-da-rubeola-congenita sindrome-de-burnout shu situações-emergenciais-de-saude suicidio-prevenção sus talassemia tetano-acidental tetano-neonatal toxoplasmose tracoma transplantes triscosporonose trombose tuberculose uma-so-saude upa-24h uso-racional-de-medicamentos vacinacao variola-dos-macacos vigitel zika-virus"
    # Transformar a string em uma lista de palavras
    words = words_string.split()
    for termo in words:
        letra=termo[0]
        #print(letra)
        #print(termo)
        i = 1
        try:
            while i <= 2:
                #OBS: tive que retirar essa url por um bug no site que faz com que 2 páginas mesmo não tendo essa página é acessada
                if(i == 0):
                    url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/tratamento-e-prevencao"
                    resposta_html = req(url)
                    if resposta_html is not None:
                        soup_busca = parsing(resposta_html)
                        print("caso 1")
                        econtrartermo(soup_busca,2,url,termo)
                        i = 3
                    else:
                        i+=1
                elif(i == 1):
                    total = 0
                    # Vamos obrigar a passar no i == 2 pois pode ser que uma das páginas não exista e tenhamos que buscar na página padrão
                    url2 = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/tratamento"
                    resposta_html2 = req(url2)
                    if resposta_html2 is not None:
                        soup_busca2 = parsing(resposta_html2)
                        total+=1
                    url3 = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/prevencao"
                    resposta_html3 = req(url3)
                    if resposta_html3 is not None:
                        soup_busca3 = parsing(resposta_html3)
                        total+=2
                    if(total == 0):
                        i=2
                    if(total == 1):
                        econtrartermo(soup_busca2,4,url2,termo) 
                        i=3
                    if(total == 2):
                        econtrartermo(soup_busca3,3,url3,termo) 
                        i=3
                    if(total == 3):
                        econtrartermo(soup_busca2,1,url2,termo) # 1 Significa que há uma página para tratamento e uma para prevenção
                        i=3
                elif(i==2):
                    url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}"
                    resposta_html = req(url)
                    if resposta_html is not None:
                        #print("caso 4")
                        soup_busca = parsing(resposta_html)
                        econtrartermo(soup_busca,5,url,termo) 
                    else:
                        print("")
                        #print(f"Não há uma página para tratamento e prevenção do termo: {termo}")
                    i = 3
                else:
                    print(f"Não há um site com a URL {termo} no site do governo federal")
        except Exception as e:
            print(e)