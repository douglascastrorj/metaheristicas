from utils import readDataset, createMap, filterBy, getDistinctSpecialtyArr, xcstdToMap, desalocarCirurgia, getHorasPorCirurgiao
import guloso2 
import guloso3
from fitness import fitnessFunction, FO2, viavel
from buscaLocal import trocaCirurgiasMesmoDia, trocaCirurgiasDiasDiferente, insercaoDeUmaOuMaisCirurgiasDaListaEspera, removeCirurgias
from metaheuristica import simulatedAnealing
from instancias import gerarInstancia
import numpy as np

import plot
from time import time

T = 46
D = 5


REPLICACOES = 50


instancias = [
    # { 'path': 'instancias/i1.csv',   'S': 2 },
    # { 'path': 'instancias/i2.csv',   'S': 2 },
    { 'path': 'instancias/i3.csv',   'S': 2 },
    { 'path': 'instancias/i4.csv',   'S': 2 },
    # { 'path': 'instancias/i5.csv',   'S': 6 },
    # { 'path': 'instancias/i6.csv',   'S': 8 },
    # { 'path': 'instancias/i7.csv',   'S': 3 },
    # { 'path': 'instancias/i8.csv',   'S': 7 },
    # { 'path': 'instancias/i9.csv',   'S': 6 },
    # { 'path': 'instancias/i10.csv',   'S': 10 },
    # { 'path': 'instancias/i11.csv',   'S': 15 },
    # { 'path': 'instancias/i12.csv',   'S': 3 },
    # { 'path': 'instancias/i13.csv',   'S': 4 },
    # { 'path': 'instancias/i14.csv',   'S': 7 }
]



# v = viavel(solucao, S, T, D, verbose=True)
# print(f'Viavel: {v}')

ilss = [ False, True ]
for instancia in instancias:
    for ils in ilss:

        f = open(f'resultados/times_resultado_{instancia["path"].split("/")[1]}-ils-{ils}-proximidade-3percent.txt', 'w')
            
        config = {
            'S': instancia['S'],
            'T': T,
            'D': D
        }
        dataset = readDataset(instancia['path'])
        cirurgias = createMap(dataset)

        # cirurgias = gerarInstancia(N=50, H=10, E=4)
        # cirurgias = gerarInstancia(N=20, H=5, E=4)

        FOS = []
        times = []
        for i in range(0, REPLICACOES):

            start = time()
            # print('gerando solucao inicial')
            xcstd, _, _ = guloso2.gerarSolucaoInicial(cirurgias, config['S'], config['D'])
            solucao = xcstdToMap(xcstd, cirurgias)
            # v = viavel(solucao,  config['S'], config['T'], config['D'], verbose=True)
            # if v == False:
            #     print('metodo legado falhou gerando por segundo metodo')
            # solucao = guloso3.gerarSolucaoInicial(cirurgias, config, verbose=False)

            
            v = viavel(solucao,  config['S'], config['T'], config['D'], verbose=False)
            if v == False:
                while v == False:
                    v = viavel(solucao,  config['S'], config['T'], config['D'], verbose=False , removeCirurgiaInviavel=True)
                    # print('removendo cirurgia inviavel')

            # print(f'FO Inicial: {FO2(solucao)} - Viavel: {v }')
            # print(getHorasPorCirurgiao(solucao))

            # print('executando simulated anealing')
            best = simulatedAnealing(solucao, config, FO2, SAmax=100, T0=1000, alpha=0.6, verbose=False, maxPetelecos=0, ils=True, bestFO=1518585)
            # history = simulatedAnealing(solucao, config, FO2, SAmax=100, T0=1000, alpha=0.6, verbose=False, maxPetelecos=0, pathrelinking=False, ils=ils, history=True)
            # plot.plotChart(history, instancia["path"].split("/")[1])
            end = time()

            fobest = FO2(best)
            FOS.append(fobest)
            times.append(end - start)

            

            # print(best)
            print(f'REPLICACAO: {i} - Instancia: {instancia["path"]} - S: {instancia["S"]}')
            print(f'\n\n(SOLUCAO INICIAL) FO = {FO2(solucao)}  - Viavel: {viavel(solucao, config["S"], config["T"], config["D"])} \n\n')
            print(f'(MELHOR SOLUCAO) FO = {FO2(best)}  - Viavel: {viavel(best, config["S"], config["T"],config["D"], verbose=False)} \n\n')
            
            f.write(f'{end - start}\n')
            # plot.exportGradeHorarios(best, config)

            # print(getHorasPorCirurgiao(best))

        print(f'FO Media: {np.array(FOS).mean()} - tempo medio: {np.array(times).mean()}')
        print(f'FO Desvio: {np.array(FOS).std()} - tempo desvio: {np.array(times).std()}')
        print(f'FO Mediana: {np.median(FOS)} - tempo mediana: {np.median(times)}')
        print(f'FO min: {np.array(FOS).min()} - tempo min: {np.array(times).min()}')
        print(f'FO max: {np.array(FOS).max()} - tempo max: {np.array(times).max()}')

        # f.write(f'REPLICACOES: {REPLICACOES} - Instancia: {instancia["path"]} - S: {instancia["S"]}\n')
        # f.write(f'FO Media: {np.array(FOS).mean()} - tempo medio: {np.array(times).mean()}\n')
        # f.write(f'FO Desvio: {np.array(FOS).std()} - tempo desvio: {np.array(times).std()}\n')
        # f.write(f'FO Mediana: {np.median(FOS)} - tempo mediana: {np.median(times)}\n')
        # f.write(f'FO min: {np.array(FOS).min()} - tempo min: {np.array(times).min()}\n')
        # f.write(f'FO max: {np.array(FOS).max()} - tempo max: {np.array(times).max()}\n')
            
        # f.close()
