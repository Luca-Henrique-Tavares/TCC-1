import csv

def extrair_primeira_palavra():
    palavras = []
    with open('dados.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader, None)  # skip the headers
        for row in reader:
            if row and row[0]:  # check if the row and the first column are not empty
                palavras_split = row[0].split()
                if palavras_split:  # check if the split string is not empty
                    primeira_palavra = palavras_split[0]  # split the string into words and take the first one
                    palavras.append(primeira_palavra)

    with open('palavras_achadas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for palavra in palavras:
            writer.writerow([palavra])
            
def filtrar_palavras_unicas():
    palavras_unicas = set()
    with open('palavras_achadas.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0]:  # check if the row and the first column are not empty
                palavras_unicas.add(row[0])

    with open('palavras_unicas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for palavra in palavras_unicas:
            writer.writerow([palavra])

if __name__ == "__main__":
    filtrar_palavras_unicas()