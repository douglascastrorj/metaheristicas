import random 
import copy
from math import e

from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
import buscaLocal
# from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, trocaCirurgiaMarcadaPorCirurgiaListaEspera, removeCirurgias

S = 2
T = 46
D = 5

# SAmax: numero maximo de iteracoes Metropolis para cadaTemperatura
# alpha: taxa de resfriamento 0 < alpha < 1
# T0: temperatura inicial
def simulatedAnealing(solucaoInicial, FO, T0=100, SAmax=100, alpha=0.5, _history = False):
    
    #armazena as atualizacoes de best
    _history = []
    
    bestSolution =  copy.deepcopy(solucaoInicial)
    solucaoCorrente =  copy.deepcopy(solucaoInicial)
    iterT = 0
    T = T0

    while T > 0.0001:
        while iterT < SAmax:
            iterT = iterT + 1

            #gerar vizinho
            s1 = buscarVizinho(solucaoCorrente, T, T0, iterT, SAmax)
            delta = FO2(s1) - FO2(solucaoCorrente)
            if viavel(s1, S, 45, D) == True:
                if delta < 0:
                    solucaoCorrente = s1
                    if FO2(s1) < FO2(bestSolution):
                        print(FO2(s1))
                        bestSolution = s1
                        _history.append( copy.deepcopy(bestSolution) )
                else:
                    x = random.random()
                    if x < e**(-delta/T):
                        solucaoCorrente = s1

            # print(f'T {T}, iterT {iterT}')
        T = T * alpha
        iterT = 0
        # print(T)
    if _history == True:
        return _history

    return bestSolution


def buscarVizinho(solucao, T, T0, iterT, SAmax):
    coef = 1 - T/T0 # 0 < coef < 1
    beta = iterT / SAmax

    # inicio do algoritmo
    # if coef > 0.5:
    #     return trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
    # else:
    #     return trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})

    fs = getLocalSearchFunctions(solucao, coef, beta)

    func = random.choice(fs)

    return func['f'](func['params'])

def getLocalSearchFunctions(solucao, coef, beta):
    # print(coef)

    if beta > 0.8:
        return [
            {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera, 'params': {'solucao': solucao, 'D': D, 'S': S, 'alpha': beta}},
            {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}}
        ]

    return [
        {'f': buscaLocal.trocaCirurgiasMesmoDia, 'params': {'solucao': solucao, 'D': D}},
        {'f': buscaLocal.trocaCirurgiasDiasDiferente, 'params': {'solucao': solucao, 'D': D}},
        {'f': buscaLocal.trocaCirurgiaMarcadaPorCirurgiaListaEspera, 'params': {'solucao': solucao}},
        # {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera, 'params': {'solucao': solucao, 'D': D, 'S': S, 'alpha': 0}},
        {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}}
    ]
