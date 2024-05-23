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

#Função principal, na qual há o scraping dos diferentes casos selecionados para a pesquisa, como demonstrados no if __name__ == '__main__'
def econtrartermo(soup,num,url,titulo):
    texto_prevencao = ""
    texto_tratamento = ""   
    texto_publicoalvo = ""
    texto=""
    next_prevencao = False
    next_tratamento = False
    next_publicoalvo = False
    m=0
    #página root
    if(num==5): 
        try:
            container = soup.find_all('div', class_='row-content')
            for div in container:
                first_line = div.text #Pega o texto da div 
                words = first_line.split() # Pega a primeira palavra do texto da div, que será transformada em uma lista de todas as palavras
                if(next_prevencao == True):
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
                        if(i==2):
                            if len(words) > 1 and (words[0] == 'Público') and (words[1] == "Alvo") : # caso o tamanho da lsita seja menor que 1 vamos tentar tratar a excessão
                                texto_publicoalvo = first_line
                                i+=1
                            elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                next_publicoalvo = True
                                i+=1
                            else:
                                i+=1
                        if(i==3):
                            while m < len(container):
                                div = container[m]
                                if (m == 2):
                                    texto = div.text
                                m += 1
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
        '''                                
        if(texto_tratamento is not None):
            print(texto_tratamento)
        if(texto_prevencao is not None):
            print(texto_prevencao)
        if(texto_publicoalvo is not None):
            print(texto_publicoalvo)
        '''
    #Caso exista a página de tratamento       
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
                                i+=1
                            elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                next_publicoalvo = True
                                i+=1
                            else:
                                i+=1
                        if(i==2):
                               while m < len(container):
                                div = container[m]
                                if (m == 2):
                                    texto = div.text
                                m += 1
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
    #caso exista a página de prevenção
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
                                    i+=1
                                elif len(words) == 2 and (words[0] == 'Público') and (words[1] == "Alvo"):
                                    next_publicoalvo = True
                                    i+=1
                                else:
                                    i+=1
                            if(i==2):
                                while m < len(container):
                                    div = container[m]
                                    if (m == 2):
                                        texto = div.text
                                    m += 1
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
    #Caso a página concerte os bugs presentes e seja possível acessar a página de tratamento e prevenção
    if(num ==2):
        try:
            container = soup.find('div',id='main')
            if container:
                texto_tratamento = container.text
                texto_prevencao = container.text
        except Exception as e:
            print(e)
    #Caso em que há 1 página para tratamento e 1 para prevenção
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
                print(texto_prevencao)
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

        try:
            url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}"
            resposta_html = req(url)
            for div in container:
                #No loop for abaixo são testados se os termos correspondem a alguma página que possua os temas: Tratamento, Prevenção ou Público Alvo. Caso em algum deles esteja em formato de lista, foram feitos códigos que pegam tais trechos
                for i in range(0,1):
                    try:
                        if(i==0):
                            while m < len(container):
                                div = container[m]
                                if (m == 2):
                                    texto = div.text
                                    print(texto)
                                m += 1
                    except Exception as e:
                        print(e)
        except Exception as e:
                print(e)
        
    pandas(url,titulo,texto_tratamento,texto_prevencao,texto_publicoalvo,texto)

def pandas(url,titulo,texto_tratamento,texto_prevencao,texto_publicoalvo,texto):
#INÍCIO DO PANDAS:
    data=dat.datetime.now()
    dia=data.day
    mes=data.month
    ano=data.year
    data=f'Acesso em: {dia}/{mes}/{ano}' # F string é uma string que possui a opção de escrever variáveis entre chaves e textos fora delas
    fonte = "Ministério da Saúde, Governo Federal"
    df = pd.DataFrame(columns=['titulo', 'texto_tratamento', 'texto_prevencao', 'texto_publicoalvo', 'texto', 'url', 'data', 'fonte'])
    
    if os.path.exists('SUS.csv'):
    # Se o arquivo CSV já existe, o usa
        df = pd.read_csv('SUS.csv')
    else:
    # Se não, o criará
        df = pd.DataFrame(columns=['titulo', 'texto_tratamento', 'texto_prevencao', 'texto_publicoalvo', 'texto', 'url', 'data', 'fonte'])
    
    new_data = {
    'titulo': titulo,
    'texto_tratamento': texto_tratamento,
    'texto_prevencao': texto_prevencao,
    'texto_publicoalvo': texto_publicoalvo,
    'texto': texto,
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
    words_string = "animais-peconhentos/acidentes-por-abelhas animais-peconhentos/acidentes-por-aranhas animais-peconhentos/acidentes-por-escorpioes animais-peconhentos/acidentes-por-lagartas animais-peconhentos/acidentes-ofidicos animais-peconhentos/aguas-vivas-e-caravelas aedes-aegypti aids-hiv amamentacao alzheimer anomalias-congenitas arboviroses arenavirus asma aspergilose ame avc bcg botulismo brucelose-humana burnout calendario-da-saúde calendario-de-vacinacao candidiase-sistemica catapora-varicela caxumba chikungunya cobreiro (herpes) coccidioidomicose cólera coqueluche covid-19 criptococose cromoblastomicose cancer-de-boca cancer-de-mama cancer-de-pele cancer-de-penis cancer-de-prostata dengue depressão depressao-pos-parto diabetes difteria doacao-de-leite doacao-de-sangue doenca-de-chagas dcj doenca-de-haff dda doencas-falciforme doencas-oculares drc dst dtha dt dtp dtpa ebola elefantíase enchentes epicovid-19 epidermolise-bolhosa ela esporotricose-humana esquistossomose esteatose-hepatica febre-amarela febre-do-mayaro febre-do-nilo-ocidental febre-do-oropouche febre-maculosa febre-tifoide feohifomicose fimose fusariose geo-helmintiase giardíase gravidez gripe-influenza guillain-barre hanseníase hantavirose hepatite-a hepatite-b hepatite-c hepatite-d hepatite-e herpes hidatidose-humana hipertensão histoplasmose hpv htlv ist insolacao imunizacaoo infarto influenza-aviaria lean-nas-emergencias leishmaniose-visceral lt leptospirose lupus malária meningite micetomas micoses-endemicas microcefalia mpox mucormicose oncocercose paracoccidioidomicose pense pentavalente peste poliomielite pcdt política-nacional-de-vigilância-em-saude pics raiva rotavirus rubeola salmonella samu-192 sarampo saude-da-crianca saude-da-pessoa-com-deficiencia saude-da-pessoa-idosa saude-do-adolescente saude-do-homem saude-do-viajante saude-mental saude-unica sindrome-congenita-associada-ao-zika seguranca-do-paciente sifilis sifilis-congenita sindrome-da-rubeola-congenita sindrome-de-burnout shu situações-emergenciais-de-saude suicidio-prevenção sus talassemia tetano-acidental tetano-neonatal toxoplasmose tracoma transplantes triscosporonose trombose tuberculose uma-so-saude upa-24h uso-racional-de-medicamentos vacinacao variola-dos-macacos vigitel zika-virus"
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

#Comandos SQL necessários para a execução do código
'''
OBS: USAR O SEGUINTE CÓDIGO:
SET SQL_SAFE_UPDATES = 0;
UPDATE `teste_tcc`.`sus2` SET `texto` = 'Asma é uma das doenças respiratórias crônicas mais comuns, juntamente com a rinite alérgica e a doença pulmonar obstrutiva crônica. As principais características dessa doença pulmonar são dificuldade de respirar, chiado e aperto no peito, respiração curta e rápida. Os sintomas pioram à noite e nas primeiras horas da manhã ou em resposta à prática de exercícios físicos, à exposição a alérgenos, à poluição ambiental e a mudanças climáticas.' WHERE (`titulo` = 'asma');
UPDATE `teste_tcc`.`sus2` SET `texto_tratamento` = 'Tratamento e prevenção\nCompartilhe:  Compartilhe por Facebook Compartilhe por Twitter Compartilhe por LinkedIn Compartilhe por WhatsApplink para Copiar para área de transferência\nPublicado em 19/10/2022 16h38 Atualizado em 20/10/2022 09h52\nA cirurgia oncológica é o tratamento mais indicado para tratar o câncer de pele para a retirada da lesão, que, em estágios iniciais, pode ser realizada em nível ambulatorial (sem internação). Já para casos mais avançados e para o câncer de pele melanoma, o tratamento vai variar de acordo com tamanho e estadiamento do tumor, podendo ser indicadas, além de cirurgia, a radioterapia e a quimioterapia, conforme cada caso.\n\nAlém disso, existe também a terapia fotodinâmica (uso de um creme fotossensível e posterior aplicação de uma fonte de luz), que é mais uma opção de tratamento para a ceratose actínica (lesão precursora do câncer de pele), carcinoma basocelular superficial e carcinoma epidermoide \"in situ\" (Doença de Bowen). A criocirurgia e a imunoterapia tópica são também opções para o tratamento desses cânceres. No entanto, exigem indicação precisa feita por um especialista experiente.\n\nQuando há metástase (o câncer já se espalhou para outros órgãos), o melanoma, hoje, é tratado com novos medicamentos, que apresentam altas taxas de sucesso terapêutico. A estratégia de tratamento para a doença avançada deve ter como objetivo postergar a evolução da doença, oferecendo chance de sobrevida mais longa aos pacientes.\n\nA principal recomendação para a prevenção do câncer de pele é evitar a exposição ao sol, principalmente nos horários em que os raios solares são mais intensos (entre 10h e 16h), bem como utilizar óculos de sol com proteção UV, roupas que protegem o corpo, chapéus de abas largas, sombrinhas e guarda-sol.\n\nAtualmente, estão disponíveis no mercado roupas e acessórios com proteção UV, que dão maior proteção contra os raios solares. Em caso de exposição solar necessária, principalmente em torno do meio-dia, recomenda-se a procura por áreas cobertas que forneçam sombra, como embaixo de árvores, marquises e toldos, com o objetivo de minimizar os efeitos da radiação solar.\n\nO uso de filtro solar com fator de proteção solar (FPS) 15 ou mais é fundamental, principalmente quando a exposição ao sol é inevitável. O filtro solar deve ser aplicado corretamente, uma vez que o real fator de proteção desses produtos varia com a espessura da camada de creme aplicada, a frequência da aplicação, a perspiração e a exposição à água. De mesmo modo, deve ser utilizado também o protetor labial.\n\nRecomendações especiais devem ser direcionadas aos bebês e às crianças, por ser, a infância, o período da vida mais suscetível aos efeitos danosos da radiação UV que se manifestam mais tardiamente na fase adulta.\n\nNas atividades ocupacionais, pode ser necessário reformular as jornadas de trabalho ou a organização das tarefas desenvolvidas ao longo do dia.\n\nImportante: Em dias nublados também é importante usar as proteções necessárias. As tatuagens podem esconder lesões, por isso merecem atenção. É necessário reaplicar o filtro solar a cada duas horas, durante a exposição solar, assim como após mergulho ou grande transpiração. Mesmo os filtros solares \"à prova d´água\" devem ser reaplicados.', `texto_prevencao` = 'Tratamento e prevenção\nCompartilhe:  Compartilhe por Facebook Compartilhe por Twitter Compartilhe por LinkedIn Compartilhe por WhatsApplink para Copiar para área de transferência\nPublicado em 19/10/2022 16h38 Atualizado em 20/10/2022 09h52\nA cirurgia oncológica é o tratamento mais indicado para tratar o câncer de pele para a retirada da lesão, que, em estágios iniciais, pode ser realizada em nível ambulatorial (sem internação). Já para casos mais avançados e para o câncer de pele melanoma, o tratamento vai variar de acordo com tamanho e estadiamento do tumor, podendo ser indicadas, além de cirurgia, a radioterapia e a quimioterapia, conforme cada caso.\n\nAlém disso, existe também a terapia fotodinâmica (uso de um creme fotossensível e posterior aplicação de uma fonte de luz), que é mais uma opção de tratamento para a ceratose actínica (lesão precursora do câncer de pele), carcinoma basocelular superficial e carcinoma epidermoide \"in situ\" (Doença de Bowen). A criocirurgia e a imunoterapia tópica são também opções para o tratamento desses cânceres. No entanto, exigem indicação precisa feita por um especialista experiente.\n\nQuando há metástase (o câncer já se espalhou para outros órgãos), o melanoma, hoje, é tratado com novos medicamentos, que apresentam altas taxas de sucesso terapêutico. A estratégia de tratamento para a doença avançada deve ter como objetivo postergar a evolução da doença, oferecendo chance de sobrevida mais longa aos pacientes.\n\nA principal recomendação para a prevenção do câncer de pele é evitar a exposição ao sol, principalmente nos horários em que os raios solares são mais intensos (entre 10h e 16h), bem como utilizar óculos de sol com proteção UV, roupas que protegem o corpo, chapéus de abas largas, sombrinhas e guarda-sol.\n\nAtualmente, estão disponíveis no mercado roupas e acessórios com proteção UV, que dão maior proteção contra os raios solares. Em caso de exposição solar necessária, principalmente em torno do meio-dia, recomenda-se a procura por áreas cobertas que forneçam sombra, como embaixo de árvores, marquises e toldos, com o objetivo de minimizar os efeitos da radiação solar.\n\nO uso de filtro solar com fator de proteção solar (FPS) 15 ou mais é fundamental, principalmente quando a exposição ao sol é inevitável. O filtro solar deve ser aplicado corretamente, uma vez que o real fator de proteção desses produtos varia com a espessura da camada de creme aplicada, a frequência da aplicação, a perspiração e a exposição à água. De mesmo modo, deve ser utilizado também o protetor labial.\n\nRecomendações especiais devem ser direcionadas aos bebês e às crianças, por ser, a infância, o período da vida mais suscetível aos efeitos danosos da radiação UV que se manifestam mais tardiamente na fase adulta.\n\nNas atividades ocupacionais, pode ser necessário reformular as jornadas de trabalho ou a organização das tarefas desenvolvidas ao longo do dia.\n\nImportante: Em dias nublados também é importante usar as proteções necessárias. As tatuagens podem esconder lesões, por isso merecem atenção. É necessário reaplicar o filtro solar a cada duas horas, durante a exposição solar, assim como após mergulho ou grande transpiração. Mesmo os filtros solares \"à prova d´água\" devem ser reaplicados.' WHERE (titulo = 'cancer-de-pele');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'A Unidade de Pronto Atendimento - UPA 24h é um dos componentes da Política Nacional de Atenção às Urgências do Ministério da Saúde, e integra a rede de serviços pré-hospitalares fixos para o atendimento às urgências.' WHERE (`titulo` = 'upa-24h');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'Acidentes ofídicos, ou simplesmente ofidismo, é o quadro clínico decorrente da mordedura de serpentes. No Brasil é comum chamar as serpentes de “cobras”. Este nome é mais corretamente empregado para se referir às serpentes da Família Elapidae, no Brasil representada pelas cobras corais verdadeiras. Algumas espécies de serpentes produzem uma peçonha em suas glândulas veneníferas capazes de perturbar os processos fisiológicos e bioquímicos normais de uma possível vítima, causando alterações do tipo colinérgicas, hemorrágicas, anticoagulantes, necróticas, miotóxicas, citolíticas e inflamatórias. Algumas espécies de serpentes peçonhentas são de interesse em saúde pública. Elas pertencem à duas famílias: Viperidae e Elapidae.' WHERE (`titulo` = 'animais-peconhentos/acidentes-ofidicos');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'Acidentes por aranhas, ou araneísmo, é o quadro clínico de envenenamento decorrente da inoculação da peçonha de aranhas, através de um par de ferrões localizados na parte anterior do animal. Assim como os escorpiões, as aranhas são representantes da classe dos aracnídeos.' WHERE (`titulo` = 'animais-peconhentos/acidentes-por-aranhas');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'As anomalias congênitas são um grupo de alterações estruturais ou funcionais que ocorrem durante a vida intrauterina e que podem ser detectadas antes, durante ou após o nascimento. Podem afetar diversos órgãos e sistemas do corpo humano e são causadas por um ou mais fatores genéticos, infecciosos, nutricionais e ambientais, podendo ser resultado de uma combinação desses fatores.' WHERE (`titulo` = 'anomalias-congenitas');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'O botulismo é uma doença neuroparalítica grave, rara, não contagiosa, causada pela ação de uma potente toxina produzida pela bactéria Clostridium botulinum (C botulinum). O agente etiológico entra no organismo por meio de ferimentos ou pela ingestão de alimentos contaminados que não têm produção e/ou conservação adequada. Sua notificação é compulsória e imediata (em até 24 horas) para que as ações de vigilância sejam realizadas em tempo de prevenir outros casos. A doença pode levar à morte por paralisia da musculatura respiratória.' WHERE (`titulo` = 'botulismo');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'A Esteatose hepática, popularmente conhecida como Gordura no Fígado, é um problema de saúde que acontece quando as células do fígado são infiltradas por células de gordura. É normal haver presença de gordura no fígado, no entanto quando este índice chega a 5% ou mais o quadro deve ser tratado o mais brevemente possível. Se não tratada corretamente, a Estatose hepática pode provocar, a médio e longo prazo, uma inflamação capaz de evoluir para quadros mais graves de hepatite gordurosa, cirrose hepática e até câncer no fígado.' WHERE (`titulo` = 'esteatose-hepatica');
UPDATE `teste_tcc`.`sus2` SET `texto` = 'Salmonella (Salmonellose) é uma bactéria da família das Enterobacteriaceae que causa intoxicação alimentar e em casos raros, pode provocar graves infecções e até mesmo a morte. É uma bactéria que possui duas espécies causadoras de doenças em humanos: S. enterica e S. bongori.  A Salmonella enterica, de maior relevância para a saúde pública, é composta por seis subespécies (S. enterica subsp. entérica, S. enterica subsp. salamae, S. enterica subsp. arizonae, S. enterica subsp. diarizonae, S. enterica subsp houtenae,  S. enterica subsp. indica). ' WHERE (`titulo` = 'salmonella');
UPDATE `teste_tcc`.`sus2` SET `texto_tratamento` = NULL WHERE (`titulo` = 'saude-mental');
UPDATE `teste_tcc`.`sus2` SET `texto_prevencao` = 'A prevenção do câncer de mama não é totalmente possível em função da multiplicidade de fatores relacionados ao surgimento da doença e ao fato de vários deles não serem modificáveis. De modo geral, a prevenção baseia-se no controle dos fatores de risco e no estímulo aos fatores protetores, especificamente aqueles considerados modificáveis.' WHERE (`titulo` = 'cancer-de-mama');
UPDATE `teste_tcc`.`sus2` SET `texto_tratamento` = 'Tratamento   Compartilhe:  Compartilhe por Facebook Compartilhe por Twitter Compartilhe por LinkedIn Compartilhe por WhatsApplink para Copiar para área de transferência\nPublicado em 17/10/2022 11h43 Atualizado em 10/02/2023 16h56\nOs medicamentos antirretrovirais (ARV) surgiram na década de 1980 para impedir a multiplicação do HIV no organismo. Esses medicamentos ajudam a evitar o enfraquecimento do sistema imunológico. Por isso, o uso regular dos ARV é fundamental para aumentar o tempo e a qualidade de vida das pessoas que vivem com HIV e reduzir o número de internações e infecções por doenças oportunistas.\n\nDesde 1996, o Brasil distribui gratuitamente os ARV a todas as pessoas vivendo com HIV que necessitam de tratamento. Atualmente, existem 22 medicamentos, em 38 apresentações farmacêuticas, conforme relação abaixo:\n\nItem	Descrição	Unidade de fornecimento\n1	Abacavir (ABC) 300mg	Comprimido revestido\n2	Abacavir (ABC) solução oral	Frasco\n3	Darunavir 800mg	\n4	Atazanavir (ATV) 300mg	Cápsula gelatinosa dura\n5	Darunavir (DRV) 75mg	Comprimido revestido\n6	Darunavir (DRV) 150mg	Comprimido revestido\n7	Darunavir (DRV) 600mg	Comprimido revestido\n8	Dolutegravir (DTG) 50mg	Comprimido revestido\n9	Efavirenz (EFZ) 200mg	Cápsula gelatinosa dura\n10	Efavirenz (EFZ) 600mg	Comprimido revestido\n11	Efavirenz (EFZ) solução oral	Frasco\n12	Enfuvirtida (T20)	Frasco-ampola\n13	Entricitabina 200mg + tenofovir 300mg	Comprimido revestido\n14	Etravirina (ETR) 100mg	Comprimido revestido\n15	Etravirina (ETR) 200mg	Comprimido revestido\n16	Raltegravir (RAL) granulado 100mg	Sachê\n17	Lamivudina (3TC) 150mg	Comprimido revestido\n18	Lamivudina 150mg + zidovudina 300mg (AZT + 3TC)	Comprimido revestido\n19	Lamivudina (3TC) solução oral	Frasco\n20	Lopinavir 100mg + ritonavir 25mg (LPV/r)	Comprimido revestido\n21	Lopinavir 80mg/mL + ritonavir 20mg/mL (LPV/r solução oral)	Frasco\n22	Lopinavir/ritonavir (LPV/r) 200mg + 50mg	Comprimido revestido\n23	Maraviroque (MVC) 150mg	Comprimido revestido\n24	Nevirapina (NVP) 200mg	Comprimido simples\n25	Nevirapina (NVP) suspensão oral	Frasco\n26	Raltegravir (RAL) 100mg	Comprimido mastigável\n27	Raltegravir (RAL) 400mg	Comprimido revestido\n28	Ritonavir (RTV) 100mg	Comprimido revestido\n29	Ritonavir (RTV) 80mg/mL	Frasco\n30	Tenofovir (TDF) 300mg	Comprimido revestido\n31	Tenofovir 300mg + lamivudina 300mg	Comprimido revestido\n32	Tenofovir 300mg + lamivudina 300mg + efavirenz 600mg	Comprimido revestido\n33	Tipranavir (TPV) 100mg/mL	Frasco\n34	Tipranavir (TPV) 250mg	Cápsula gelatinosa mole\n35	Zidovudina (AZT) 100mg	Cápsula gelatinosa dura\n36	Zidovudina (AZT) solução injetável	Frasco-ampola\n37	Zidovudina (AZT) xarope	Frasco' WHERE (`titulo` = 'aids-hiv');
UPDATE `teste_tcc`.`sus2` SET `texto_prevencao` = 'Prevenção Compartilhe:  Compartilhe por Facebook Compartilhe por Twitter Compartilhe por LinkedIn Compartilhe por WhatsApplink para Copiar para área de transferência\nPublicado em 17/10/2022 12h12 Atualizado em 06/02/2024 15h50\nA melhor técnica de evitar a Aids / HIV é a prevenção combinada, que consiste no uso simultâneo de diferentes abordagens de prevenção, aplicadas em diversos níveis para responder as necessidades específicas de determinados segmentos populacionais e de determinadas formas de transmissão do HIV.\n\nPor isso, se você passou por uma situação de risco, como ter feito sexo desprotegido ou compartilhado seringas, faça o teste de HIV. Caso a exposição sexual de risco tenha acontecido há menos de 72 horas, informe-se sobre a Profilaxia Pós-Exposição ao HIV (PEP). O diagnóstico da infecção pelo HIV é feito a partir da coleta de sangue ou por fluido oral. No Brasil, temos os exames laboratoriais e os testes rápidos, que detectam os anticorpos contra o HIV em cerca de 30 minutos. Esses testes são realizados gratuitamente pelo Sistema Único de Saúde (SUS), nas unidades da rede pública e nos Centros de Testagem e Aconselhamento (CTA).\n\nIntervenções biomédicas\nSão ações voltadas à redução do risco de exposição, mediante intervenção na interação entre o HIV e a pessoa passível de infecção. Essas estratégias podem ser divididas em dois grupos: intervenções biomédicas clássicas, que empregam métodos de barreira física ao vírus, já largamente utilizados no Brasil; e intervenções biomédicas baseadas no uso de antirretrovirais (ARV).\n\nComo exemplo do primeiro grupo, tem-se a distribuição de preservativos masculinos e femininos e de gel lubrificante. Os exemplos do segundo grupo incluem o Tratamento para Todas as Pessoas – TTP, a Profilaxia Pós-Exposição – PEP e a Profilaxia Pré-Exposição – PrEP.\n\nIntervenções comportamentais\nSão ações que contribuem para o aumento da informação e da percepção do risco de exposição ao HIV e para sua consequente redução, mediante incentivos a mudanças de comportamento da pessoa e da comunidade ou grupo social em que ela está inserida.\n\nComo exemplos, podem ser citados: incentivo ao uso de preservativos masculinos e femininos, aconselhamento sobre HIV/aids e outras IST, incentivo à testagem, adesão às intervenções biomédicas, vinculação e retenção nos serviços de saúde, redução de danos para as pessoas que usam álcool e outras drogas e estratégias de comunicação e educação entre pares.\n\nIntervenções estruturais\nSão ações voltadas aos fatores e condições socioculturais que influenciam diretamente a vulnerabilidade de indivíduos ou grupos sociais específicos ao HIV, envolvendo preconceito, estigma, discriminação ou qualquer outra forma de alienação dos direitos e garantias fundamentais à dignidade humana.\n\nPodemos enumerar como exemplos: ações de enfrentamento ao racismo, sexismo, LGBTfobia e demais preconceitos, promoção e defesa dos direitos humanos, campanhas educativas e de conscientização.\n\nComo forma de subsidiar profissionais, trabalhadores(as) e gestores(as) de saúde para o planejamento e implementação das ações de Prevenção Combinada, o Departamento de IST, HIV/Aids e Hepatites Virais apresenta um conjunto de recomendações, expressas na publicação “Prevenção Combinada do HIV: Bases conceituais para profissionais, trabalhadores(as) e gestores(as) de saúde\".\n\nEspera-se que, a partir da leitura do documento, tenham-se mais elementos para responder às necessidades específicas de determinados públicos a determinadas formas de transmissão do HIV.\n\nRepresentação gráfica da Prevenção Combinada\nUma das maneiras de pensar a Prevenção Combinada é por meio da \"mandala\". O princípio da estratégia da Prevenção Combinada baseia-se na livre conjugação dessas ações, sendo essa combinação determinada pelas populações envolvidas nas ações de prevenção estabelecidas (população-chave, prioritária ou geral) e pelos meios em que estão inseridas.\n\nPopulações-chave\nA epidemia brasileira é concentrada em alguns segmentos populacionais que, muitas vezes, estão inseridos em contextos que aumentam suas vulnerabilidades e apresentam prevalência para o HIV superior à média nacional, que é de 0,4%. Essas populações são:\n\nGays e outros HSH;\nPessoas trans;\nPessoas que usam álcool e outras drogas;\nPessoas privadas de liberdade;\nTrabalhadoras do sexo.\nPopulações prioritárias\nSão segmentos populacionais que possuem caráter transversal e suas vulnerabilidades estão relacionadas às dinâmicas sociais locais e às suas especificidades. Essas populações são:\n\nPopulação de adolescentes e jovens;\nPopulação negra;\nPopulação indígena;\nPopulação em situação de rua.\nPré-natal\nDurante a gestação e no parto, pode ocorrer a transmissão do HIV (vírus causador da Aids), e também da sífilis e da hepatite B para o bebê. O HIV também pode ser transmitido durante a amamentação. Por isso as gestantes, e também seus parceiros sexuais, devem realizar os testes para HIV, sífilis e hepatites durante o pré-natal e no parto.\n\nO diagnóstico e o tratamento precoce podem garantir o nascimento saudável do bebê. Informe-se com um profissional de saúde sobre a testagem.\n\nQue testes a gestante deve realizar no pré-natal?\n\nNos três primeiros meses de gestação: HIV, sífilis e hepatites;\nNos três últimos meses de gestação: HIV e sífilis;\nEm caso de exposição de risco e/ou violência sexual: HIV, sífilis e hepatites;\nEm caso de aborto: sífilis.\nOs testes para HIV e para sífilis também devem ser realizados no momento do parto, independentemente de exames anteriores. O teste de hepatite B também deve ser realizado no momento do parto, caso a gestante não tenha recebido a vacina.\n\nE se o teste for positivo para o HIV durante a gestação?\n\nAs gestantes que forem diagnosticadas com HIV durante o pré-natal têm indicação de tratamento com os medicamentos antirretrovirais durante toda gestação e, se orientado pelo médico, também no parto. O tratamento previne a transmissão vertical do HIV para a criança.\n\nO recém-nascido deve receber o medicamento antirretroviral (xarope) e ser acompanhado no serviço de saúde. Recomenda-se também a não amamentação, evitando a transmissão do HIV para a criança por meio do leite materno\n\nImportante: Mulheres com diagnóstico negativo para HIV durante o pré-natal ou parto devem utilizar camisinha (masculina ou feminina) nas relações sexuais, inclusive durante o período de amamentação, prevenindo a infecção e possibilitando o crescimento saudável do bebê.\n\nTestagem para o HIV\nO Sistema Único de Saúde (SUS) oferece gratuitamente testes para diagnóstico do HIV (o vírus causador da Aids), e também para diagnostico da sífilis e das hepatites B e C. Existem, no Brasil, dois tipos de testes: os exames laboratoriais e os testes rápidos.\n\nOs testes rápidos são práticos e de fácil execução; podem ser realizados com a coleta de uma gota de sangue ou com fluido oral e fornecem o resultado em, no máximo, 30 minutos.\n\nQuando fazer o teste de HIV?\n\nO teste de HIV deve ser feito com regularidade e sempre que você tiver passado por uma situação de risco, como ter feito sexo sem camisinha. É muito importante que você saiba se tem HIV, para buscar tratamento no tempo certo, possibilitando que você ganhe muito em qualidade de vida. Procure um profissional de saúde e informe-se sobre o teste.\n\nPor que usar preservativos?\nO preservativo, ou camisinha, é o método mais conhecido, acessível e eficaz para se prevenir da infecção pelo HIV e outras infecções sexualmente transmissíveis (IST), como a sífilis, a gonorreia e também alguns tipos de hepatites. Além disso, ele evita uma gravidez não planejada.\n\nExistem dois tipos de camisinha: a masculina, que é feita de látex e deve ser colocada no pênis ereto antes da penetração; e a feminina, que é feita de látex ou borracha nitrílica e é usada internamente na vagina, podendo ser colocada algumas horas antes da relação sexual, não sendo necessário aguardar a ereção do pênis.\n\nOnde pegar os preservativos?\n\nOs preservativos masculino e feminino são distribuídos gratuitamente em qualquer serviço público de saúde. Caso você não saiba onde retirá-los, ligue para o Disque Saúde (136).\n\nSaiba que a retirada gratuita de preservativo nas unidades de saúde é um direito seu; por isso, não devem ser impostas quaisquer barreiras ou condições para que você os obtenha. Retire quantos preservativos masculinos ou femininos você julgar que necessite.\n\nComo usar os preservativos?\n\nManusear a camisinha é muito fácil. Treine antes - assim você não erra na hora. Durante as preliminares, colocar a camisinha no(a) parceiro(a) pode se tornar um momento prazeroso. Só é preciso seguir o modo correto de uso.\n\nAtenção: Nunca reutilize a camisinha e também nunca use duas camisinhas ao mesmo tempo, pois ela pode se romper ou estourar.\n\nPEP (Profilaxia Pós-Exposição ao HIV)\nA PEP é uma medida de prevenção de urgência à infecção pelo HIV, hepatites virais e outras infecções sexualmente transmissíveis (IST), que consiste no uso de medicamentos para reduzir o risco de adquirir essas infecções. Deve ser utilizada após qualquer situação em que exista risco de contágio, tais como:\n\nViolência sexual;\nRelação sexual desprotegida (sem o uso de camisinha ou com rompimento da camisinha);\nAcidente ocupacional (com instrumentos perfurocortantes ou contato direto com material biológico).\nA PEP é uma tecnologia inserida no conjunto de estratégias da Prevenção Combinada, cujo principal objetivo é ampliar as formas de intervenção para atender às necessidades e possibilidades de cada pessoa e evitar novas infecções pelo HIV, hepatites virais e outras IST.\n\nComo funciona a PEP para o HIV?\n\nComo profilaxia para o risco de infecção para o HIV, a PEP consiste no uso de medicamentos antirretrovirais para reduzir o risco de infecção em situações de exposição ao vírus.\n\nTrata-se de uma urgência médica, que deve ser iniciada o mais rápido possível - preferencialmente nas primeiras duas horas após a exposição e no máximo em até 72 horas. A duração da PEP é de 28 dias e a pessoa deve ser acompanhada pela equipe de saúde.\n\nRecomenda-se avaliar todo paciente com exposição sexual de risco ao HIV para um eventual episódio de infecção aguda pelos vírus das hepatites A, B e C.\n\nOnde encontrar a PEP?\n\nA PEP é oferecida gratuitamente pelo SUS. Acesse os serviços que realizam atendimento de PEP.\n\nPrEP (Profilaxia Pré-Exposição ao HIV) \nA Profilaxia Pré-Exposição ao HIV (PrEP, do inglês Pre-Exposure Prophylaxis) consiste no uso de antirretrovirais (ARV) que são utilizados antes da exposição para reduzir o risco de adquirir a infecção pelo HIV. Essa estratégia tem se mostrado eficaz e segura em pessoas com risco aumentado de adquirir a infecção.' WHERE (`titulo` = 'aids-hiv');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doença de alzheimer' WHERE (`titulo` = 'alzheimer');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Lúpus' WHERE (`titulo` = 'lupus');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Infecções por Salmonella' WHERE (`titulo` = 'salmonella');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Vacinas' WHERE (`titulo` = 'vacinacao');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Asma' WHERE (`titulo` = 'asma');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Câncer de Pele' WHERE (`titulo` = 'cancer-de-pele');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Câncer de Penis' WHERE (`titulo` = 'cancer-de-penis');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Câncer de Mama' WHERE (`titulo` = 'cancer-de-mama');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Dengue' WHERE (`titulo` = 'dengue');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Câncer de prostata' WHERE (`titulo` = 'cancer-de-prostata');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doenças Oculares' WHERE (`titulo` = 'doencas-oculares');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Depressão pós-parto' WHERE (`titulo` = 'depressao-pos-parto');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Ébola' WHERE (`titulo` = 'ebola');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doença de Chagas' WHERE (`titulo` = 'doenca-de-chagas');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Herpes Simples' WHERE (`titulo` = 'herpes');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Rubéola' WHERE (`titulo` = 'rubeola');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Raiva' WHERE (`titulo` = 'raiva');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde da Criança' WHERE (`titulo` = 'saude-da-crianca');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde da pessoa com deficiência'WHERE (`titulo` = 'saude-da-pessoa-com-deficiencia');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde do Idoso' WHERE (`titulo` = 'saude-da-pessoa-idosa');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde do Adolescente' WHERE (`titulo` = 'saude-do-adolescente');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'A Saúde dos homens' WHERE (`titulo` = 'saude-do-homem');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde dos viajantes' WHERE (`titulo` = 'saude-do-viajante');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Saúde Mental' WHERE (`titulo` = 'saude-mental');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Sífilis' WHERE (`titulo` = 'sifilis');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'HIV' WHERE (`titulo` = 'aids-hiv');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doenças Sexualmente Transmissíveis' WHERE (`titulo` = 'dst');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'AVC' WHERE (`titulo` = 'avc');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Catapora' WHERE (`titulo` = 'catapora-varicela');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Câncer bucal' WHERE (`titulo` = 'cancer-de-boca');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doenças Diarreicas' WHERE (`titulo` = 'dda');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Vírus Zika' WHERE (`titulo` = 'zika-virus');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doença Renal Crônica' WHERE (`titulo` = 'drc');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doenças de Transmissão Hídrica e Alimentar' WHERE (`titulo` = 'dtha');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Esclerose Lateral Amiotrófica(ela)' WHERE (`titulo` = 'ela');
UPDATE `teste_tcc`.`sus2` SET `titulo` = 'Doença de Creutzfeldt-Jakob' WHERE (`titulo` = 'dcj');
ALTER TABLE `teste_tcc`.`sus2` 
ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST,
ADD PRIMARY KEY (`id`);
;
'''
