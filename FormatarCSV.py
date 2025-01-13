import csv
import re

with open('dados.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # Especifique o delimitador correto
    data = [row for row in reader]

# Processa cada linha
for row in data:
    # Pegue o conteúdo da segunda coluna (chamada de Paragrafo)
    paragraph = row['Paragrafo']
    
    # Formate os textos para que, ao encontrar locais com vários "espaços" juntos, transforme esses espaços em apenas um
    paragraph = re.sub(' +', ' ', paragraph)
    
    # Exclua o texto à direita do segundo ponto final encontrado em cada parágrafo
    sentences = paragraph.split('.')
    if len(sentences) > 2:
        paragraph = '.'.join(sentences[:2]) + '.'
    
    # Atualiza o parágrafo na linha
    row['Paragrafo'] = paragraph

# Salve os novos textos em um outro arquivo CSV
with open('dados_formatados.csv', 'w', newline='', encoding='utf-8') as csvfile:
    all_keys = set()

    # Itere sobre todos os dicionários em data e adicione suas chaves ao conjunto
    for row in data:
        all_keys.update(row.keys())

    # Converta o conjunto para uma lista para obter os fieldnames
    fieldnames = list(all_keys)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')  # Especifique o delimitador correto
    
    writer.writeheader()
    writer.writerows(data)
    
with open('dados_formatados.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    formatted_data = [row for row in reader]
