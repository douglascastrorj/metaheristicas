import random 
import copy
from math import e

from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, filterBy, getHorasPorCirurgiao
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
import buscaLocal
# from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, trocaCirurgiaMarcadaPorCirurgiaListaEspera, removeCirurgias


# SAmax: numero maximo de iteracoes Metropolis para cadaTemperatura
# alpha: taxa de resfriamento 0 < alpha < 1
# T0: temperatura inicial
def simulatedAnealing(solucaoInicial, config, FO, T0=100, SAmax=100, alpha=0.5, _history = False, maxIterSemMelhoras = 500, verbose = False, maxPetelecos = 3, pathrelinking=False):
    
    #armazena as atualizacoes de best
    _history = []
    
    bestSolution =  copy.deepcopy(solucaoInicial)
    solucaoCorrente =  copy.deepcopy(solucaoInicial)
    iterT = 0
    T = T0

    iterSemMelhoras = 0
    nPetelecos = 0
    while T > 0.001:
        while iterT < SAmax:
            iterT = iterT + 1
            iterSemMelhoras += 1
            
            #gerar vizinho
            s1 = buscarVizinho(copy.deepcopy(solucaoCorrente), config, T, T0, iterT, SAmax)

            foS1 = FO2(s1)
            foCorrente = FO2(solucaoCorrente)
            foBest = FO2(bestSolution)

            delta = foS1 - foCorrente
            x = random.random()
            # print(f'T: {T} delta {delta} e**(-delta/T): {e**(-delta/T)} x: {x}, x < e**(-delta/T): {x < e**(-delta/T)}')
            if viavel(s1, config['S'], config['T'], config['D']) == True:
                if delta < 0:
                    solucaoCorrente = copy.deepcopy(s1)
                    if foS1 < foBest:
                        if verbose:
                            _print(T, foS1,  foBest )
                        bestSolution = copy.deepcopy(s1)
                        _history.append( {'solucao': copy.deepcopy(bestSolution), 'fo': foBest } )
                        iterSemMelhoras = 0
                else:
                    
                    if x < e**(-delta/T):
                        # print('aceitou piora')
                        _history.append( {'solucao': copy.deepcopy(s1), 'fo': foS1 } )
                        solucaoCorrente = copy.deepcopy(s1)
                        if foS1 < foBest:
                            bestSolution = copy.deepcopy(s1)
                        if verbose:
                            _print(T, foS1,  foBest )
            # else:
                # if verbose:
                    # print(f'Solucao Inviavel: {foS1}')
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

    if pathrelinking:
        sliceIndex = int( len(_history) * 0.5 )
        solucoesElite = sorted(_history, key=lambda k: k['fo'])[:sliceIndex]
        return pathRelinking(bestSolution, solucoesElite, config)

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
            {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera2, 'params': {'solucao': solucao, 'D': config['D'], 'S': config['S'], 'T': config['T'], 'alpha': beta}},
            {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}},
            {'f': buscaLocal.trocaP1PorD0, 'params': {'solucao': solucao}},
            {'f': buscaLocal.removeOciosidadeCirurgiao, 'params': {'solucao': solucao, 'S': config['S'], 'T': config['T'], 'D': config['D']}},
            {'f': buscaLocal.antecipaPrioridadeMaisBaixa, 'params': {'solucao': solucao, 'S': config['S'], 'T': config['T'], 'D': config['D']}}
        ]

    return [
        {'f': buscaLocal.trocaCirurgiasMesmoDia, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.trocaCirurgiasDiasDiferente, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.trocaCirurgiaMarcadaPorCirurgiaListaEspera, 'params': {'solucao': solucao}},
        {'f': buscaLocal.insercaoDeUmaOuMaisCirurgiasDaListaEspera2, 'params': {'solucao': solucao, 'D': config['D'], 'S': config['S'], 'T': config['T'], 'alpha': beta}},
        {'f': buscaLocal.realocarHorario, 'params': {'solucao': solucao}},
        {'f': buscaLocal.realocarDia, 'params': {'solucao': solucao, 'D': config['D']}},
        {'f': buscaLocal.removeCirurgias, 'params': {'solucao': solucao, 'alpha': coef}},
        {'f': buscaLocal.trocaP1PorD0, 'params': {'solucao': solucao}},
        {'f': buscaLocal.desalocaNaoP1D0, 'params': {'solucao': solucao}},
        {'f': buscaLocal.removeOciosidadeCirurgiao, 'params': {'solucao': solucao, 'S': config['S'], 'T': config['T'], 'D': config['D']}},
        {'f': buscaLocal.antecipaPrioridadeMaisBaixa, 'params': {'solucao': solucao, 'S': config['S'], 'T': config['T'], 'D': config['D']}}
    ]


def peteleco(solucao):
    print('\n\n PETELECO!! \n')
    alocadas = filterBy(solucao,'alocada', True)
    s = copy.deepcopy(solucao) 
    qtdARemover = random.randint(0, int(len(alocadas) * 0.35))
    for i in range(0, qtdARemover):
        s = buscaLocal.removeCirurgias({'solucao': s, 'alpha': random.random()})
    return s


def pathRelinking(best, solucoesElite, config):
    print('\nPATH RELINKING\n')
    # print(len(solucoesElite), ' utilizando solucoes elite')

    for i in range (0, 50):
        inicial = copy.deepcopy( random.choice(solucoesElite)['solucao'] )
        guia = random.choice(solucoesElite)['solucao']

        viaveis = []
        for c in inicial:
            if guia[c]['alocada'] == False:
                continue

            if iguais(guia[c], inicial[c]) == False:
                alocarCirurgia(inicial, c, guia[c]['sala'], guia[c]['horaInicio'], guia[c]['dia'])
                if viavel(inicial, config['S'], config['T'], config['D']) == True:
                    print('VIAVEL PATH RELINKING')
                    print(f'BEST: {FO2(best)} - corrente: {FO2(inicial)}')
                    viaveis.append({'solucao':copy.deepcopy(inicial), 'fo': FO2(inicial) })
                    if FO2(inicial) < FO2(best):
                        best = copy.deepcopy(inicial)
                else:
                    desalocarCirurgia(inicial, c)


    # print(FO2(best))
    # for solucaoElite in solucoesElite:
    #     #introduzir caracteristicaas da solucao elite na solucao corrente
    #     best = alocaCirurgiaDaSolucaoElite(best, solucaoElite['solucao'], config)
    #     best = removeOciosidadeCirurgiao(best, solucaoElite['solucao'], config)
    #     pass
    
    # print(FO2(best))
    # print('\n\n\n')
    return best


def alocarCirurgia(solucao, idCirurgia, s, t, d):
    solucao[idCirurgia]['dia'] = d
    solucao[idCirurgia]['sala'] = s
    solucao[idCirurgia]['horaInicio'] = t
    solucao[idCirurgia]['horaFim'] = t + solucao[idCirurgia]['duracao']
    solucao[idCirurgia]['alocada'] = True


def desalocarCirurgia(solucao, idCirurgia):
    solucao[idCirurgia]['dia'] = None
    solucao[idCirurgia]['sala'] = None
    solucao[idCirurgia]['horaInicio'] = None
    solucao[idCirurgia]['horaFim'] = None
    solucao[idCirurgia]['alocada'] = False

def alocaCirurgiaDaSolucaoElite(solucao, solucaoElite, config):
    solucaoCpy = copy.deepcopy(solucao)

    # print(solucaoElite)

    for cElite in solucaoElite:
        #alocar solucao
        for d in range(0, config['D']):
            for s in range(0, config['S']):
                for t in range(0, config['T'] - solucaoCpy[cElite]['duracao']):
                    if solucaoCpy[cElite]['alocada'] == False and solucaoElite[cElite]['alocada'] == True:
                        alocarCirurgia(solucaoCpy, cElite, s, t, d)
                        if viavel(solucaoCpy, config['S'], config['T'], config['D'] ) == False:
                            desalocarCirurgia(solucaoCpy, cElite)
    
    return solucaoCpy

def removeOciosidadeCirurgiao(solucao, solucaoElite, config):
    solucaoCpy = copy.deepcopy(solucao)

    horasCirurgioesBest = getHorasPorCirurgiao(solucao)
    horasCirurgioesSolucaoElite = getHorasPorCirurgiao(solucaoElite)

    print('remove ociosidade')
    for cirurgiao in horasCirurgioesSolucaoElite:
        # if horasCirurgioesSolucaoElite[cirurgiao]['horasSemana'] > horasCirurgioesBest[cirurgiao]['horasSemana']:
        print('cirurgiao', cirurgiao)
        if True:
            for c in solucaoCpy:
                if solucaoCpy[c]['alocada'] == True:
                    continue
                if solucaoCpy[c]['cirurgiao'] == cirurgiao:
                    for d in range(0, config['D']):
                        for s in range(0, config['S']):
                            for t in range(0, config['T'] - solucaoCpy[c]['duracao']):
                                if solucaoCpy[c]['alocada'] == True:
                                    continue
                                alocarCirurgia(solucaoCpy, c, s, t, d)
                                if viavel(solucaoCpy, config['S'], config['T'], config['D'] ) == False:
                                    desalocarCirurgia(solucaoCpy, c)
                                else:
                                    print('conseguiu alocar cirurgia de cirurgiao ocioso')
                                    print(f'Cirurgia {c} Cirurgiao {cirurgiao}')

    return solucaoCpy


def iguais(cirurgia1, cirurgia2):
    if cirurgia1['id'] != cirurgia2['id']:
        return False
    if cirurgia1['alocada'] != cirurgia2['alocada']:
        return False
    if cirurgia1['horaInicio'] != cirurgia2['horaInicio']:
        return False
    if cirurgia1['horaFim'] != cirurgia2['horaFim']:
        return False
    if cirurgia1['dia'] != cirurgia2['dia']:
        return False
    if cirurgia1['sala'] != cirurgia2['sala']:
        return False
    return True