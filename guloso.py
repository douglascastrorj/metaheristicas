from utils import createDecisionVar, getSurgeryByPriority, getDistinctSpecialty, getCirurgia, getSurgeriesBySpecialty, getIdFromIndex, getIndexFromId
import numpy as np

# argmax ( qtd(cirurgias e) / Sum(tc e) )
def getMelhorEspecialidadesParaAtender(dataset, cirurgias, E):
    tce = np.zeros(E)
    qtde = np.zeros(E)

    # print('tce', tce)
    for c in cirurgias:
        cirurgia = getCirurgia(dataset, c)
        e = getIndexFromId(cirurgia['e'])
        tc = cirurgia['tc']

        tce[e] = tce[e] + tc
        qtde[e] = qtde[e] + 1

    #solucao de contorno para minimizar ignorando o 0
    for e in range(0, E):
        if qtde[e] == 0 or tce[e] == 0:
            tce[e] = 1
            qtde[e] = np.Infinity
    
    densidade = qtde / tce

    # transformar de indice em id
    return  getIdFromIndex(np.argmin(densidade))

def filtrarPorMelhorEspecialidade(dataset, cirurgias, E):
    melhorEspecialidade = getMelhorEspecialidadesParaAtender(dataset, cirurgias, E)

    print('melhorEspecialidade = ', melhorEspecialidade)
    return getSurgeriesBySpecialty(dataset, melhorEspecialidade)

# falta validar se profissional pode atender (cirurgia) cirurgias nao 

def gerarSolucaoInicial(dataset, S):

    # filtrar cirurgias de prioridade 1
    priority1 = getSurgeryByPriority(dataset, 1)

    C = len(dataset['c'])
    T = 46
    D = 5
    E = getDistinctSpecialty(dataset)

    # print('distinct e ', E)

    #criar variaveis de decisao
    Xcstd, _, __ = createDecisionVar(C, S, T, D, E)

    cirurgiasAtendidas = np.zeros(C)
    tempoSalas = np.zeros(S)

    priority1MelhorEspecialidade = filtrarPorMelhorEspecialidade(dataset, priority1, E)
    #preencher prioridades 1
    for s in range(0, S):
        for c in priority1MelhorEspecialidade:
            cirurgia = getCirurgia(dataset, c)

            if(cirurgiasAtendidas[c] == 1):
                continue

            if(tempoSalas[s] + cirurgia['tc'] + 2 > 46):
                continue
            
            for t in range(0, cirurgia['tc']):
                Xcstd[c][s][t][0] = 1

            cirurgiasAtendidas[c] = 1

            if tempoSalas[s] > 0:
                tempoSalas[s] = tempoSalas[s] + 2 #somar 2 slots de higienizacao entre cirurgias

            tempoSalas[s] = tempoSalas[s] + cirurgia['tc']
    
    for s in range(0, S):
        for c in range(0, C):
            cirurgia = getCirurgia(dataset, c)

            if(cirurgiasAtendidas[c] == 1):
                continue

            if(tempoSalas[s] + cirurgia['tc'] + 2 > 46):
                continue

            # respeitar conceito de bloco fechado

    
    return Xcstd
