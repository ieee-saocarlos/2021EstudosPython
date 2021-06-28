#!/usr/bin/env python3
#Copyright (C) 2021 Lucas Eduardo Gulka Pulcinelli
#LICENSE: 2-clause BSD

#programa que lê um arquivo CSV contendo compras com uma data Date,
#uma descrição itemDescription e um preço price em USD,
#transformando as duas ultimas informações na lingua e moeda provida pela linha de comando
#os preços serão transformados conforme o indice de conversão da data do item

#módulos necessários: forex_python, deep_translator e pandas

#FIXME: forex_python manda cada request pela internet,
#logo traduzir e converter 14521 rows demoraria um tempo absurdo
#(isso se não bloquearem seu IP)

#eu testei alguns módulos para baixar os índices de conversão de determinado período
#mas não consegui pela falta de documentação (testei o módulo pandasdmx)
#aparentemente tem o módulo yfinance, mas não sei se serve e já estou feliz com o que consegui

import sys
import locale
import datetime
import time
import pandas as pd
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


#colocando o preço de cada item na moeda correta
if curr_symbol != "USD":
    start_time = time.time()
    for i, price in enumerate(df["price"]):
        if i > 5:
            break #protege seu ip
    
        #pega a data do item
        date_item = df.at[i, "Date"].split("-")
        date_item = [int(dmy) for dmy in date_item]
        date_obj = datetime.datetime(date_item[2], date_item[1], date_item[0])
        weekday = date_obj.weekday()
        if weekday >= 5: #o conversor dá erro caso o dia do não seja um dia de semana, então nesse caso pega da sexta anterior
            date_obj = date_obj + datetime.timedelta(days=4-weekday)
        
        #converte e coloca no dataframe
        price = converter.convert("USD", curr_symbol, price, date_obj=date_obj)
        df.at[i, "price"] = "{0:.2f}".format(price)

    print("Convertido! Demora em segundos: {0:.2f}".format(time.time() - start_time))


#salvando o dataframe com as novas informações
df.to_csv("compras_{}.csv".format(language_to))