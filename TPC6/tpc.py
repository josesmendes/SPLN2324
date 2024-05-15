import spacy
import sys
from collections import Counter

nlp = spacy.load("pt_core_news_lg")

with open(sys.argv[1], encoding="utf-8") as file:
    text = file.read()

doc = nlp(text)

pares_counter = Counter()

for sentence in doc.sents:
    nomes = []
    for token in sentence:
        if token.pos_=="PROPN":
            nomes.append(token.text)
    if len(nomes)>2:            
        if (f"{nomes[1]}_{nomes[0]}" in pares_counter):
            par = f"{nomes[1]}_{nomes[0]}"
        else:
            par = f"{nomes[0]}_{nomes[1]}"
        pares_counter.update({par : 1})

pares_mais_comuns = pares_counter.most_common(10)  # Altere 10 para o número desejado de pares mais comuns

# Imprima os pares de nomes mais comuns
print("Pares de nomes mais comuns:")
for par, frequencia in pares_mais_comuns:
    print(par, "-", frequencia)
