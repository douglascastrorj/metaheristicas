from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia, getHorasPorCirurgiao
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia
import numpy as np

import plot
from time import time


S = 7
T = 46
D = 5

config = {
    'S': S,
    'T': T,
    'D': D
}

REPLICACOES = 1

dataset = readDataset('dataset/i100p115percent.csv')
cirurgias = createMap(dataset)

# cirurgias = gerarInstancia(N=50, H=10, E=4)
# cirurgias = gerarInstancia(N=20, H=5, E=4)

FOS = []
times = []
for i in range(0, REPLICACOES):

    start = time()
    xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=True)

    solucao = xcstdToMap(xcstd, cirurgias)
    v = viavel(solucao, S, T, D, verbose=True)

    print(solucao)
    print(f'FO Inicial: {FO2(solucao)} - Viavel: {v }')
    # print(getHorasPorCirurgiao(solucao))

    best = simulatedAnealing(solucao, config, FO2, SAmax=250, T0=300, alpha=0.6, verbose=False, maxPetelecos=1)

    end = time()

    fobest = FO2(best)
    FOS.append(fobest)
    times.append(end - start)

    

    print(best)
    print(f'\n\n(SOLUCAO INICIAL) FO = {FO2(solucao)}  - Viavel: {viavel(solucao, S, T, D)} \n\n')
    print(f'(MELHOR SOLUCAO) FO = {FO2(best)}  - Viavel: {viavel(best, S, T, D)} \n\n')

    plot.exportGradeHorarios(best, config)

    print(getHorasPorCirurgiao(best))

print(f'FO Media: {np.array(FOS).mean()} - tempo medio: {np.array(times).mean()}')
