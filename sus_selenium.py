from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def selenium(url,num):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        html = driver.page_source
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    parsing(html,num)

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

def parsing(resposta_html,num):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        econtrartermo(soup,num)
        return soup
    except Exception as e:
        print("Falha ao fazer o parsing")
        print(e)

def econtrartermo(soup,num):
    print("AQUI ESTAMOSSS")
    print(num)
    if(num==4):    
        try:
            container = soup.find_all('div')
            for div in container:
                first_line = div.text.split('\n')[0]
                print(first_line)
        except Exception as e:
            print(e)

# Há 3 possibilidades de casos de tratamento e prevenção, os quais listei abaixo. Nesse caso, para evitar o custo computacional, caso haja alguma aba para os dois, o código irá parar e mostrar que há uma aba para tratamento e prevenção. Caso contrário, ele irá verificar se há uma aba para tratamento e prevenção separadamente. Caso haja, ele irá mostrar que há uma aba para tratamento e prevenção. Caso contrário, ele irá mostrar que não há tratamento ou prevenção para o termo.
if __name__ == '__main__':
    # Sua lista de palavras como uma string
    words_string = "animais-peconhentos/acidentes-por-abelhas"
    # Transformar a string em uma lista de palavras
    words = words_string.split()
    for termo in words:
        letra=termo[0]
        print(letra)
        print(termo)
        try:
            for i in range(0,3):
                if(i == 0):
                    url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/tratamento-e-prevencao"
                    resposta_html = req(url)
                    if resposta_html is not None:
                        selenium(url,1)
                        print("caso 1")
                    else:
                        print(f"Não há uma página para tratamento e prevenção do termo: {termo}")
                        i+=1
                elif(i == 1):
                    total = 0
                    for e in range(0,2):
                        if(e == 0):
                            url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/tratamento"
                            resposta_html = req(url)
                            if resposta_html is not None:
                                selenium(url,2)
                                print("caso 2")
                                total = 1
                                e+=1
                        elif(e == 1):
                            url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}/prevencao"
                            resposta_html = req(url)
                            if resposta_html is not None:
                                selenium(url,3)
                                print("caso 3")
                                total += 1
                                e+=1
                        if(total == 2):
                            print("Há uma aba de tratamento e prevenção para o termo:")
                        else:
                            print("Não há tratamento ou prevenção para o termo")
                            i+=1
                elif(i==2):
                    print("AQUII")
                    url = f"https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/{letra}/{termo}"
                    resposta_html = req(url)
                    if resposta_html is not None:
                        print("caso 4")
                        selenium(url,4)
                    else:
                        print(f"Não há uma página para tratamento e prevenção do termo: {termo}")
        except Exception as e:
            print(e)