import random 
import copy
from math import e

from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, filterBy
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
import buscaLocal
# from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, trocaCirurgiaMarcadaPorCirurgiaListaEspera, removeCirurgias


# SAmax: numero maximo de iteracoes Metropolis para cadaTemperatura
# alpha: taxa de resfriamento 0 < alpha < 1
# T0: temperatura inicial
def simulatedAnealing(solucaoInicial, config, FO, T0=100, SAmax=100, alpha=0.5, _history = False, maxIterSemMelhoras = 1000, verbose = False, maxPetelecos = 3):
    
    #armazena as atualizacoes de best
    _history = []
    
    bestSolution =  copy.deepcopy(solucaoInicial)
    solucaoCorrente =  copy.deepcopy(solucaoInicial)
    iterT = 0
    T = T0

    iterSemMelhoras = 0
    nPetelecos = 0
    while T > 0.0001:
        while iterT < SAmax:
            iterT = iterT + 1
            iterSemMelhoras += 1

            #gerar vizinho
            s1 = buscarVizinho(solucaoCorrente, config, T, T0, iterT, SAmax)
            delta = FO2(s1) - FO2(solucaoCorrente)
            if viavel(s1, config['S'], config['T'], config['D']) == True:
                if delta < 0:
                    solucaoCorrente = copy.deepcopy(s1)
                    if FO2(s1) < FO2(bestSolution):
                        if verbose:
                            _print(T, FO2(s1),  FO2(bestSolution) )
                        bestSolution = copy.deepcopy(s1)
                        _history.append( copy.deepcopy(bestSolution) )
                else:
                    x = random.random()
                    if x < e**(-delta/T):
                        solucaoCorrente = copy.deepcopy(s1)
                        iterSemMelhoras = 0
                        if FO2(s1) < FO2(bestSolution):
                            bestSolution = copy.deepcopy(s1)
                        if verbose:
                            _print(T, FO2(s1),  FO2(bestSolution) )
            
            #parar algoritmo mais cedo
            if iterSemMelhoras > maxIterSemMelhoras:
                if nPetelecos < maxPetelecos:
                    solucaoCorrente = peteleco(solucaoCorrente)
                    iterSemMelhoras = 0
                    nPetelecos += 1
                else:
                    break
        
        #parar algoritmo mais cedo
        if iterSemMelhoras > maxIterSemMelhoras:
            print(f'maximo de iteraçoes sem melhoras atingido {maxIterSemMelhoras}')
            break

            # print(f'T {T}, iterT {iterT}')
        T = T * alpha
        iterT = 0
        # print(T)
    if _history == True:
        return _history

    return bestSolution

def _print( T, fo, bestFO ):
    print(f'T: {T} - FO: {fo} - best: {bestFO}')


def buscarVizinho(solucao, config, T, T0, iterT, SAmax):
    coef = 1 - T/T0 # 0 < coef < 1
    beta = iterT / SAmax

    # inicio do algoritmo
    # if coef > 0.5:
    #     return trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})
    # else:
    #     return trocaCirurgiasDiasDiferente({'solucao': solucao, 'D': D})

    fs = getLocalSearchFunctions(solucao, config, coef, beta)

    func = random.choice(fs)

    return func['f'](func['params'])

def getLocalSearchFunctions(solucao, config, coef, beta):
    # print(coef)

    if beta > 0.8:
        return [
            {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera, 'params': {'solucao': solucao, 'D': config['D'], 'S': config['S'], 'alpha': beta}},
            {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}},
            {'f': buscaLocal.trocaP1PorD0, 'params': {'solucao': solucao}}
        ]

    return [
        {'f': buscaLocal.trocaCirurgiasMesmoDia, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.trocaCirurgiasDiasDiferente, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.trocaCirurgiaMarcadaPorCirurgiaListaEspera, 'params': {'solucao': solucao}},
        # {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera, 'params': {'solucao': solucao, 'D': config['D'], 'S': config['S'], 'alpha': beta}},
        {'f': buscaLocal.realocarHorario, 'params': {'solucao': solucao}},
        {'f': buscaLocal.realocarDia, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}},
        {'f': buscaLocal.trocaP1PorD0, 'params': {'solucao': solucao}}
    ]


def peteleco(solucao):
    print('\n\n\n\n\n\n PETELECO!! \n\n\n\n\n')
    alocadas = filterBy(solucao,'alocada', True)
    s = copy.deepcopy(solucao) 
    qtdARemover = random.randint(0, int(len(alocadas) * 0.35))
    for i in range(0, qtdARemover):
        s = buscaLocal.removeCirurgias({'solucao': s, 'alpha': random.random()})
    return s