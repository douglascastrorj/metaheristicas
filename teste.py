from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia, getHorasPorCirurgiao
from guloso2 import gerarSolucaoInicial
from fitness import fitnessFunction, FO2, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia
import numpy as np

import plot
from time import time


S = 10
T = 46
D = 5

config = {
    'S': S,
    'T': T,
    'D': D
}

REPLICACOES = 1


instancias = [
    # { 'path': 'instancias/i1.csv',   'S': 2 },
    # { 'path': 'instancias/i2.csv',   'S': 2 },
    # { 'path': 'instancias/i3.csv',   'S': 2 },
    # { 'path': 'instancias/i4.csv',   'S': 2 },
    # { 'path': 'instancias/i5.csv',   'S': 6 },
    # { 'path': 'instancias/i6.csv',   'S': 8 },
    # { 'path': 'instancias/i7.csv',   'S': 3 },
    # { 'path': 'instancias/i8.csv',   'S': 7 },
    # { 'path': 'instancias/i9.csv',   'S': 6 },
    # { 'path': 'instancias/i10.csv',   'S': 10 },
    # { 'path': 'instancias/i11.csv',   'S': 15 },
    # { 'path': 'instancias/i12.csv',   'S': 3 },
    # { 'path': 'instancias/i13.csv',   'S': 4 },
    { 'path': 'instancias/i14.csv',   'S': 7 }
]

# f = open('output_replicacoes.txt', 'w')

# v = viavel(solucao, S, T, D, verbose=True)
# print(f'Viavel: {v}')

for instancia in instancias:

    config['S'] = instancia['S']
    dataset = readDataset(instancia['path'])
    cirurgias = createMap(dataset)

    # cirurgias = gerarInstancia(N=50, H=10, E=4)
    # cirurgias = gerarInstancia(N=20, H=5, E=4)

    FOS = []
    times = []
    for i in range(0, REPLICACOES):

        start = time()
        xcstd, yesd, z = gerarSolucaoInicial(cirurgias, S, D, verbose=False)

        solucao = xcstdToMap(xcstd, cirurgias)
        v = viavel(solucao, S, T, D, verbose=True)

        # print(solucao)
        print(f'FO Inicial: {FO2(solucao)} - Viavel: {v }')
        # print(getHorasPorCirurgiao(solucao))

        best = simulatedAnealing(solucao, config, FO2, SAmax=100, T0=1000, alpha=0.6, verbose=True, maxPetelecos=0, pathrelinking=False)

        end = time()

        fobest = FO2(best)
        FOS.append(fobest)
        times.append(end - start)

        

        print(best)
        print(f'REPLICACAO: {i} - Instancia: {instancia["path"]} - S: {instancia["S"]}')
        print(f'\n\n(SOLUCAO INICIAL) FO = {FO2(solucao)}  - Viavel: {viavel(solucao, S, T, D)} \n\n')
        print(f'(MELHOR SOLUCAO) FO = {FO2(best)}  - Viavel: {viavel(best, S, T, D)} \n\n')

        plot.exportGradeHorarios(best, config)

        print(getHorasPorCirurgiao(best))

    print(f'FO Media: {np.array(FOS).mean()} - tempo medio: {np.array(times).mean()}')

    # f.write(f'REPLICACOES: {REPLICACOES} - Instancia: {instancia["path"]} - S: {instancia["S"]}')
    # f.write(f'FO Media: {np.array(FOS).mean()} - tempo medio: {np.array(times).mean()}\n\n')
