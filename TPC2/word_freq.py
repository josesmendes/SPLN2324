#!/usr/bin/env python3
'''
NAME
   wordfreq - calcula frequencia de palavras num texto

SYNOPSIS
   word_freq [options] input_files
    options: 
    -m 20 : Mostra apenas as 1ª 20 palavras
    -n : ordena alfabeticamente
    -p : remove diferenças de cases nas palavras
    -f : mostrar comparacao de frequencias de palavras
    -l : selecionar lingua de referencia; en: ingles, pt: portugues(por default é pt)
    -c file1 file2: comparar entre 2 ficheiros as palavras mais usadas num e no outro lado

FILES:
    https://www.linguateca.pt/
Description'''

from collections import Counter
from jjcli import * 
import re

__version__ = "0.0.3"


def imprime_lista(lista):
    for palavra, n_occur in lista:
        print(f"{n_occur}   {palavra}")

def imprime_freq(lista):
    for keys in lista:
        print(f"{keys} ::  {lista[keys]}")

def tokenizer(texto):
    tokens = re.findall(r'\w+(?:-\w+)?|[.:!?;,—]+', texto)
    return tokens

def regulize(ocurrencias):
    fixed_ocurrencias = {}
    for palavra in ocurrencias.keys():
        fstchar = palavra[0] 
        if fstchar.islower():
            copia = fstchar.upper() + palavra[1:]
            if ocurrencias[palavra] < ocurrencias[copia]:
                fixed_ocurrencias[copia] = ocurrencias[copia] + ocurrencias[palavra]
            else:
                fixed_ocurrencias[palavra] = ocurrencias[copia] + ocurrencias[palavra]
        else:
            copia = fstchar.lower() + palavra[1:]
            if ocurrencias[palavra] < ocurrencias[copia]:
               fixed_ocurrencias[copia] = ocurrencias[copia] + ocurrencias[palavra]
            else:
                fixed_ocurrencias[palavra] = ocurrencias[copia] + ocurrencias[palavra]
    return fixed_ocurrencias

def database_comparison(content):
    db_dict = dict()
    counter = 0
    cd = dict()

    with open('tests/bd.txt', 'r', encoding='iso-8859-1') as database_file:
        for line in database_file:
            split = re.split(r'[\s\t]+', line, maxsplit=1)
            db_dict[split[1][:-1]] = int(split[0])
            counter += int(split[0])
    
    occ_sum = sum(occ for _, occ in content)
    
    for key, value in content:
        if key in db_dict:
            ratio = (value/occ_sum) / (db_dict[key]/counter)
        else:
            ratio = (value/occ_sum) / (1/counter)
        cd[key] = round(ratio, 4)

    return cd



def main():
    cl=clfilter("nm:pf",doc=__doc__)     ## option values in cl.opt dictionary
    for txt in cl.text():     ## process one file at the time
        lista_palavras = tokenizer(txt)
        ocurrencias = Counter(lista_palavras)
        if "-p" in cl.opt:
            new_ocurrencias = regulize(ocurrencias)
            ocurrencias = Counter(new_ocurrencias)
            #imprime_lista(new_ocurrencias.items())
        if "-m" in cl.opt:
            imprime_lista(ocurrencias.most_common(int(cl.opt.get("-m"))))
        elif "-n" in cl.opt:
            lista_palavras.sort()
            ocurrencias = Counter(lista_palavras)
            imprime_lista(ocurrencias.items())
        if "-f" in cl.opt:
            cd = database_comparison(ocurrencias.items())
            imprime_freq(cd)
        else:
            ocurrencias = Counter(lista_palavras)
            imprime_lista(ocurrencias.items())

