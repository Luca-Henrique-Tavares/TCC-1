from sqlalchemy import create_engine,text
import pandas as pd
from deep_translator import GoogleTranslator
from PyDictionary import PyDictionary
import csv
import datetime as dat

'''
#Função que trará significação da base de dados do Medline Plus:
def medline():
    try:
        create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
    except Exception as e:
        print(e)
    try:
        df = pd.read_sql_table('dici_teste', con=connection())
        tamanho = len(df)
        titulo = []
        id = []
        for i in range(0,tamanho):
            titulo.append(df['title'].iloc[i])
            id.append(df['id_true'].iloc[i])
    except Exception as e:
        print(e)
    print(titulo)
    print(id)

#Função que trará significação da base de dados do SUS:
def sus():
    try:
        create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
    except Exception as e:
        print(e)
    try:
        df = pd.read_sql_table('sus2', con=connection())
        tamanho = len(df)
        titulo = []
        id = []
        for i in range(0,tamanho):
            titulo.append(df['titulo'].iloc[i])
            id.append(df['id'].iloc[i])
    except Exception as e:
        print(e)
    print(titulo)
    print(id)
'''

#Função que traduz os termos escolhidos e traduz, além de recolher seus significados. Além disso, cria um dicionário e os adciona em um arquivo .csv
def transforma():
    palavras = ["Abdômen", "Açúcar", "Amígdala", "Alvéolo", "Antebraço", "Apêndice", "Aponeurose", "Aracnoide", "Artérias", "Coronárias", "Suprarrenal", "Arteríolas", "Articulações", "Aurículas", "Axilas", "Baço", "Barba", "Barriga", "Bexiga", "Bícepes", "Bigode", "Bile", "Boca", "Bochechas", "Braços", "Brônquios", "Bronquíolos", "Bulbo", "Cabelo", "Cabeça",  "Capilares", "Cárdia", "Ceco", "Célula", "Cerebelo", "Cérebro", "Cérvix", "Cílios", "Cintura", "Clítoris", "Cóclea", "Cólon", "Coração", "Córnea", "Córtex", "Costas", "Cotovelo", "Coxa", "Dedos", "Dentes", "Caninos", "Incisivos", "Molares", "Derme", "Dorsal", "Ducto", "Duodeno", "Embrião", "Endocárdio", "Endométrio", "Esfíncter", "Esclera", "Espermatozóide", "Esqueleto", "Esterno", "Estômago", "Esófago", "Epiderme", "Epidídimo", "Epiglote", "Falanges", "Metacarpo", "Carpo", "Face", "Faringe", "Fêmures", "Fígado", "Fóvea", "Fur", "Garganta", "Gengivas", "Glabela", "Glande", "Glote", "Glândulas", "Gordura", "Hemoglobina", "Hímen", "Hipocampo", "Hipoderme", "Hipófise", "Hipotálamo","Íleo", "Infecção","Intestino", "Íris", "Jejuno", "Joelho", "Lábios", "Laringe", "Laringofaringe", "Leucócitos", "Ligamentos", "Lipoma", "Mamas ", "Mamilos", "Mandíbula", "Maxilar", "Mãos", "Medula", "Meninge", "Membrana","Mesentério", "Vilosidades", "Miocárdio", "Músculos", "Nádegas", "Narinas", "Nariz", "Nasofaringe", "Nefrónio", "Nervos","Nuca", "Olhos", "Ombros", "Orelhas", "Orofaringe", "Ossos", "Óvulo", "Palato", "Pálpebras", "Pâncreas", "Panturrilha", "Peito", "Pele", "Pênis", "Pericárdio", "Períneo", "Periósteo", "Pernas", "Pés", "Pestanas", "Piloro", "Pituitária", "Placentas", "Pleura", "Prepúcio", "Próstata", "Pulmões", "Pulso", "Pupilas", "Quadril", "Retinas", "Rins", "Rosto", "Sangue", "Seio", "Sêmem", "Septo", "Sacro", "Shin", "Sinus", "Sobrancelhas", "Tálamo", "Tecidos",  "Tendões", "Testa", "Testículos", "Tímpano", "Tiróide", "Tíbia", "Tonsila", "Tórax", "Tornozelo", "Torso", "Traqueia", "Tríceps", "Tumor", "Úmero", "Unhas", "Uretra", "Ureteres", "Útero", "Úvea", "Úvula", "Vagina", "Válvulas", "Veias", "Ventrículos", "Vénulas", "Vértebras", "Virilha", "Vírus", "Vesícula", "Vulva"]
    print(len(palavras))
    tradutor_en = GoogleTranslator(source="pt",target="en")
    dictionary = PyDictionary()
    dicionario = {}
    for palavra in palavras:
        try:
            word = tradutor_en.translate(palavra)
            termo = word
            termos = termo.split()#Separa a frase caso tenha mais de uma palavra
            num_termos = len(termos)
            if num_termos == 1:
                #print(palavra)
                meaning = dictionary.meaning(word) # significado recebe conexão com dicionário e o significado da palavra
                #print(meaning)
                if meaning is not None: # Caso não haja signficação para a palavra não deverá ir para o dicionário, caso haja irá nesse if 
                    dicionario[palavra] = meaning
                    #print(dicionario)
                else:
                    print("Palavra sem significado",palavra)#OBS: você deve retirar as palavras que não tem significado, caso contrário haverá erro no código:Error: The Following Error occured: list index out of range 
            else:
                print("Erro no termo ",palavra)
        except Exception as e:
            print(e)
            print(palavra)
    #dicionario = tradutor_pt.translate(dicionario)
    # Abra um novo arquivo CSV para escrita
    with open('dicionario.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Escreva o cabeçalho
        writer.writerow(['titulo', 'texto'])
        # Escreva os dados
        for key, value in dicionario.items():
            writer.writerow([key, value])

def pandas():
    # Criação de dataframes do pandas
    df=pd.read_csv('dicionario.csv')
    # Colocaremos no daraframe outras colunas com termos constantes
    data = dat.datetime.now()
    dia = data.day
    mes = data.month
    ano = data.year

    data_str = f'Acesso em: {dia}/{mes}/{ano}'# F string na qual a data é formada a partir de outras strings
    url = "https://pypi.org/project/Py-Dictionary/"
    fonte = "Py-Dictionary com a utilização da base de dadoos do WordNet"

    df['data'] = data_str
    df['url'] = url
    df['fonte'] = fonte
    inserir(df)

# Criação de conexão com o banco de dados MySQL

def connection():
    try:
        engine = create_engine('mysql+pymysql://root:123456@localhost/teste_tcc')
        return engine
    except Exception as e:
        print(e)

# Inserção do DataFrame no banco de dados
def inserir(df):
    try:
        df.to_sql('anatomia', con=connection(), if_exists='replace', index=False)
    except Exception as e:
        print(e)

#Acessa a tabela mysql e traduz os termos em inglês para português
def ler_tabela():
    global c
    print(c)
    tradutor_pt=GoogleTranslator(source="en", target="pt")
    try:
       
            df=pd.read_sql_table('anatomia', con=connection())
            texto = df['texto'].iloc[c]
            print(f"Texto original: {texto}")  # Imprime o texto original
            texto_traduzido = tradutor_pt.translate(texto)
            print(f"Texto traduzido: {texto_traduzido}")  # Imprime o texto traduzido
            print(f"titulo: {df['titulo'].iloc[c]}")  # Imprime o titulo
            df.loc[c, 'texto'] = texto_traduzido #Atualiza na linha C o termo traduzido. Não é possível fazer isto com o termo id, pois, pelo visto o indice da coluna não corresponde necessariamente ao id. Exemplo: ID = 1 e indice = 0, que seria o correto não acontece
            df.to_sql('anatomia', con=connection(), if_exists='replace', index=False)
    except Exception as e:
        print(e)    


if __name__ == '__main__':
    transforma()
    pandas()
    c = 0
    while c < 200:
        ler_tabela()
        c += 1

'''
ALTER TABLE `teste_tcc`.`anatomia` 
ADD COLUMN `id_true` INT NOT NULL AUTO_INCREMENT AFTER `fonte`,
ADD PRIMARY KEY (`id_true`);
;
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'(anatomia\', \'especialmente se permitir movimento\',  \'a forma ou maneira pela qual as coisas se juntam e uma conexão é feita\']}' WHERE (`titulo` = 'Articulações');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'qualquer um dos membros terminais da mão (às vezes exceto o polegar\']}'WHERE (`titulo` = 'Dedos');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'o tipo, número e disposição dos dentes (coletivamente\', \'estruturas duras semelhantes a ossos nas mandíbulas dos vertebrados; usadas para morder e mastigar ou para ataque e defesa\']}' WHERE (`titulo` = 'Dentes');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'uma substância gordurosa macia que ocorre no tecido orgânico e consiste em uma mistura de lipídios (principalmente triglicerídeos\', \'um tipo de tecido corporal contendo gordura armazenada que serve como fonte de energia; também amortece e isola vital órgãos\', \'excesso de peso corporal\']}' WHERE (`titulo` = 'Gordura');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\"parte inferior ou posterior do cérebro; contínuo com a medula espinhal; (\'bulbo\' é um termo antigo para medula oblonga\"]}'WHERE (`titulo` = 'Bulbo');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'uma cobertura para o corpo (ou partes dele\', \'como na cabeça humana\', \'uma distância ou espaço muito pequeno\', \'qualquer um dos cilíndricos filamentos que crescem caracteristicamente na epiderme de um mamífero\', \'uma projeção ou processo filamentoso em um organismo\']}}' WHERE (`titulo` = 'Cabelo');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a parte superior do corpo humano ou a parte frontal do corpo em animais; contém o rosto e o cérebro\', \'aquilo que é responsável pelos pensamentos, sentimentos e funções cerebrais conscientes; a sede da faculdade da razão\']}' WHERE (`titulo` = 'Cabeça');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a abertura no estômago e aquela parte do estômago conectada ao esôfago\']}' WHERE (`titulo` = 'Cárdia');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'qualquer compartimento pequeno\', \'(biologia\', \'como em mônadas\', \'um dispositivo que fornece uma corrente elétrica como resultado de uma reação química\']}'WHERE (`titulo` = 'Célula');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'aquela parte do sistema nervoso central que inclui todos os centros nervosos superiores; encerrado dentro do crânio; contínuo com a medula espinhal\']}' WHERE (`titulo` = 'Cérebro');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'a parte do intestino grosso entre o ceco e o reto; extrai a umidade dos resíduos alimentares antes de serem excretados\']}' WHERE (`titulo` = 'Cólon');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a estrutura dura (ossos e cartilagens)\',]}' WHERE (`titulo` = 'Esqueleto');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'o estado patológico resultante da invasão do corpo por microrganismos patogênicos\', \'(fonética\', \'(medicina\', \'um incidente no qual uma doença infecciosa é transmitida\']}' WHERE (`titulo` = 'Infecção');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'um órgão aumentado e musculoso em forma de saco do canal alimentar; o principal órgão da digestão\', \'a região do corpo de um vertebrado entre o tórax e a pelve\']}' WHERE (`titulo` = 'Estômago');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [ \'diafragma muscular que controla o tamanho da pupila que por sua vez controla a quantidade de luz que entra no olho; forma a porção colorida do olho\']}' WHERE (`titulo` = 'Íris');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'articulação articulada na perna humana conectando a tíbia e a fíbula ao fêmur e protegida na frente pela patela\', \'articulação entre o fêmur e a tíbia em um quadrúpede; corresponde ao joelho humano\']}' WHERE (`titulo` = 'Joelho');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'qualquer um dos ossos dos dedos das mãos ou dos pés\']}'WHERE (`titulo` = 'Falange');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'qualquer uma das duas dobras carnudas de tecido que circundam a boca e desempenham um papel na fala\'}}'WHERE (`titulo` = 'Lábios');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a pequena projeção de uma glândula mamária\']}' WHERE (`titulo` = 'Mamilos');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'órgão glandular marrom-avermelhado grande e complicado localizado na porção superior direita da cavidade abdominal; secreta bile e atua no metabolismo de proteínas, carboidratos e gorduras; sintetiza substâncias envolvidas na coagulação do sangue; sintetiza vitamina A; desintoxica substâncias venenosas e decompõe eritrócitos desgastados\', \'fígado de animal usado como carne\']}' WHERE (`titulo` = 'Fígado');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a parte do crânio de um vertebrado que emoldura a boca e segura os dentes\', \'os ossos do crânio que emolduram a boca e servem para abri-la; os ossos que seguram os dentes\']}' WHERE (`titulo` = 'Maxilar');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'o (preênsil\', \'um trabalhador contratado em uma fazenda ou rancho\', \'algo escrito à mão\', \'habilidade\']}' WHERE (`titulo` = 'Mãos');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'a rede gordurosa de tecido conjuntivo que preenche as cavidades dos ossos\', \'tecido muito macio e muito nutritivo de medula óssea\']}' WHERE (`titulo` = 'Medula');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'um dos órgãos contráteis do corpo\', \'tecido animal consistindo predominantemente de células contráteis\']}' WHERE (`titulo` = 'Músculos');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'o órgão do olfato e entrada do trato respiratório; a parte proeminente da face do homem ou de outros mamíferos\']}' WHERE (`titulo` = 'Nariz');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'a frequência com que o coração bate; geralmente medida para obter uma avaliação rápida da saúde de uma pessoa\", \'Verbo\': [\'expandir e contrair ritmicamente; bater ritmicamente\', \'produzir ou modular (como ondas eletromagnéticas\', \'passar por ou como se fosse por pulsação\']}' WHERE (`titulo` = 'Pulso');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'qualquer feixe de fibras nervosas que corre para vários órgãos e tecidos do corpo\']}' WHERE (`titulo` = 'Nervos');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a abertura contrátil no centro da íris do olho; assemelha-se a um grande ponto preto\']}' WHERE (`titulo` = 'Pupila');
UPDATE teste_tcc.anatomia SET texto = 'Olhos: {\'Substantivo\': [\'o órgão da visão\']}' WHERE (`titulo` = 'Olhos');
UPDATE teste_tcc.anatomia SET texto = 'Queixo: {\'Substantivo\': [\'a parte saliente da mandíbula inferior\']}'WHERE (`titulo` = 'Queixo');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a parte do corpo entre o pescoço e a parte superior do braço\',\'uma articulação esférica entre a cabeça do úmero e uma cavidade da escápula\']}' WHERE (`titulo` = 'Ombros');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'o órgão dos sentidos para a audição e o equilíbrio\']}' WHERE (`titulo` = 'Orelha');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a frente da cabeça humana, da testa ao queixo e de orelha a orelha\']}' WHERE (`titulo` = 'Rosto');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'o fluido (vermelho em vertebrados\']}' WHERE (`titulo` = 'Sangue');
UPDATE teste_tcc.anatomia SET texto = ' {\'Substantivo\': [\'tecido conjuntivo rígido que constitui o esqueleto dos vertebrados\', \'a substância calcificada porosa da qual os ossos são feitos\']}' WHERE (`titulo` = 'Ossos');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a frente do tronco, do pescoço ao abdômen\', \'qualquer um dos dois órgãos glandulares carnudos e macios secretores de leite no peito de uma mulher\', \'carne esculpida no peito de uma ave\', \"a parte do corpo de um animal que corresponde ao peito de uma pessoa\"]}' WHERE (`titulo` = 'Seio');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'\'a parte muscular posterior da perna\']}' WHERE (`titulo` = 'Panturrilha');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a parte do torso humano entre o pescoço e o diafragma ou a parte correspondente em outros vertebrados\', \'a frente do tronco do pescoço ao abdômen\']}' WHERE (`titulo` = 'Tórax');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'um membro humano; comumente usado para se referir a um membro inteiro, mas tecnicamente apenas à parte do membro entre o joelho e o tornozelo\"]}' WHERE (`titulo` = 'Pernas');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'a parte da perna de um ser humano abaixo da articulação do tornozelo\', \'qualquer um dos vários órgãos de locomoção ou fixação em invertebrados\']}' WHERE (`titulo` = 'Pé');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'placa córnea cobrindo e protegendo parte da superfície dorsal dos dedos\']}' WHERE (`titulo` = 'Unhas');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'uma estrutura em um órgão oco (como o coração\', \'controle que consiste em um dispositivo mecânico para controlar o fluxo de um fluido\']}' WHERE (`titulo` = 'Válvulas');
UPDATE teste_tcc.anatomia SET texto = '{\'Substantivo\': [\'um vaso sanguíneo que transporta sangue dos capilares em direção ao coração\', \'um estilo ou maneira distinta\', \'qualquer um dos feixes vasculares ou costelas que formam a estrutura ramificada dos tecidos condutores e de suporte em uma folha ou outro órgão vegetal\']}' WHERE (`titulo` = 'Veias');
UPDATE `teste_tcc`.`anatomia` SET `titulo` = 'Canela' WHERE (`titulo` = 'Shin');
UPDATE `teste_tcc`.`anatomia` SET `titulo` = 'Pelo' WHERE (`titulo` = 'Fur');
 '''