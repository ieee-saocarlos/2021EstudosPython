#!/usr/bin/env python3
#Copyright (C) 2021 Lucas Eduardo Gulka Pulcinelli
#LICENSE: 2-clause BSD

#programa que lê um arquivo CSV contendo compras com uma data Date,
#uma descrição itemDescription em inglês e um preço price em USD,
#transformando as duas ultimas informações na lingua e moeda provida pela linha de comando
#os preços serão transformados conforme a data média dos itens

#módulos necessários: deep_translator, forex_python, numpy e pandas

import sys
import locale
import datetime
import time
import pandas as pd
import numpy as np
import deep_translator
import forex_python.converter

#inputs
if len(sys.argv) < 3:
    language_to = input("qual lingua você quer traduzir para? (vazio para pt_BR) ")
    file_csv = input("qual o arquivo contendo o CSV? (vazio para ../compras.csv) ")
else:
    language_to = sys.argv[1]
    file_csv = sys.argv[2]

#inicalizando tradutor
if language_to == "":
    language_to = "pt_BR"
if language_to[0:2] == "en": #google translate dá erro caso você tente traduzir de inglês para inglês
    translate = False
else:
    translate = True
    try:
        translator = deep_translator.GoogleTranslator(source="en", target=language_to[0:2])
    except deep_translator.exceptions.LanguageNotSupportedException:
        print("linguagem invalida ou não suportada!", file=sys.stderr)
        sys.exit(-1)

#incializando a conversão de moedas
try:
    locale.setlocale(locale.LC_MONETARY, language_to)
    curr_symbol = locale.localeconv()["int_curr_symbol"][:-1] #por algum motivo tem um espaço no final, então corta ele
    converter = forex_python.converter.CurrencyRates()
except locale.Error:
    print("locale inválido ou não suportado!", file=sys.stderr)
    sys.exit(-1)

#inicializando o dataframe
if file_csv == "":
    file_csv = "../compras.csv"
try:
    df = pd.read_csv(file_csv)
except (IsADirectoryError,FileNotFoundError):
    print("arquivo invalido ou inexistente!", file=sys.stderr)
    sys.exit(-1)




#criando um dicionario com todas as palavras únicas como chaves e traduzidas como valores
lexicon = df["itemDescription"].unique()
lexicon_dict = {}
for word in lexicon:
    lexicon_dict[word]  = translator.translate(word) if translate else word

#traduzindo cada linha
df["itemDescription"] = df.apply(lambda row: lexicon_dict[row["itemDescription"]], axis=1)


#pegando o mês médio dos itens (eu sei que economia não funciona assim, mas não consegui de outra forma)
months = df.apply(
    lambda row: 
    (np.array(row["Date"].split("-")).astype(int) #pega as datas dos itens, separa em dia mes ano
    *[1/30,1,12]).sum(), axis=1) #multiplica tudo para transformar em mês e soma (para o item)
mean_month = months.mean()

#pegando data média dos itens
mean_y,mean_m,mean_d = (int(mean_month/12), int(mean_month)%12, int((mean_month%1)*30))
date_obj = datetime.datetime(mean_y, mean_m, mean_d)

weekday = date_obj.weekday()
if weekday >= 5: #o conversor dá erro caso o dia do não seja um dia de semana, então nesse caso pega da sexta anterior
    date_obj = date_obj + datetime.timedelta(days=4-weekday)

#pegando o valor de conversão na data
convert_value = converter.convert("USD", curr_symbol, 1, date_obj=date_obj)

#aplicando a conversão no dataframe
df["price"] = df.apply(lambda row: "{0:.2f}".format(row["price"] * convert_value), axis=1)


#salvando o dataframe com as novas informações
df.to_csv("compras_{}.csv".format(language_to))
