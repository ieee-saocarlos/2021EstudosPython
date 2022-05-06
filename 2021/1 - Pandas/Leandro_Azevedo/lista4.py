# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 19:17:11 2021

@author: leand
"""

import pandas as pd
import random
from unidecode import unidecode

import sys, os 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def isnumber(value):
    try:
         float(value)
    except ValueError:
         return False
    return True

resource_path('palavrascod.xlsx')
prov = []
df = pd.read_excel("palavrascod.xlsx", sheet_name="Sheet1")
palavra = 0
def tamanho(palavra) :
    global prov
    palavra = unidecode(input("Digite 'n' caso já queira criar a frase\nfale o tamanho da palavra: "))
    if isnumber(palavra) == True:
        print("fale o numero por extenso, por favor")
        tamanho(palavra)
    if palavra == "n" :
        fim()
    if palavra == "fim":
        print("finalizaremos, obrigado pela preferencia")
    if palavra != 'n' and palavra != 'fim' :
        global pre
        pre = []
        pre.append(palavra)
        pre.append((input("art: artigo // pron: pronome // ver:verbo // sub: substantivo\nadj: adjetivo // misc: outros\nfale a classe gramatical da palavra: ").rstrip()))
        prov = prov + [pre]
        tamanho(palavra)

def fim():
    global prov
    frase = []
    for func in prov :
        filter1_df = df.loc[df['tam'] == func[0]]
        sla = filter1_df.loc[df['gram'] == func[1]]
        fim = list(sla['palavra'])
        frase.append(random.choice(fim))
        frase.append(" ")
    print('-------------------------------------------------\n', ''.join(frase), '\n-------------------------------------------------')
    tamanho(palavra)
    
tamanho(palavra)