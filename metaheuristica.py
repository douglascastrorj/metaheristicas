import random 
import copy
from math import e

from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO1, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera

S = 2
T = 46
D = 5

# SAmax: numero maximo de iteracoes Metropolis para cadaTemperatura
# alpha: taxa de resfriamento 0 < alpha < 1
# T0: temperatura inicial
def simulatedAnealing(solucaoInicial, FO, T0=100, SAmax=100, alpha=0.5):
    
    bestSolution =  copy.deepcopy(solucaoInicial)
    solucaoCorrente =  copy.deepcopy(solucaoInicial)
    iterT = 0
    T = T0

    while T > 0.0001:
        while iterT < SAmax:
            iterT = iterT + 1

            #gerar vizinho
            s1 = trocaCirurgiasDiasDiferente({'solucao': solucaoCorrente, 'D': D})
            delta = FO1(s1) - FO1(solucaoCorrente)
            if viavel(s1, S, T, D):
                if delta < 0:
                    solucaoCorrente = s1
                    if FO1(s1) < FO1(bestSolution):
                        bestSolution = s1
                else:
                    x = random.random()
                    if x < e**(-delta/T):
                        solucaoCorrente = s1
        T = T * alpha
        iterT = 0
        # print(T)
    return bestSolution