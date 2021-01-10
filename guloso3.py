from utils import xcstdToMap, alocarCirurgia, desalocarCirurgia, filterBy, filterNotBy, createDecisionDict, getDistinctSpecialtyArr2, createMedicSlotMap, createEspecialidadesSalaDia, mapToList, getPenalizacao, getIndexFromId 
import numpy as np
from operator import itemgetter
from fitness import viavel
import random

MAX_SLOTS_MEDICO_DIA = 24
MAX_SLOTS_MEDICO_SEMANA = 100
T = 46



def gerarSolucaoInicial(cirurgias, config, verbose = False):

    # print(cirurgiasP1)
    # print(demaisCirurgias)

    E = getDistinctSpecialtyArr2(cirurgias)
    Xcstd, _, _ = createDecisionDict(cirurgias, config['S'], config['T'], config['D'], E)

    solucao = xcstdToMap(Xcstd, cirurgias)
  
    cirurgiasP1 = filterBy(cirurgias, 'p', 1)
    demaisCirurgias = filterNotBy(cirurgias, 'p', 1)

    tempoSalas = np.zeros((config['S'], config['D']))

    alocarPrimeiroSlotDisponivel(solucao, cirurgiasP1, config, tempoSalas)
    alocarPrimeiroSlotDisponivel(solucao, demaisCirurgias, config, tempoSalas)
    
    return solucao


def alocarPrimeiroSlotDisponivel(solucao, cirurgias, config, tempoSalas):
    cirurgias_ = mapToList(cirurgias)
    cirurgias_ = ordenaCirurgias(cirurgias_)

    for cirurgia in cirurgias_:
        cP1 = cirurgia['c']
        # print(cP1)
        if solucao[cP1]['alocada'] == True:
            continue
        
        breakLoop = False
        for d in range(0, config['D']):
            for s in range(0, config['S']):
                
                if config['T'] - tempoSalas[s][d] < solucao[cP1]['duracao']:
                    breakLoop = True
                    break

                slotInicial = int(tempoSalas[s][d])
                for t in range(slotInicial, config['T'] - solucao[cP1]['duracao']):
                    if solucao[cP1]['alocada'] == True:
                        continue
                    alocarCirurgia(solucao, cP1, s, t, d)
                    if viavel(solucao, config['S'], config['T'], config['D'] ) == False:
                        desalocarCirurgia(solucao, cP1)
                    else:
                        if tempoSalas[s][d] >= 0: 
                            tempoSalas[s][d] += 2
                            tempoSalas[s][d] += solucao[cP1]['duracao']

                        breakLoop = True
                        break
                if breakLoop:
                    break
            if breakLoop:
                break



def getCoeficienteOrdenacao(cirurgia):
    penalidade = getPenalizacao(cirurgia['p'])
    diasEspera = cirurgia['w']

    return float(penalidade) / (diasEspera + 0.1)


def ordenaCirurgias(cirurgias):  
    # print(cirurgias)  
    for i in range(0, len(cirurgias)):
        for j in range(0, len(cirurgias)):
            valor1 = getCoeficienteOrdenacao(cirurgias[i])
            valor2 = getCoeficienteOrdenacao(cirurgias[j])
            if valor1 < valor2:
                swap = cirurgias[j]
                cirurgias[j] = cirurgias[i]
                cirurgias[i] = swap
    return cirurgias
