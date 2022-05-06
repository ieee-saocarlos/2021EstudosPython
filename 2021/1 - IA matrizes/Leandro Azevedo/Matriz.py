# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 21:11:19 2021

@author: leand
"""

import numpy as np
import seaborn as sns
base = np.zeros((20,20))
matriz = np.copy(base)
matrizprov = np.copy(base)    #cria a matriz e a provisória
contador = 0
teste = 10000000000000000000000000000000000000   #cria o numero inicial de teste, numero grande pra krl pra n dar problema de terminar com 1 tentativa só

def arrumação(matriz):
    matriz[0,:] = -50
    matriz[:,0]= -50
    matriz[-1,:]=30
    matriz[:,-1]=30  # aqui eu arrumo o formato da matriz
    matriz[0,-1]=0
    matriz[-1,0]=0
    return matriz
    

 #abaixo sao as tentativas de fazer a média dos numeros

while True:
    contador += 1
    tamanho = len(matriz[0])  #coisinhas basicas pra funcionar, como um contador e a arrumaçao da matriz
    arrumação(matriz)
    
    coluna = 1
    while coluna< tamanho:
        linha = 1
        while linha < tamanho-1:
#           caso em que o elemento está na borda inferior esquerda
            if linha+1==tamanho and coluna+1==tamanho:               
                matrizprov[linha,coluna] = ((matriz[linha-1, coluna]+matriz[linha,coluna-1])/2)
            elif linha+1!=tamanho and coluna+1==tamanho:
#                caso em que o elemento está na borda direita (acho)
                matrizprov[linha,coluna] = ((matriz[linha-1, coluna]+matriz[linha,coluna-1]+matriz[linha+1, coluna])/3)
            elif linha+1==tamanho and coluna+1!=tamanho:
#                caso que o elemento está na borda de baixo (acho)
                matrizprov[linha,coluna] = ((matriz[linha-1, coluna]+matriz[linha,coluna-1]+matriz[linha, coluna+1])/3)
            elif linha+1!=tamanho and coluna+1!=tamanho :
#                caso em que o elemento tem 4 vizinhos normalmente
                matrizprov[linha,coluna] = ((matriz[linha-1, coluna]+matriz[linha,coluna-1]+matriz[linha+1, coluna]+matriz[linha, coluna+1])/4)
            linha += 1
        coluna += 1
        
    matrizprov = arrumação(matrizprov) #arrumo dnv o formato da matriz
    testenovo = np.allclose(matrizprov, matriz, rtol = 1e-04)
    if testenovo == True:
        matriz = np.copy(matrizprov)   #testo se a matriz ta mt parecida, e, se estiver, encerro o programa
        print(matriz)
        print("O programa rodou %s vezes" %contador) #contador pra ter ideia do quao ineficiente ta
        break
    teste = testenovo
    matriz = np.copy(matrizprov) #caso a matriz n esteja igual, o programa continua com a nova matriz
    

sns.heatmap(matrizprov, cmap = "coolwarm"); #formação do heatmap