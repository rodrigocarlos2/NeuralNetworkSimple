
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# XOR Multilayer Perceptron usando BackPropagation
# 
# Rodrigo Leal
# Baseado no algoritmo de Neil Schemenauer

import math
import random
import numpy
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as pyplot

random.seed(0)

# corrigir o erro = TERM environment variable not set.
# os.environ["TERM"] = 'xterm'

# gera numeros aleatorios obedecendo a regra:  a <= rand < b
def criar_linha():
    print "-"*80

def rand(a, b):
    return (b-a) * random.random() + a

# nossa funcao sigmoide - gera graficos em forma de S
# funcao tangente hiperbolica
def funcao_ativacao_tang_hip(x):
    return math.tanh(x)

# derivada da tangente hiperbolica
def derivada_funcao_ativacao(x): 
    t = funcao_ativacao_tang_hip(x)
    return 1 - t**2

def funcao_ativacao_log(x):
    return 1 / ( 1 + math.exp(-x))

def derivada_funcao_ativacao_log(x):
    return log(x) * (1 - log(x))

# Logistic function with output in [-1, 1].
def funcao_ativacao_log2(x):
    return 1 - 2 * log(x)

def derivada_funcao_ativacao_log2(x):
    return -2 * log(x) * (1 - log(x))

class RedeNeural:
    def __init__(self, nos_entrada, nos_ocultos, nos_saida):
        # camada de entrada
        self.nos_entrada = nos_entrada + 1 # +1 por causa do no do bias
        # camada oculta
        self.nos_ocultos = nos_ocultos
        # camada de saida
        self.nos_saida = nos_saida
        # quantidade maxima de interacoes
        self.max_interacoes = 1000
        # taxa de aprendizado
        self.taxa_aprendizado = 0.35
        # momentum Normalmente eh ajustada entre 0.5 e 0.9
        self.momentum = 0.25

        # activations for nodes 
        # cria uma matriz, preenchida com uns, de uma linha pela quantidade de nos
        self.ativacao_entrada = numpy.ones(self.nos_entrada)
        self.ativacao_ocultos = numpy.ones(self.nos_ocultos)
        self.ativacao_saida = numpy.ones(self.nos_saida)
        
        self.resultados_ativacao_saida = numpy.ones(self.nos_saida)
 
        # criar a matriz de pesos, preenchidas com zeros
        self.wi = numpy.zeros((self.nos_entrada, self.nos_ocultos))
        self.wo = numpy.zeros((self.nos_ocultos, self.nos_saida))
		
        # adicionar os valores dos pesos
        # vetor de pesos da camada de entrada - intermediaria
        for i in range(self.nos_entrada):
            for j in range(self.nos_ocultos):
                self.wi[i][j] = rand(-0.2, 0.2)

        # vetor de pesos da camada intermediaria - saida
        for j in range(self.nos_ocultos):
            for k in range(self.nos_saida):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum   
        self.ci = numpy.zeros((self.nos_entrada, self.nos_ocultos))
        self.co = numpy.zeros((self.nos_ocultos, self.nos_saida))

    def fase_forward(self, entradas):
        # input activations: -1 por causa do bias
        for i in range(self.nos_entrada - 1):           
            self.ativacao_entrada[i] = entradas[i]

        # calcula as ativacoes dos neuronios da camada escondida
        for j in range(self.nos_ocultos):
            soma = 0
            for i in range(self.nos_entrada):
                soma = soma + self.ativacao_entrada[i] * self.wi[i][j]
            self.ativacao_ocultos[j] = funcao_ativacao_tang_hip(soma)

        # calcula as ativacoes dos neuronios da camada de saida
        # Note que as saidas dos neuronios da camada oculta fazem o papel de entrada 
        # para os neuronios da camada de saida.
        for j in range(self.nos_saida):
            soma = 0
            for i in range(self.nos_ocultos):
                soma = soma + self.ativacao_ocultos[i] * self.wo[i][j]
            self.ativacao_saida[j] = funcao_ativacao_tang_hip(soma)
            
        return self.ativacao_saida    


    def fase_backward(self, saidas_desejadas):
        # calcular os gradientes locais dos neuronios da camada de saida
        output_deltas = numpy.zeros(self.nos_saida)
        erro = 0
        for i in range(self.nos_saida):
            erro = saidas_desejadas[i] - self.ativacao_saida[i]
            output_deltas[i] = derivada_funcao_ativacao(self.ativacao_saida[i]) * erro

        # calcular os gradientes locais dos neuronios da camada escondida
        hidden_deltas = numpy.zeros(self.nos_ocultos)
        for i in range(self.nos_ocultos):
            erro = 0
            for j in range(self.nos_saida):
                erro = erro + output_deltas[j] * self.wo[i][j]
            hidden_deltas[i] = derivada_funcao_ativacao(self.ativacao_ocultos[i]) * erro

        # a partir da ultima camada ate a camada de entrada
        # os nos da camada atual ajustam seus pesos de forma a reduzir seus erros
        for i in range(self.nos_ocultos):
            for j in range(self.nos_saida):
                change = output_deltas[j] * self.ativacao_ocultos[i]
                self.wo[i][j] = self.wo[i][j] + (self.taxa_aprendizado * change) + (self.momentum * self.co[i][j])
                self.co[i][j] = change

        # atualizar os pesos da primeira camada
        for i in range(self.nos_entrada):
            for j in range(self.nos_ocultos):
                change = hidden_deltas[j] * self.ativacao_entrada[i]
                self.wi[i][j] = self.wi[i][j] + (self.taxa_aprendizado * change) + (self.momentum * self.ci[i][j])
                self.ci[i][j] = change

        # calcula erro
        erro = 0
        for i in range(len(saidas_desejadas)):
            erro = erro + 0.5 * (saidas_desejadas[i] - self.ativacao_saida[i]) ** 2
        return erro

    def test(self, entradas_saidas):

        acertos = 0

        for p in entradas_saidas:
            array = self.fase_forward(p[0])
            print("Entradas: " + str(p[0]) + ' - Saida encontrada/fase forward: ' + str(array[0]))

            temp1 = array[0]*100

            if(temp1>85 and p[1] == [1]):
                acertos = acertos+1

            if(temp1<=85 and p[1] == [0]):
                acertos = acertos+1

        acuracia = (acertos/4) * 100

        print "Acuracia = %d POR CENTO"%acuracia

        objects = ('Acertos', 'Erros')
        y_pos = np.arange(len(objects))
        performance = [100,0]
         
        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Acuracia em %')
        plt.title('Acuracia da Rede Neural na Classificacao de Ataques DDoS')
         
        plt.show()
        

    def treinar(self, entradas_saidas):

        a = [5,3,4,2,7,5,4,6,3,2]

        i2 = 0

        for i in range(self.max_interacoes):
            erro = 0
            for p in entradas_saidas:
                entradas = p[0]
                saidas_desejadas = p[1]
                self.fase_forward(entradas)
                erro = erro + self.fase_backward(saidas_desejadas)
            if i % 100 == 0:
                print "Erro = %2.3f"%erro
                a[i2] = float("{0:.3f}".format(erro))
                i2 = i2+1

        x = numpy.arange(10)

        y = numpy.array(a)

        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim(0,1)
        pyplot.plot(x,y)
        for i,j in zip(x,y):
            ax.annotate(str(j),xy=(i,j))

        pyplot.show()


def iniciar():

    entradas_saidas = [
        [[1],   [1]], # 100 MBits = 1 Attack
        [[0.9], [1]], # 90 MBits = 1 Attack
        [[0.2], [0]], # 20 MBits = 0 Not Attack
        [[0.3], [0]]  # 30 Mbits = 0 Not Attack
    ]
	
    # cria rede neural com duas entradas, duas ocultas e um no de saida    
    n = RedeNeural(1, 4, 1)
    criar_linha()
    n.treinar(entradas_saidas)
    # testar
    criar_linha()
    n.test(entradas_saidas)

if __name__ == '__main__':
    iniciar()
